# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Ahmed Salim
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.models import User
from apps.authentication.models import Profile, Message
from .forms import DweetForm, ProfileImageForm, MessageForm
from django.shortcuts import redirect
from apps.authentication.models import Dweet
from django.shortcuts import render, get_object_or_404


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        if load_template == '':
            load_template = 'dashboard.html'
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    

@login_required
def profile_view(request, username=None):
    profiles = Profile.objects.all()

    if username:
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        is_following = request.user.profile.follows.filter(id=profile.id).exists()

        if request.method == "POST":
            if 'follow' in request.POST:
                action = request.POST.get("follow")
                if action == "follow":
                    request.user.profile.follows.add(profile)
                elif action == "unfollow":
                    request.user.profile.follows.remove(profile)
                request.user.profile.save()
                return redirect('profile', username=username)
            elif 'upload_image' in request.POST:
                image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
                if image_form.is_valid():
                    image_form.save()
                    return redirect('profile', username=username)
            form = DweetForm(request.POST)
            if form.is_valid():
                dweet = form.save(commit=False)
                dweet.user = request.user
                dweet.save()
                return redirect('profile', username=username)
        else:
            form = DweetForm()
            image_form = ProfileImageForm(instance=request.user.profile)

        if user == request.user:
            dweets = Dweet.objects.all().order_by("-created_at")
        else:
            dweets = Dweet.objects.filter(user=user).order_by("-created_at")
        context = {
            'profile': profile,
            'is_following': is_following,
            'form': form,
            'dweets': dweets,
            'profiles': profiles,
            'image_form': image_form,
        }
    else:
        context = {
            'profiles': profiles
        }
    return render(request, "home/profile.html", context)


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'home/send_message.html', {'form': form})

@login_required
def send_message_user(request, username):
    receiver = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
        form.fields['receiver'].initial = receiver
    return render(request, 'home/send_message.html', {'form': form})

@login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'home/inbox.html', {'messages_received': messages_received})

@login_required
def message_detail(request, message_id):
    message = Message.objects.get(id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return render(request, 'home/message_detail.html', {'message': message})

