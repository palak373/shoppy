from django.db import models
from django.db.models.signals import post_save

from accounts.models import UserProfile

class MarketingPreference(models.Model):
    user            = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    subcribed       = models.BooleanField(default=False)
    mailchimp_msg   = models.TextField(blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


def marketing_pref_post_save_update(sender, instance, created, *args, **kwargs):
    if created:
        print('add user to mailchimp')

post_save.connect(marketing_pref_post_save_update, sender=MarketingPreference)


def marketing_pref_post_save(sender, instance, created, *args, **kwargs):
    if created:
        MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(marketing_pref_post_save, sender=UserProfile)