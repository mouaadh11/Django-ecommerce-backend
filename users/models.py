# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        # On s'assure que le username est défini sur l'email si absent
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    We extend Django's built-in User model.
    AbstractUser already gives us: username, email, password,
    first_name, last_name, is_staff, is_active, date_joined
    We add our own fields below.
    """
    email = models.EmailField(unique=True)   # Override to make email unique
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()  # Use our custom manager
    # Make email the login field instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Still required for createsuperuser

    def __str__(self):
        return self.email


class Address(models.Model):
    """Shipping/billing addresses belonging to a user."""
    ADDRESS_TYPES = [
        ('shipping', 'Shipping'),
        ('billing', 'Billing'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='shipping')
    full_name = models.CharField(max_length=100)
    street_line1 = models.CharField(max_length=255)
    street_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} — {self.city}, {self.country}"