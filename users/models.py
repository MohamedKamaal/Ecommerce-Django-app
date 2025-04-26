"""
Custom user manager and user model to add specific fields,
and use email instead of username for authentication.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model where authentication is done using email instead of username.
    Includes methods to create regular users and superusers.
    """

    def create_user(self, email, password, **kwargs):
        """
        Creates and returns a user with an email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.
            **kwargs: Additional keyword arguments for user fields.

        Raises:
            ValueError: If the email is not provided or invalid.

        Returns:
            User: The created user instance.
        """
        # check for username

        # check for email
        if not email:
            raise ValueError("You must provide an email to register")
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Email is not valid")
        # normalize email
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        # add password after being hashed
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Creates and returns a superuser with admin privileges.

        Args:
            email (str): The email address of the superuser.
            password (str): The password of the superuser.
            **kwargs: Additional keyword arguments for user fields.

        Returns:
            User: The created superuser instance.
        """
        user = self.create_user(email, password, **kwargs)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    USERNAME_FIELD = "email"


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model where email is the unique identifier for authentication
    instead of usernames. Includes fields for:
    first name, last name, email, date joined
    and status flags (active, staff, superuser).
    """

    username = None
    first_name = models.CharField(
        max_length=100,
        verbose_name="First Name",
        help_text="Enter your first name"
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Last Name",
        help_text="Enter your last name"
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name="Email Address",
        help_text="Enter a valid email address. This will be used for login."
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Joined",
        help_text="The date and time when the user was created."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this user should be treated as active."
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Staff Status",
        help_text="Designates whether the user can log into the admin site."
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Superuser Status",
        help_text="Designates that this user has all permissions without explicitly assigning them."
    )


    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this user.

        Args:
            subject (str): Subject of the email.
            message (str): Email message content.
            from_email (str, optional): Sender's email.
            **kwargs: Additional email sending options.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        """
        Returns the string representation of the user, which is their email.
        """
        return str(self.email)
