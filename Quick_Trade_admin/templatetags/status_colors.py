from django import template

register = template.Library()

@register.filter
def get_status_color(status):
    return {
        'Active': 'green',
        'Inactive': 'gray',
        'Pending': 'orange',
        'Expired': 'blue',
        'Rejected': 'red',
    }.get(status, 'black')
    
    
@register.filter
def get_status(status):
    return {
        'Active': 'success',
        'Inactive': 'primary',
        'Pending': 'warning',
        'Expired': 'danger',
        'Rejected': 'danger',
    }.get(status, 'dark') 
