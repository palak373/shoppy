from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import pre_save, post_save

from accounts.models import UserProfile
from accounts.signals import user_logged_in

from .signals import object_viewed_signal
from .utils import get_client_ip

class ObjectViewed(models.Model):
    user            = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} viewed on {}'.format(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

def object_viewed_reciever(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    new_obj_viewed = ObjectViewed.objects.create(user=request.user, ip_address=get_client_ip(request), content_type=c_type, object_id=instance.id)


object_viewed_signal.connect(object_viewed_reciever)

class UserSession(models.Model):
    user            = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    session_key     = models.CharField(max_length=100, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)
    ended           = models.BooleanField(default=True)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key)
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def user_session_post_save_reciever(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(pk=instance.id)
        for i in qs:
            i.end_session()
        if not instance.active and not instance.ended:
            instance.end_session()

post_save.connect(user_session_post_save_reciever, sender=UserSession)

def user_post_save_reciever(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for i in qs:
                i.end_session()

post_save.connect(user_post_save_reciever, sender=UserProfile)



def user_logged_in_reciever(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    user_session = UserSession.objects.create(user=user, ip_address=ip_address, session_key=session_key)

user_logged_in.connect(user_logged_in_reciever)