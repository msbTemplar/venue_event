from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from . forms import RegisterUserForm

# Create your views here.


def login_user(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, "Error during login prueba oitra vez")
            return redirect('login')
    else:
        context = {}
        return render(request, 'authenticate/login.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, "you were logged out")
    return redirect('home')

def register_user(request):
    
    if request.method == "POST":
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            
            user = authenticate(username=username, password=password)
            
            login(request,user)
            
            messages.success(request, "registracion successfull")
            return redirect('home')
    else:
         form=RegisterUserForm()
    
    
    context={'form':form}
    return render(request, 'authenticate/register_user.html', context)