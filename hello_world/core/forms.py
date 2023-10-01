from django import forms
from .models import UserProfile, BulletPoint  # Import UserProfile from the correct module
from django.forms import formset_factory
from .models import Experience, Education 

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'city', 'state', 'zip_code', 'phone_number', 'email',
                  'profile_image', 'resume', 'linkedin_link', 'github_link', 'project_link']

class BulletPointForm(forms.ModelForm):
    class Meta:
        model = BulletPoint
        fields = ['name']

BulletPointFormSet = formset_factory(BulletPointForm, extra=1)  # Set 'extra' as needed

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'summary_statement',
                  'description_1', 'description_2', 'description_3', 'description_4', 'description_5']
        

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'major', 'degree', 'gpa', 'start_date', 'end_date']
        
class ProfileImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['resume']
