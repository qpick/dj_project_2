from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AdListing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    start_bid = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    photo = models.ImageField(default='default-image.png', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    watchers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="watched_listings")
    current_bid = models.FloatField(default=0, blank=True, null=True)
    new_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='new_owner', blank=True, null=True,
                                  on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + ' ' + self.title

    @property
    def watched(self):
        return self.watchers.all().exists()


class Comment(models.Model):
    content = models.CharField(max_length=200)
    ad_listing = models.ForeignKey(AdListing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Bid(models.Model):
    ad_listing = models.ForeignKey(AdListing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + ' - $' + str(self.price) + ' - ' + self.created_at.strftime('%B %d %Y')
