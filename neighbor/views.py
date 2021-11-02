from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api


@login_required(login_url='/accounts/login/')
def home(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    if profile is None:
        profile = Profile.objects.filter(
            user_id=current_user.id).first()  # get profile
        posts = Post.objects.filter(user_id=current_user.id)
        locations = Location.objects.all()
        neighborhood = Neighborhood.objects.all()
        business = Business.objects.filter(user_id=current_user.id)
        return render(request, "profile.html", {"danger": "please update your Profile ", "locations": locations, "neighborhood": neighborhood, "business": business, "posts": posts})
    else:
        neighborhood = profile.neighborhood
        posts = Post.objects.filter(neighbourhood=neighborhood).order_by("-created_at")
        return render(request, 'index.html', {'posts': posts,"profile":profile})


@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    userid =current_user.id
    profile = Profile.objects.filter(user_id = current_user.id).first()
    posts = Post.objects.filter(user_id=current_user.id)
    locations = Location.objects.all()
    neighborhood = Neighborhood.objects.all()
    business = Business.objects.filter(user_id=userid)
    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'locations': locations, 'neighborhood': neighborhood, 'business': business})

@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':

        current_user = request.user

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        name = request.POST["first_name"] + " " + request.POST["last_name"]

        neighborhood = request.POST["neighborhood"]
        location = request.POST["location"]
        bio = request.POST['bio']

        profile_image = request.FILES['profile_pic']
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image['url']

        user = User.objects.get(id=current_user.id)

    # check for an instance
        if location == "":
            location = None
        else:
            location = Location.objects.get(name=location)

        if neighborhood == "":
            neighborhood = None
        else:
            neighborhood = Neighborhood.objects.get(name=neighborhood)

    #end check for an instance


        if Profile.objects.filter(user_id=current_user.id).exists():

            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_photo = profile_url
            profile.bio = bio
            profile.neighborhood = neighborhood
            profile.location = location
            profile.save()
        else:
            profile = Profile(user_id=current_user.id,name=name,neighborhood=neighborhood,location=location,
                              profile_photo=profile_url, bio=bio)
            profile.save_profile()

        user.first_name = first_name
        user.username = username
        user.last_name = last_name
        user.email = email

        user.save()

        return redirect('/profile', {'success': 'Updated your profile Successfully'})
    else:
        return render(request, 'profile.html', {'failed': 'Update Failed'})  


@login_required(login_url="/accounts/login/")
def add_business(request):
    if request.method == "POST":
        current_user = request.user
        name = request.POST["bs_name"]
        email = request.POST["bs_email"]
        description = request.POST["bs_desc"]
        profile = Profile.objects.filter(user_id=current_user.id).first()

        if profile is None:
            profile = Profile.objects.filter(
                user_id=current_user.id).first()  # get profile
            posts = Post.objects.filter(user_id=current_user.id)
            locations = Location.objects.all()
            neighborhood = Neighborhood.objects.all()
            business = Business.objects.filter(user_id=current_user.id)
            return render(request, "profile.html", { "locations": locations, "neighborhood": neighborhood,"business": business,"posts": posts})
        else:
            neighborhood = profile.neighborhood

        if neighborhood == "":
            neighborhood = None
        else:
            neighborhood = Neighborhood.objects.get(name=neighborhood)

        business = Business(
            user_id=current_user.id,
            name=name,
            email=email,
            description=description,
            neighbourhood=neighborhood,
        )
        business.create_business()

        return redirect("/profile", {"success": "Business Created Successfully"})
    else:
        return render(request, "profile.html", {"danger": "Business Failed"})


@login_required(login_url="/accounts/login/")
def add_post(request):
    if request.method == "POST":
        current_user = request.user
        title = request.POST["title"]
        content = request.POST["content"]
        category = request.POST["category"]
        location = request.POST["location"]

        profile = Profile.objects.filter(user_id=current_user.id).first()
        if profile is None:
            profile = Profile.objects.filter(user_id=current_user.id).first()
            posts = Post.objects.filter(user_id=current_user.id)
            locations = Location.objects.all()
            neighborhood = Neighborhood.objects.all()
            businesses = Business.objects.filter(user_id=current_user.id)
            return render(request, "profile.html", {"error":"please update your profile to post","locations": locations, "neighborhood": neighborhood, "categories": category, "businesses": businesses, "posts": posts})
        else:
            neighborhood = profile.neighborhood

        if location == "":
            location = None
        else:
            location = Location.objects.get(name=location)

        if request.FILES:
            image = request.FILES["image"]
            image = cloudinary.uploader.upload(image)
            image_url = image["url"]

            post = Post(
                user_id=current_user.id,
                title=title,
                content=content,
                image=image_url,
                category=category,
                location=location,
                neighborhood=neighborhood,
            )
            post.save_post()

            return redirect("/profile", {"success": "Post was Created Successfully"})
        else:
            post = Post(
                user_id=current_user.id,
                title=title,
                content=content,
                category=category,
                location=location,
                neighborhood=neighborhood,
            )
            post.save_post()

            return redirect("/profile", {"success": "Post Created Successfully"})

    else:
        return render(request, "profile.html", {"danger": "Post Creation Failed"})