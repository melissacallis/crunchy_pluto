from django.db import models



class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    
    
    class Meta:
        app_label = 'core'

    def __str__(self):
        return self.username
    
class BulletPoint(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    

    def __str__(self):
        return self.name
    
class Experience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    summary_statement = models.TextField(blank=True, null=True)    
    description_1 = models.TextField(blank=True, null=True) 
    description_2 = models.TextField(blank=True, null=True)
    description_3 = models.TextField(blank=True, null=True)
    description_4 = models.TextField(blank=True, null=True)
    description_5 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"

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
