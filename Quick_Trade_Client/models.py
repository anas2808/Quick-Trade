from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
# Create your models here.

class main_categories(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    categories_name = models.CharField(max_length=100,unique=True)
    image=models.CharField(null=False,max_length=100)
    
    class Meta:
        db_table = 'main_categories'
        
    def __str__(self):
        return self.categories_name
    
    
# class sub_categories(models.Model):
#     id= models.AutoField(primary_key=True,unique=True)
#     main_categories = models.ForeignKey(main_categories, on_delete=models.CASCADE)
#     sub_categories_name= models.CharField(max_length=100,unique=True)
#     image=models.CharField(null=False,max_length=100)
    
#     class Meta:
#         db_table = 'sub_categories'
        
#     def __str__(self):
#         return self.sub_categories_name
    
    


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.registration_date = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True)
    bio = models.TextField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # Override related_name for reverse relationships
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

def get_30_days_later():
    return timezone.now() + timedelta(days=30)

class Product(models.Model):
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Like New', 'Like New'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor'),
    ]
    Ad_Status_Choice=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Pending','Pending'),
        ( 'Expired', 'Expired'),
        ('Rejected','Rejected'),
    ]
    
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=64, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=128)
    image = models.ImageField(upload_to='listing_images/')
    created_at = models.DateTimeField(default=timezone.now)
    expiry_date=models.DateTimeField(default=get_30_days_later)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    ad_status=models.CharField(max_length=64,choices=Ad_Status_Choice,default='Pending')
    main_category = models.ForeignKey(main_categories, on_delete=models.CASCADE, related_name='products')
    
    
    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    subject = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.subject}"
    
    class Meta:
        ordering = ['-created_at']