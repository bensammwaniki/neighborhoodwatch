from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api
from os import name
# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'index.html')
@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    userid =current_user.id
    profile = Profile.objects.filter(user_id = current_user.id).first()
    posts = Post.objects.filter(user_id=current_user.id)
    locations = Location.objects.all()
    neighborhood = Neighborhood.objects.all()
    businesses = Business.objects.filter(user_id=userid)
    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'locations': locations, 'neighborhood': neighborhood, 'businesses': businesses})

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