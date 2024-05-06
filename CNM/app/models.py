from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Must have a username'))
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_posters', True)
        return self.create_user(username, password, **extra_fields)



GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
) 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
                        help_text=_('30 characters or less required. Contains only letters, numbers, and characters @/./+/-/_'),
                        error_messages={
                            'unique': _("The username already exists."),
                        },
                        null=False, blank=False
                        )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Specify the user who has all system administrative rights.'
        ), 
    )                                              
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Specify users with access to the admin page.'),
    )
    is_posters = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Specify users with permission to post'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Specify the user who is considered "active". Unselect to deactivate this account.'
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(_('LastLogin'), blank=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')
        ordering = ['username']


User = get_user_model()

def use_directory_paths(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, filename)
    return "user_{0}/{1}".format(instance.user.id, filename)

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,blank=False)
    image = models.FileField(upload_to=use_directory_paths, default="default.jpg", null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default="Other")
    facebook = models.URLField(null=True, blank=True)
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0.000)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = _('User Information')
        verbose_name_plural = _('User Information')
        ordering = ['date']



class Posts(models.Model):
    NORMAL = 'Normal'
    VIP = 'VIP'
    PRO = 'Pro'
    POST_TYPE_CHOICES = [
        (NORMAL, 'Normal'),
        (VIP, 'VIP'),
        (PRO, 'Pro'),
    ]

    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255, null=True, blank=True)
    available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    images1=models.ImageField(upload_to="images",null=True)
    images2=models.ImageField(upload_to="images",null=True)
    images3=models.ImageField(upload_to="images",null=True)
    images4=models.ImageField(upload_to="images",null=True)
    images5=models.ImageField(upload_to="images",null=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default=NORMAL)

    def __str__(self):
        return self.title

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



