from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Listings(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    bid=models.IntegerField()
    image=models.URLField(blank=True)
    category=models.CharField(max_length=50,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="listing")
    active=models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.title} to {self.description} price {self.bid}"


class Watchlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="watch")
    watchlist=models.ManyToManyField(Listings, related_name='cart')    


class Bid(models.Model):
    item=models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="amount")
    bid=models.IntegerField(blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="money")

    def __str__(self):
        return f"{self.item}  {self.user} price {self.bid}"

