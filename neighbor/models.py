from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')

    image = CloudinaryField('image')
    post_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    posted_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_post_by_user(cls, user):
        project = cls.objects.filter(user=user)
        return project

    def save_image(self):
        self.save()

    def delete_project(self):
        self.delete()

    #  get by id
    @classmethod
    def get_one_post(cls, id):
        project = cls.objects.get(id=id)
        return project

    def update_(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()    

    @classmethod
    def search_post(cls, search_term):
        project = cls.objects.filter(
                    project_name__icontains=search_term)
        return project    

    def __str__(self):
        return self.user.username       

    def __str__(self):
        return self.image_name


class Location(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    # save location
    def save_location(self):
        self.save()

    def __str__(self):
        return self.name

class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    occupants_count = models.IntegerField(default=0)
    Neighbor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def create_neigborhood(self):
        self.save()

    @classmethod
    def delete_neighborhood(cls, id):
        cls.objects.filter(id=id).delete()

    @classmethod
    def update_neighborhood(cls, id):
        cls.objects.filter(id=id).update()

    @classmethod
    def search_by_name(cls, search_term):
        hood = cls.objects.filter(name__icontains=search_term)
        return hood

    @classmethod
    def find_neigborhood(cls, id):
        hood = cls.objects.get(id=id)
        return hood

    def __str__(self):
        return self.name



class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, null=True)
    profile_photo = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def save_profile(self):
        self.save()

    def __str__(self):
        return self.name





class Business(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    # update business
    def update_business(self):
        self.update()

    # search business
    @classmethod
    def search_by_name(cls, search_term):
        business = cls.objects.filter(name__icontains=search_term)
        return business

    # find business by id
    @classmethod
    def find_business(cls, id):
        business = cls.objects.get(id=id)
        return business

    def __str__(self):
        return self.name        