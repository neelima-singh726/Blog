from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views import View
from users.forms import LoginForm, RegisterForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)
class SignInView(View):
    """View for user sign in/login

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders login form in case of invalid login 
        Redirects to home page for valid login.
    """
    def get(self, request):
        try:
            if request.user.is_authenticated:
                return redirect('home')
            form = LoginForm()
            return render(request, 'login.html', {'form': form})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e) 
            return redirect('login')

    def post(self, request):
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Hi {username.title()}, welcome back!')
                    return redirect('home')

            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html', {'form': form})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)            
            return redirect('login')

class SignOutView(View):
    """View for user sign out.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Redirection to the login page after logging out.
    """
    @method_decorator(login_required)
    def get(self, request):
        try:
            logout(request)
            messages.success(request, 'You have been logged out.')
            return redirect('login')
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)
            return redirect('login')

class SignUpView(View):
    """View for user sign up.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered registration form or a redirection to the home page after successful registration.
    """
    def get(self, request):
        try:
            form = RegisterForm()
            return render(request, 'register.html', {'form': form})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)          
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('register')

    def post(self, request):
        try:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, 'You have signed up successfully.')
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'register.html', {'form': form})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            error_message = str(e)
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('register')
