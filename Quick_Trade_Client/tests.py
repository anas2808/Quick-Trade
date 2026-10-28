from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import UserRegistrationForm
from .models import CustomUser, Message, Product, main_categories


class QuickTradeTestDataMixin:
    def create_user(self, email, username, password="TestPassword!234"):
        return CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=username.title(),
            last_name="Tester",
        )

    def create_category(self, name="Electronics"):
        return main_categories.objects.create(categories_name=name, image="category.png")

    def create_product(self, seller, category, **kwargs):
        defaults = {
            "name": "Test phone",
            "description": "A phone in good condition",
            "price": Decimal("12000.00"),
            "condition": "Good",
            "location": "Ahmedabad",
            "image": "listing_images/test.jpg",
            "ad_status": "Active",
            "expiry_date": timezone.now() + timedelta(days=10),
            "main_category": category,
            "seller": seller,
        }
        defaults.update(kwargs)
        return Product.objects.create(**defaults)


class RegistrationFormTests(TestCase):
    def test_registration_requires_terms_acceptance(self):
        form = UserRegistrationForm(data={
            "username": "newmember",
            "email": "newmember@example.com",
            "first_name": "New",
            "last_name": "Member",
            "phone": "",
            "bio": "",
            "password": "TestPassword!234",
            "confirm_password": "TestPassword!234",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("terms_accepted", form.errors)

    def test_registration_rejects_mismatched_passwords(self):
        form = UserRegistrationForm(data={
            "username": "newmember",
            "email": "newmember@example.com",
            "first_name": "New",
            "last_name": "Member",
            "phone": "",
            "bio": "",
            "password": "TestPassword!234",
            "confirm_password": "DifferentPassword!234",
            "terms_accepted": "on",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("confirm_password", form.errors)


class ListingAndMessagingTests(QuickTradeTestDataMixin, TestCase):
    def setUp(self):
        self.seller = self.create_user("seller@example.com", "seller")
        self.other_user = self.create_user("buyer@example.com", "buyer")
        self.category = self.create_category()
        self.product = self.create_product(self.seller, self.category)

    def test_product_list_filters_search_and_price_together(self):
        self.create_product(
            self.seller,
            self.category,
            name="Budget laptop",
            price=Decimal("7000.00"),
        )
        response = self.client.get(reverse("product_list"), {
            "search": "phone",
            "price_min": "10000",
            "price_max": "15000",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test phone")
        self.assertNotContains(response, "Budget laptop")

    def test_owner_can_open_edit_listing(self):
        self.client.force_login(self.seller)
        response = self.client.get(reverse("update_product", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_edit_listing(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse("update_product", args=[self.product.id]))
        self.assertEqual(response.status_code, 404)

    def test_get_request_does_not_delete_listing(self):
        self.client.force_login(self.seller)
        response = self.client.get(reverse("delete_listing", args=[self.product.id]))
        self.assertRedirects(response, reverse("profile"))
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_owner_can_delete_listing_with_post(self):
        self.client.force_login(self.seller)
        response = self.client.post(reverse("delete_listing", args=[self.product.id]))
        self.assertRedirects(response, reverse("profile"))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_message_detail_is_private_to_participants(self):
        message = Message.objects.create(
            sender=self.seller,
            receiver=self.other_user,
            product=self.product,
            subject="Question",
            content="Is this available?",
        )
        stranger = self.create_user("stranger@example.com", "stranger")
        self.client.force_login(stranger)
        response = self.client.get(reverse("message_detail", args=[message.id]))
        self.assertRedirects(response, reverse("message_list"))
