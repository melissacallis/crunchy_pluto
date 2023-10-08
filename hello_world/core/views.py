from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
from .forms import UserForm, BulletPointForm, ExperienceForm, EducationForm, AccomplishmentsForm, EditProfileForm, CreateUserForm
from .models import BulletPoint, UserProfile, Experience, Education, Accomplishments

from django.conf import settings
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages  
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, CustomAuthForm



def index(request):
    # Your view logic here
    return render(request, 'core/index.html')

def frontpage(request):
    return render (request, 'core/frontpage.html')



def user_form(request, username=None):
    user = None  # Set user to None if this is a new user registration

    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)

        if form.is_valid():
            # Extract password fields from form cleaned data
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            # Check if passwords match
            if password1 != password2:
                messages.error(request, 'Passwords do not match')
                return redirect('user_form')

            # Form data is valid, create or update the UserProfile
            user_profile, created = UserProfile.objects.get_or_create(username=username)
            user_profile.first_name = form.cleaned_data['first_name']
            user_profile.last_name = form.cleaned_data['last_name']
            user_profile.city = form.cleaned_data['city']
            user_profile.state = form.cleaned_data['state']
            user_profile.zip_code = form.cleaned_data['zip_code']
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.email = form.cleaned_data['email']
            user_profile.profile_image = form.cleaned_data['profile_image']
            user_profile.resume = form.cleaned_data['resume']
            user_profile.linkedin_link = form.cleaned_data['linkedin_link']
            user_profile.github_link = form.cleaned_data['github_link']
            user_profile.project_link = form.cleaned_data['project_link']
            user_profile.set_password(password1)  # Set the user's password
            user_profile.save()

            # Authenticate and log in the user
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful')

                # Redirect to success_demo with the 'username' parameter
                return redirect('success_demo', username=username)
            else:
                messages.error(request, 'Authentication failed')
    else:
        # If it's not a POST request, initialize the form
        form = CreateUserForm(instance=user)  # Pass user if editing an existing user

    return render(request, 'registration/user_form.html', {'form': form, 'user': user})





    

def profile_view(request):
    # Redirect to the success_demo view
    return redirect('success_demo', username=request.user.username)



def login_user(request):
    if request.method == 'POST':
        form = CustomAuthForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                print(f"User {username} logged in successfully.")
                return redirect('success_demo', username=username)
        return render(request, 'core/login_user.html', {'form': form})
    else:
        form = CustomAuthForm()
        return render(request, 'core/login_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')  # Redirect to your desired page after logout



# Define the get_user_data function with a username parameter
def get_user_data(username):
    try:
        user = UserProfile.objects.get(username=username)  # Retrieve the user based on the provided username
        bullet_points = BulletPoint.objects.filter(user_profile=user)  # Query the bullet points for the user
        user.bullet_points = bullet_points
        return user
    except UserProfile.DoesNotExist:
        # Handle the case where the provided username doesn't exist
        # You can return an error message or raise an exception as needed
        return None
    
def edit_profile(request, username):
    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        # Handle the case where the user profile doesn't exist
        return HttpResponse("User profile not found", status=404)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            # Update the user profile fields excluding username and password
            form.save()
            return redirect('success_demo', username=username)
    else:
        form = EditProfileForm(instance=user_profile)

    return render(request, 'core/edit_profile.html', {'form': form, 'user': user_profile})


def add_skills(request, username):
    if request.method == 'POST':
        form = BulletPointForm(request.POST)
        if form.is_valid():
            try:
                # Get the user's profile
                user_profile = UserProfile.objects.get(username=username)
                
                # Create a new bullet point with the skill and associate it with the user's profile
                skill_name = form.cleaned_data['name']  # Use the correct field name 'name'
                bullet_point = BulletPoint(user_profile=user_profile, name=skill_name)
                bullet_point.save()
                
                # Redirect back to the user's profile page or wherever you want
                return redirect('success_demo', username=username)
            except UserProfile.DoesNotExist:
                # Handle the case when the user profile doesn't exist
                # You can redirect the user to an error page or take appropriate action
                return HttpResponse("User profile not found.")
    else:
        form = BulletPointForm()

    return render(request, 'core/add_skills.html', {'form': form})


