from django.test import TestCase
from .models import *
from django.contrib.auth.models import User

# Create your tests here.

class NeighborhoodTestClass(TestCase):
    def setUp(self):
        self.location = Location(name='Test Location')
        self.location.save_location()
        self.neighborhood = Neighborhood(
            name='Test Neighbor', location=self.location)

    def test_instance(self):
        self.assertTrue(isinstance(self.neighbourhood, Neighborhood))

    def test_save_method(self):
        self.neighbourhood.create_neigborhood()
        neighborhoods = Neighborhood.objects.all()
        self.assertTrue(len(neighborhoods) > 0)

    def test_delete_method(self):
        self.neighborhood.create_neigborhood()
        self.neighborhood.delete()
        neighborhoods = Neighborhood.objects.all()
        self.assertTrue(len(neighborhoods) == 0)


# Location Model Tests
class LocationTestClass(TestCase):
    def setUp(self):
        self.location = Location(name='Test Location')

    def test_instance(self):
        self.assertTrue(isinstance(self.location, Location))

    def test_save_method(self):
        self.location.save_location()
        locations = Location.objects.all()
        self.assertTrue(len(locations) > 0)

    def test_delete_method(self):
        self.location.save_location()
        self.location.delete()
        locations = Location.objects.all()
        self.assertTrue(len(locations) == 0)