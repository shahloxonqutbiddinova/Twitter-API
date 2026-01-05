#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from api.models import User, UserConfirmation
#import random
#import string

#@receiver(post_save, sender = User)
#def create_user(sender, instance, created, **kwargs):
#    if created:
#       code = generate_pin()
#       UserConfirmation.objects.create(
#           user = instance,
#           code=code
#       )