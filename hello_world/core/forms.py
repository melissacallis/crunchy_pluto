from django import forms
import logging
from .models import UserProfile, BulletPoint, Experience, Education, Accomplishments  # Import UserProfile from the correct module
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.forms import formset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class CreateUserForm(UserCreationForm):
    # Add fields from UserProfile
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = UserCreationForm.Meta.fields + (
            'username', 'password1', 'password2', 'first_name', 'last_name', 'city', 'state', 'zip_code', 'phone_number',
            'email', 'profile_image', 'resume', 'linkedin_link', 'github_link', 'project_link'
        )

class CustomAuthForm(AuthenticationForm):
    class Meta:
        model = User  # Set the model to your UserProfile model
        fields = ['username', 'password']
         

        
class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'first_name', 'last_name', 'city', 'state', 'zip_code', 'phone_number', 'email', 'profile_image', 'resume', 'linkedin_link', 'github_link', 'project_link']
        
        widgets = {
            'password': forms.PasswordInput(),
        }
        
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['username', 'password', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_login']



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
        
class AccomplishmentsForm(forms.ModelForm):
    class Meta:
        model = Accomplishments
        fields = ['accomplishments', 'accomplishment_image']
        
class CustomLoginView(LoginView):
    template_name = 'core/login_user.html'
    authentication_form = AuthenticationForm  # Use the built-in form
