import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user


    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        abstract = True
        ordering = ['email']


    def get_full_name(self):
        return self.email


    def get_short_name(self):
        return self.email


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""

        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractEmailUser):
    USER_TYPE_CHOICES = (
        ('seller', 'Seller'),
        ('customer', 'Customer')
    )
    user_type = models.CharField(
        choices=USER_TYPE_CHOICES,
        max_length=255, blank=True
    )
    full_name = models.CharField(
        'Full name', max_length=255, blank=True
    )
    bank_account = models.CharField(max_length=14, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activation_code = models.CharField(max_length=36,blank=True)


    def get_full_name(self):
        return self.full_name


    def get_short_name(self):
        return self.full_name


    def create_activation_code(self):
        self.activation_code = str(uuid.uuid4())


    @property
    def is_seller(self):
        return self.user_type == 'seller'

    @property
    def is_customer(self):
        return self.user_type == 'customer'


    def __str__(self):
        return '{name} < {email}'.format(
            name=self.full_name,
            email=self.email
        )


# class Profile(models.Model):
#     GENDER = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=120, blank=False)
#     last_name = models.CharField(max_length=120, blank=False)
#     gender = models.CharField(max_length=1, choices=GENDER)
#     address = models.CharField(max_length=255, blank=False)

#     def __unicode__(self):
#         return u'Profile of user: {0}'.format(self.user.email)


# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#         post_save.connect(create_profile, sender=User)


# def delete_user(sender, instance=None, **kwargs):
#     try:
#         instance.user
#     except User.DoesNotExist:
#         pass
#     else:
#         instance.user.delete()
#         post_delete.connect(delete_user, sender=Profile)




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )