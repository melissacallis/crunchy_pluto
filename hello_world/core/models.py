from django.db import models
from PIL import Image
from django.core.validators import MaxLengthValidator, FileExtensionValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Permission, BaseUserManager, Group
from django.utils.translation import gettext_lazy as _


def resize_profile_image(instance, filename):
    # Set your desired size
    max_size = (150, 150)

    # Define the relative path within the media directory
    upload_path = f"images/{instance.username}/{filename}"

    # Open the uploaded image using Pillow
    image = Image.open(instance.profile_image.path)

    # Resize the image
    image.thumbnail(max_size)

    # Save the resized image to the specified upload path
    media_root = settings.MEDIA_ROOT
    image.save(os.path.join(MEDIA_ROOT, upload_path))

    return upload_path

class UserProfileManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

class UserProfile(AbstractUser, PermissionsMixin):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, default='password')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    linkedin_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    project_link = models.URLField(blank=True)
    profile_image = models.ImageField(
        upload_to='images/',
        default='images/default.jpg',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
        ]
    )


    # Add custom related_name for groups and user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='user_profiles'  # Specify your custom related_name here
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='user_profiles_permissions'  # Specify your custom related_name here
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    def __str__(self):
        return self.username

    
class BulletPoint(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    

    def __str__(self):
        return self.name
    
class Experience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    summary_statement = models.TextField(blank=True, null=True)    
    description_1 = models.TextField(
        blank=True, null=True,
        validators=[MaxLengthValidator(limit_value=500)]  # Set your desired character limit
    )
    description_1 = models.TextField(
        blank=True, null=True,
        validators=[MaxLengthValidator(limit_value=500)]  # Set your desired character limit
    )
    description_2 = models.TextField(
        blank=True, null=True,
        validators=[MaxLengthValidator(limit_value=500)]  # Set your desired character limit
    )
    description_3 = models.TextField(
        blank=True, null=True,
        validators=[MaxLengthValidator(limit_value=500)]  # Set your desired character limit
    )
    description_4 = models.TextField(
        blank=True, null=True,
        validators=[MaxLengthValidator(limit_value=500)]  # Set your desired character limit
    )
    description_5 = models.TextField(
        blank=True, null=True,
        validators=[MaxLengthValidator(limit_value=500)]  # Set your desired character limit
    )
            

    def __str__(self):
        return f"{self.company_name} - {self.job_title}: : {self.summary_statement}"

class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    degree = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.school} - {self.major}"
    
class Accomplishments(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    accomplishments = models.CharField(max_length=255)
    accomplishment_image = models.ImageField(upload_to='certs/', blank=True, null=True)
