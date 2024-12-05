from django.shortcuts import render,get_object_or_404, redirect
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from.models import profile
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm, AdminProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url  = reverse_lazy("login")
    template_name = 'registration/signup.html'

@login_required
def profileView(request, userid):
# def profileView(request):

    userid = request.user.id
    Profile = profile.objects.get(user_id = userid)
    print(Profile)

    return render(request, template_name='userApp/profile.html', context={'profile':Profile})

@login_required
def editProfileView(request, userid):
    userObject = get_object_or_404(User, id = userid)
    profileObject = get_object_or_404(profile, user_id = userid)

    if request.method == 'POST':
        generalForm = UserForm(request.POST, instance=userObject)
        profileForm_user = UserProfileForm(request.POST, request.FILES,  instance=profileObject)
        profileForm_admin = AdminProfileForm(request.POST, request.FILES,  instance=profileObject)

        if request.user.is_superuser:
            if generalForm.is_valid() and profileForm_admin.is_valid():

                if profileForm_admin.cleaned_data['role'].lower() == 'staff':
                    userObject.is_staff = True
                    userObject.is_superuser = False
                elif profileForm_admin.cleaned_data['role'].lower() == 'admin':
                    userObject.is_staff = True
                    userObject.is_superuser = True
                else:
                    userObject.is_staff = False
                    userObject.is_superuser = False
                generalForm.save()
                profileForm_admin.save()

                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile', userid)
            else:
                return render(request, template_name='userApp/edit_profile.html', context={'generalForm':generalForm, 'profileForm': profileForm_admin})
        else:
            if generalForm.is_valid() and profileForm_user.is_valid():
                generalForm.save()
                profileForm_user.save()

                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile', userid)
            else:
                return render(request, template_name='userApp/edit_profile.html', context={'generalForm':generalForm, 'profileForm':profileForm_user})



    else:
        generalForm = UserForm(instance=userObject)
        profileForm_user = UserProfileForm(instance=profileObject)
        profileForm_admin = AdminProfileForm(instance=profileObject)

        if request.user.is_superuser:
            return render(request, template_name='userApp/edit_profile.html', context={'generalForm':generalForm, 'profileForm': profileForm_admin})
        else:
            return render(request, template_name='userApp/edit_profile.html', context={'generalForm':generalForm, 'profileForm':profileForm_user}) 
@login_required
def allUserView(request): 
    alluser = profile.objects.all()
    return render(request, template_name= 'userApp/alluser.html', context={'alluser': alluser})

@login_required
def deactivateUserView(request, userid):
    user = User.objects.get(id = userid)
    if user.is_active:

        user.objects.filter(id =userid).update(is_active = False)
        messages.success(request, 'Deactivation succesfull')
    else:
        user.objects.filter(id = userid).update(is_activate = True)
        messages.success(request, 'Activation succesfull')
    return redirect('alluser')















    # Profile = profile.objects.all()
    [
        (),
        ()
    ]
    Profile = profile.objects.filter()
    [
        ()
    ]




