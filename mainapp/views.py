from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate , login as auth_login , logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import uuid
from .models import *
from .utils import *


@login_required
def home(request):
    product = Product.objects.all()
    return render(request, 'index.html',{'product':product})

def write_review(request, id):
    message = ''
    user = Product.objects.get(id=id)
    product = get_object_or_404(Product, pk=id)
    reviews = product.reviews.all().order_by('-rating')

    user_has_reviewed = ProductReview.objects.filter(product=product, user=request.user).exists()

    if user_has_reviewed:
        message = "You already Give you Review you can't do again"
    else:
        if request.method == "POST":
            comment = request.POST.get("comment")
            rating = request.POST.get("rating") 

            review = ProductReview.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
    return render(request, 'review.html', {'user': user,'reviews':reviews,"message":message})

def login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate (request, username = username , password = password)
        if user is not None:
            auth_login(request,user)
            return redirect('/')
        else :
            message = "Invalid username or password. Please try again."

    return render(request, 'login.html', {'messege':message})

def logout(request):
    auth_logout(request)
    return redirect("/login/")

def sign_up(request):
    messege = ''
    if request.method == "POST":
        username = request.POST['username']
        first_name=request.POST["first-name"]
        last_name=request.POST["last-name"]
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re-password']

        if password == re_password:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username,password=re_password,first_name=first_name,last_name=last_name,email=email)
                email_token = str(uuid.uuid4())
                print(email_token,"Deepak")
                profile = Profile.objects.create(user = user , email_token = email_token)
                send_email_token(email , profile.email_token)
                messege = "Account Create Successful"
            else:
                messege = "Username already exists."
        else:
            messege = "Passwords do not match."
    return render(request, 'signup.html' ,{'messege':messege})

def verify(request,token):
    print(f"Received token: {token}")
    try:
        profile = Profile.objects.get(email_token= token )
        profile.is_verify = True
        profile.save()
        return HttpResponse("Your account Verified")
    except Exception as e:
        return HttpResponse("Invalid Token")