def edit_user_profile(request, username=None):
    user = get_user_data()  # Replace with your logic to get user data

    user_form = UserForm(instance=user)
    bullet_point_form = BulletPointForm(initial={'bullet_points': '\n'.join(get_bullet_points())})

    if request.method == 'POST':
        if 'user_info' in request.POST:
            user_form = UserForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                return redirect('edit_user_profile', username=username)
        elif 'skills' in request.POST:
            bullet_point_form = BulletPointForm(request.POST)
            if bullet_point_form.is_valid():
                bullet_points = bullet_point_form.cleaned_data['bullet_points']
                # Process and save bullet points as needed
                # ...
                return redirect('core:edit_user_profile', username=username)

    return render(request, 'core/edit_user_profile.html', {'user_form': user_form, 'bullet_point_form': bullet_point_form, 'user': user})



def success_skills(request, username=None):
    # Get the user data based on the provided username
    user = get_user_data(username)

    if user:
        # Assuming you have a related name for the BulletPoint ForeignKey field in the UserProfile model
        skills = user.bulletpoint_set.all()
    else:
        skills = []  # User not found or other error handling

    if request.method == 'POST':
        if 'initial_submit' in request.POST:
            # Handle initial skill input
            bullet_point_form = BulletPointForm(request.POST)
            if bullet_point_form.is_valid():
                # Process and save initial bullet points as needed
                name = bullet_point_form.cleaned_data['name']
                description = bullet_point_form.cleaned_data['description']
                # Create a BulletPoint instance for the initial skill input
                BulletPoint.objects.create(user_profile=user, name=name, description=description)
        elif 'revision_submit' in request.POST:
            # Handle skill revision
            bullet_point_revision_form = BulletPointForm(request.POST)
            if bullet_point_revision_form.is_valid():
                bullet_points = bullet_point_revision_form.cleaned_data['bullet_points']
                bullet_point_lines = bullet_points.split('\n')

                # Process and save revised bullet points as needed
                for i, line in enumerate(bullet_point_lines):
                    bullet_point_field_name = f'bullet_point_{i + 1}'
                    bullet_point_value = bullet_point_revision_form.cleaned_data.get(bullet_point_field_name)
                    # Save or process each revised bullet point here

    # Create instances of BulletPointForm for both initial skill input and revision
    bullet_point_form = BulletPointForm()
    bullet_point_revision_form = BulletPointForm()

    return render(request, 'core/success_skills.html', {
        'user': user,
        'username': username,
        'skills': skills,
        'first_name': user.first_name,
        'bullet_point_form': bullet_point_form,
        'bullet_point_revision_form': bullet_point_revision_form,
    })


def edit_skills(request, username=None, skill_id=None):
    # Get the user data based on the provided username
    user = get_object_or_404(UserProfile, username=username)

    # Get the skill to be edited
    skill = get_object_or_404(BulletPoint, id=skill_id, user_profile=user)

    if request.method == 'POST':
        # Process and save edited skill as needed
        form = BulletPointForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()

            # Redirect back to 'success_demo' with the 'username' parameter
            return redirect('success_demo', username=username)
    else:
        # Initialize the form with the selected skill for editing
        form = BulletPointForm(instance=skill)

    # Debugging statement to check the skill instance
    print(f"Skill instance: {skill}")
    print(f"After initializing the form, Skill name: {form.instance.name}")

    # Pass the user and form objects to the template
    context = {'user': user, 'form': form}

    # Render the 'core/edit_skills.html' template
    return render(request, 'core/edit_skills.html', context)




def delete_skill(request, username, skill_id):
    user = get_object_or_404(UserProfile, username=username)
    skill = get_object_or_404(BulletPoint, id=skill_id, user_profile=user)
    
    if request.method == 'POST':
        skill.delete()
    
    # Redirect back to 'success_demo' with the 'username' parameter
    return redirect('success_demo', username=username)




