from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        # Register User
        # Get form values (with POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, "That username is taken")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "That email address is being used")
                    return redirect('register')
                else:
                    # Looks Good
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        password=password,
                        email=email,
                    )
                    # LOgin after register
                    # auth.login(request,user)
                    # messages.success(request, "You are now logged in")
                    # return redirect('index')

                    # or inform for successful registration and redirect to login page
                    user.save()
                    messages.success(request, "You are now registered")
                    return redirect('login')

        else:
            messages.error(request, 'Password mismatch')
            return redirect('register')

    else:
        return render(request,'accounts/register.html')






def login(request):
    if request.method == 'POST':
        # Login User
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, "You are now logged in!")
            return redirect('dashboard')
        else:
            messages.error(request,"Username or password is incorrect")
            return redirect('login')

    else:
        return render(request,'accounts/login.html')





def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are now logged out")

        return redirect('index')







def dashboard(request):
    return render(request,'accounts/dashboard.html')
