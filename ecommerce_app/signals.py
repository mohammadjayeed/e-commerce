from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer

# Signal for autocreation of Customer object once a user is created
@receiver(post_save, sender=User)
def create_customer(sender, **kwargs):
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])

# Signal for deleting a user if the customer profile gets deleted
@receiver(post_delete, sender=Customer)
def delete_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()