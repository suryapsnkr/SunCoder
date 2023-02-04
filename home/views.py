from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from datetime import datetime
from django.core.mail import send_mail, EmailMultiAlternatives
# Create your views here.
def home(request):
    #messages.success(request, 'Welcome to SunCoder Homepage.')
    return render(request, 'home/home.html')

def about(request, time=datetime.now().strftime('%B')):
    #messages.success(request, 'welcome to SunCoder about.')
    now = datetime.now()
    # get current time
    time = now.strftime('%I:%M %p')
    return render(request, 'home/about.html',{'time': time})

def contact(request):
    #messages.success(request, "Welcome to SunCoder Contact.")
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        # check for error
        contact=Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
        messages.success(request, "Your message has been successfully sent")
        # send_mail
        send_mail(
        'SunCoder',
        'Thanks for contact us.',
        'suryapsnkr@gmail.com',
        [email],
        fail_silently=False,
    )
        # EmailMultiAlternatives
        subject='Testing Mail'
        form_email='suryapsnkr@gmail.com'
        msg='<p><b>Welcome {name},</i>Thanks for contact to us.</i>'
        to=email
        msg=EmailMultiAlternatives(subject,msg,form_email,[to])
        msg.content_subtype='html'
        msg.send()
    return render(request, 'home/contact.html')
    
def search(request):
    query=request.GET['query']
    allPosts= Post.objects.filter(title__icontains=query)
    context={'allPosts': allPosts}
    return render(request, 'home/search.html', context)

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your SunCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")

# for change password of user
def ChangePswd(request):
    if request.method == 'POST':
        oldpswd = request.POST['oldpswd']
        newpswd = request.POST['newpswd']

        user = User.objects.get(id = request.user.id)
        check = user.check_password(oldpswd)
        if check == True:
            user.set_password(newpswd)
            user.save()
            messages.success(request, 'Change password successfully.')
        else:
            messages.error(request, 'Invalid current password.')
            return render(request, 'pswd.html')
    return render(request, 'home/cpswd.html')