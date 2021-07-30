# Create your models here.

from django.conf import settings
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import pre_save



# Functions
def _get_upload_path(instance, filename):
    return instance.upload_path(filename)

# Models
class UserProfile(models.Model):

    # Relations
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    # Attributes
    email = models.EmailField(
        _('email'),
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=200,
        blank=True,
        null=True,
    )
    picture = models.ImageField(
        _('picture'),
        blank=True,
        upload_to=_get_upload_path,
    )

    # Meta Data
    created_on = models.DateTimeField(
        _('created on'),
        auto_now_add=True,
        editable=False,
        null=True,
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now=True,
        editable=False,
        null=True,
    )

    # Meta
    class Meta:
        ordering = ['user']
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    # Functions
    def __str__(self):
        return "%s - %s" % (self.user)

    def __unicode__(self):
        return u"%s - %s" % (self.user)

    def upload_path(self, filename=None):
        path = '%s/%s' % (
            'userprofile',
            time.strftime('%Y/%m/%d', datetime.now())
        )
        if filename:
            path += '/%s' % filename
        return path


class Project(models.Model):
    # Choices
    STATUS_CHOICES = (
        ('c', _('Completed')),
        ('o', _('On Progress')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(
        _('content'),
        blank=True
    )
    text = models.TextField(blank=True)
    status = models.CharField(
        _('status'),
        choices=STATUS_CHOICES,
        max_length=1,
        default='o'
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class ProjectItem(models.Model):
    # Choices
    STATUS_CHOICES = (
        ('c', _('Completed')),
        ('o', _('On Progress')),
    )

    # Relations
    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(
        _('content'),
        blank=True
    )
    text = models.TextField(blank=True)
    status = models.CharField(
        _('status'),
        choices=STATUS_CHOICES,
        max_length=1,
        default='o'
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
