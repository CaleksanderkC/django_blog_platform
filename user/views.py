from django.core.checks import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from theme.models import Post, Comment
from user.forms import (
    UserLogIn,
    UserCreat,
    UserForm,
    ProfileForm
)


@login_required(login_url='user:log_in')
def index(request):
    user = request.user
    users_post = Post.objects.filter(author=user)
    users_comment = Comment.objects.filter(author=user)
    context = {
        'users_post': users_post,
        'users_comment': users_comment
    }
    return render(request, 'user/index.html', context)


def sing_up(request):
    user_form = UserCreat(request.POST or None)
    if request.method == 'POST' and user_form.is_valid():
        user_form.save()
        username = user_form.cleaned_data.get('username')
        raw_password = user_form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)

        return redirect(reverse('theme:index'))
    context = {
        'form': user_form
    }
    return render(request, 'user/sing_up.html', context)


def log_in(request):
    form = UserLogIn()
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('theme:index'))
        else:
            messages.error(request, 'invalid login or password')
            return render(request, 'user/log_in.html', {'form': form})
            
    content = {
        'form': form
    }
    return render(request, 'user/log_in.html', content)


def log_out(request):
    logout(request)
    return redirect(reverse('theme:index'))


@login_required(login_url='user:log_in')
def update_profile(request):
    user = request.user
    if request.method == 'POST':

        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            return redirect('user:profile')
        else:
            return redirect('theme:index')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/change_profile.html', context)
