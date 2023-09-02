import logging
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from blog.forms import PostForm
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from demo_project.settings import EMAIL, PSWD

logger = logging.getLogger(__name__)
class HomeView(View):
    """View for the home page.

    Args:
        View (class): The base View class.

    Returns:
        HttpResponse: Renders home page with the list of posts.
    """
    def get(self, request):
        try:
            posts = Post.objects.all()
            context = {
                'posts': posts,
                'title': 'Zen of Python'
            }
            return render(request, 'home.html', context)
        except Exception as e:
            # Log the exception details
            logger.error(f"An error occurred: {str(e)}")

            # Handle the exception here, you can customize the response
            error_message = str(e)  # Convert the exception to a string
            return HttpResponse(f"An error occurred: {error_message}", status=500)

class AboutView(View):
    """View for the about page."""
    def get(self, request):
        try:
            return render(request, 'about.html')
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)  # Convert the exception to a string
            return HttpResponse(f"An error occurred: {error_message}", status=500)

@method_decorator(login_required, name='dispatch')
class CreatePostView(View):
    """View for creating a new post.

    Args:
        View (class): The base View class.

    Returns:
        HttpResponse: Renders a form for creating a new post or a redirection to the home page after successful creation.
    """
    def get(self, request):
        try:
            context = {'form': PostForm()}
            return render(request, 'post_form.html', context)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)  # Convert the exception to a string
            return HttpResponse(f"An error occurred: {error_message}", status=500)

    def post(self, request):
        try:
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                email_sender_view = SendEmailView()
                response = email_sender_view.send_email(request.user.email)

                messages.success(request, 'The post has been created successfully.')

                return redirect('home')
            else:
                messages.error(request, 'Please correct the following errors:')
                return render(request, 'post_form.html', {'form': form})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)  # Convert the exception to a string
            return HttpResponse(f"An error occurred: {error_message}", status=500)


@method_decorator(login_required, name='dispatch')
class EditPostView(View):
    """View for editing a post.

    Args:
        View (class): The base View class.

    Returns:
        HttpResponse: Renders a form for editing a post or a redirection to the home page after successful editing.
    """
    def get(self, request, id):
        try:
            queryset = Post.objects.filter(author=request.user)
            post = get_object_or_404(queryset, pk=id)
            context = {'form': PostForm(instance=post), 'id': id}
            return render(request, 'post_form.html', context)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)  # Convert the exception to a string
            return render(request, '404page.html')


    def post(self, request, id):
        try:
            queryset = Post.objects.filter(author=request.user)
            post = get_object_or_404(queryset, pk=id)
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'The post has been updated successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the following errors:')
                return render(request, 'post_form.html', {'form': form})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)  # Convert the exception to a string
            return render(request, '404page.html')

@method_decorator(login_required, name='dispatch')
class DeletePostView(View):
    """View for deleting a post.

    Args:
        View (class): The base View class.

    Returns:
        HttpResponse: Rendeers a confirmation page for post deletion or a redirection to the home page after successful deletion.
    """
    def get(self, request, id):
        try:
            queryset = Post.objects.filter(author=request.user)
            post = get_object_or_404(queryset, pk=id)
            context = {'post': post}
            return render(request, 'post_confirm_delete.html', context)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)  # Convert the exception to a string
            return render(request, '404page.html')

    def post(self, request, id):
        try:
            queryset = Post.objects.filter(author=request.user)
            post = get_object_or_404(queryset, pk=id)
            post.delete()
            messages.success(request, 'The post has been deleted successfully.')
            return redirect('home')
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)  # Convert the exception to a string
            return render(request, '404page.html')
        
from django.http import HttpResponse, JsonResponse
import smtplib

import json
import smtplib
from django.http import JsonResponse
from email.mime.text import MIMEText
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from base64 import urlsafe_b64decode, urlsafe_b64encode


class SendEmailView(View):
    def send_email(self, email):
        try:
            subject = "Post Created"
            body = "Post created successfully"
            sender = EMAIL
            recipients = [email]
            password = PSWD

            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipients, msg.as_string())

            return {'success': True}
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)
            return {'success': False, 'error': str(e)}




