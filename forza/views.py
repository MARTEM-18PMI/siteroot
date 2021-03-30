from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .forms import LoginForm, RegistrationForm
from .models import Blog, Post


def get_main(request):
    return render(request, 'forza/index.html', {})


def get_inner(request):
    return render(request, 'forza/inner-content.html', {})


def get_tunings_list(request):
    blogs = Blog.objects.annotate(post_count=Count('post')).order_by('-post_count')
    # blogs = Blog.objects.order_by('title')
    context = {
        'blogs': blogs,
    }
    return render(request, 'forza/tunings.html', context)


@login_required(login_url='/forza/login')
def blog(request, blog_id):
    if request.method == 'POST':
        return create_post(request, blog_id)
    else:
        return render_blog(request, blog_id)


def log_out(request):
    logout(request)
    redirect_url = request.GET.get('next') or reverse('index')
    return redirect(redirect_url)


def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    return redirect(request.GET['next'])
                except:
                    return render(request, 'forza/login.html', {'form': form})

            else:
                form.add_error('Invalid credentials!')
    else:
        form = LoginForm()
    return render(request, 'forza/login.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logout(request)
            blog_title = form.cleaned_data['blog_title']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'User already exists!')
            elif password != password_again:
                form.add_error('password_again', 'Passwords mismatch!')
            else:
                user = User.objects.create_user(username, email, password)
                blog = Blog.objects.create(author=user, title=blog_title)
                login(request, user)
                context = {'blog': blog, 'posts': []}
                return render(request, 'forza/index.html', context)
    else:
        form = RegistrationForm()
    return render(request, 'forza/signup.html', {'form': form})


def render_blog(request, blog_id, additional_context={}):
    blog = get_object_or_404(Blog, id=blog_id)

    context = {
        'blog': blog,
        'posts': blog.post_set.order_by('-created_at'),
        **additional_context
    }
    return render(request, 'forza/tuningblog.html', context)


def create_post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    subject = request.POST['subject']
    subject_error = None
    if not subject or subject.isspace():
        subject_error = 'Please provide non-empty subject!'

    text = request.POST['text']
    text_error = None
    if not text or text.isspace():
        text_error = 'Please provide non-empty text!'

    if subject_error or text_error:
        error_context = {
            'subject_error': subject_error,
            'text_error': text_error,
            'subject': subject,
            'text': text,
        }
        return render_blog(request, blog_id, error_context)
    else:
        Post(blog_id=blog.id, subject=subject, text=text).save()
        return HttpResponseRedirect(reverse('blog_by_id', kwargs={'blog_id': blog_id}))