def success_demo(request, username=None):
    # Get the user data based on the provided username
    
    user = get_object_or_404(UserProfile, username=username)

    # Retrieve the user's skills
    skills = BulletPoint.objects.filter(user_profile=user)
    experiences = Experience.objects.filter(user_profile=user)
    education = Education.objects.filter(user_profile=user)
    accomplishments = Accomplishments.objects.filter(user=user)
        # Add this line to fetch experiences
        # Create a list of descriptions for each experience
    descriptions_list = []
    for experience in experiences:
        descriptions = []
        for i in range(1, 6):  # Assuming you have up to 5 job descriptions
            field_name = f'job_description_{i}'
            description = getattr(experience, field_name, None)
            if description:
                descriptions.append(description)
        descriptions_list.append(descriptions)

    # Handle skill removal if POST request
    if request.method == 'POST':
        skill_id_to_remove = request.POST.get('remove_skill_id')
        if skill_id_to_remove:
            # Delete the skill with the specified ID
            BulletPoint.objects.filter(id=skill_id_to_remove).delete()
            # Redirect back to the success_demo page
            return redirect('success_demo', username=username)

    return render(request, 'core/success_demo.html', {'user': user, 'username': username, 'skills': skills, 'experiences': experiences, 'education': education, 'accomplishments':accomplishments})


def view_user_profile(request, username):
    user = UserProfile.objects.get(username=username)
    return render(request, 'core/user_profile.html', {'user': user})

def add_experience(request, username):
    user = get_object_or_404(UserProfile, username=username)

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user_profile = user
            experience.save()
            return redirect('success_demo', username=username)
    else:
        form = ExperienceForm()

    return render(request, 'core/add_experience.html', {'user': user, 'form': form})

def edit_experience(request, username, experience_id):
    user = get_object_or_404(UserProfile, username=username)
    experience = get_object_or_404(Experience, id=experience_id, user_profile=user)

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('success_demo', username=username)
    else:
        form = ExperienceForm(instance=experience)

    return render(request, 'core/edit_experience.html', {'user': user, 'form': form})


def delete_experience(request, username, experience_id):
    # Get the user data based on the provided username
    user = get_object_or_404(UserProfile, username=username)

    # Get the experience instance to delete
    experience = get_object_or_404(Experience, id=experience_id, user_profile=user)

    if request.method == 'POST':
        experience.delete()

    # Redirect back to 'success_demo' with the 'username' parameter
    return redirect('success_demo', username=username)


def add_education(request, username):
    user = get_object_or_404(UserProfile, username=username)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            # Create an Education instance but don't save it to the database yet
            education = form.save(commit=False)            
            # Associate the education with the user profile
            education.user_profile = user
            # Save the education instance to the database
            education.save()
            return redirect('success_demo', username=username)
    else:
        form = EducationForm()
    return render(request, 'core/add_education.html', {'user': user, 'form': form})


def edit_education(request, username, education_id):
    user = get_object_or_404(UserProfile, username=username)
    education = get_object_or_404(Education, id=education_id, user_profile=user)

    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('success_demo', username=username)
    else:
        form = EducationForm(instance=education)

    return render(request, 'core/edit_education.html', {'user': user, 'form': form})

def delete_education(request, username, education_id):
    user = get_object_or_404(UserProfile, username=username)
    education = get_object_or_404(Education, id=education_id, user_profile=user)

    if request.method == 'POST':
        education.delete()

    return redirect('success_demo', username=username)

def add_certification(request, username):
    user_profile = UserProfile.objects.get(username=username)
    
    if request.method == 'POST':
        form = AccomplishmentsForm(request.POST, request.FILES)
        if form.is_valid():
            accomplishment = form.save(commit=False)  # Save the form data without committing to the database
            accomplishment.user = user_profile  # Set the user for the accomplishment
            accomplishment.save()  # Save the accomplishment to the database
            return redirect('success_demo', username=username)  # Redirect to the user's profile page
    else:
        form = AccomplishmentsForm()
    
    return render(request, 'core/add_certification.html', {'form': form})


def edit_certification(request, username, accomplishments_id):
    user_profile = get_object_or_404(UserProfile, username=username)
    certification = get_object_or_404(Accomplishments, id=accomplishments_id, user=user_profile)

    if request.method == 'POST':
        form = AccomplishmentsForm(request.POST, request.FILES, instance=certification)
        if form.is_valid():
            form.save()
            return redirect('success_demo', username=username)
    else:
        form = AccomplishmentsForm(instance=certification)

    return render(request, 'core/edit_certification.html', {
        'form': form,
        'username': username,
        'certification_id': accomplishments_id,
        'certification': certification if request.method != 'POST' else form.cleaned_data.get('accomplishments')
    })





    
    


