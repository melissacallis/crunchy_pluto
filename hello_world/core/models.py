from django.db import models
from PIL import Image
from django.core.validators import MaxLengthValidator, FileExtensionValidator

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




class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
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
    
    class Meta:
        app_label = 'core'

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
