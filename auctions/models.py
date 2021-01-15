from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


# this is the model for users and it inherits AbstractUser
class User(AbstractUser):
    pass


# model for listings
class Listing(models.Model):
    # objects = None
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=64, default='')
    subcategory = models.CharField(max_length=64, default='')
    image_link = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    # image_one = models.ImageField(null=True, blank=True, upload_to='images/')
    # image_two = models.ImageField(null=True, blank=True, upload_to='images/')
    # image_three = models.ImageField(null=True, blank=True, upload_to='images/')

# class Category(models.Model):
#     name = models.CharField(max_length=64)
#
#     def __str__(self):
#         return self.name

# model for bids
class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()
    listing = models.ForeignKey(to='Listing', on_delete=models.CASCADE, null=True, blank=True)


# model for comments
class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=64)
    listingid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(to='Listing', on_delete=models.CASCADE, null=True, blank=True)


# model for watchlist
class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    listing = models.ForeignKey(to='Listing', on_delete=models.CASCADE, null=True, blank=True)


# model to store the winners
class Winner(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winprice = models.IntegerField()
    title = models.CharField(max_length=64, null=True)
    listing = models.ForeignKey(to='Listing', on_delete=models.CASCADE, null=True, blank=True)


# class CategoryNew( models.Model ):
#         title = models.CharField(max_length=255, blank=True, null=False)
#         # parents = models.ForeignKey('self', related_name='children', limit_choices_to={'parents__isnull': True}, on_delete=models.CASCADE, default=1, blank=True, null=True)
#         listing = models.ForeignKey(to='Listing', on_delete=models.CASCADE, null=True, blank=True)

# class Category_new(models.Model):
#     parent_category_new = models.ForeignKey('self', null=True, blank=True)
