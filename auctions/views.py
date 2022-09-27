from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *

class Newform(forms.Form):
    title=forms.CharField(max_length=50)
    description= forms.CharField(max_length=200)
    bid=forms.IntegerField()
    image=forms.URLField(required=False)
    category=forms.CharField(max_length=50,required=False)

def index(request):
    li = Listings.objects.filter(active=True)
    return render(request, "auctions/index.html",{'lists':li})

def create(request):
    if request.method == "POST":
        title=request.POST["title"]
        description= request.POST["description"]
        bid=request.POST["bid"]
        image=request.POST["image"]
        category=request.POST["category"]
        li = Listings(title=title,description=description,bid=bid,image=image,category=category, user=request.user)
        li.save()
    form=Newform()
    return render(request, "auctions/create.html",{"form":form})

def listing(request, list_id):
    print("1")
    listing = Listings.objects.get(pk=list_id)
    price=listing.bid
    if (listing.amount.filter(item=list_id).last()):
        price=listing.amount.filter(item=list_id).last().bid
    user = request.user.is_authenticated
    comments=listing.comment.all()
    if user != None:
            if listing.user==request.user:
                return render(request, "auctions/listing.html", {'listing':listing, 'user':request.user, 'price':price, 'bool':True, 'comments':comments})
            return render(request, "auctions/listing.html", {'listing':listing, 'user':request.user, 'price':price, 'comments':comments})
        
    return render(request, "auctions/listing.html", {'listing':listing})

def cdlisting(request, list_id):
    
    listing = Listings.objects.get(pk=list_id)
    user = User.objects.get(pk=request.user.id)
    if (listing.amount.filter(item=list_id).last() and user.money.filter(user=request.user)):
        price=listing.amount.filter(item=list_id).last().bid
        if price==user.money.filter(user=request.user).last().bid:
            return render(request, "auctions/listing.html", {'listing':listing, 'price':price, "message":'You won the Bid'})
    return render(request, "auctions/listing.html", {'listing':listing, 'price':price})
        

def add(request, listing_id):
    lists = Listings.objects.get(pk=listing_id)
    if(Watchlist.objects.filter(user=request.user)):
        Watchlist.objects.get(user=request.user).watchlist.add(lists)
    else:
        x=Watchlist(user=request.user)
        x.save()
        x.watchlist.add(lists)
    return HttpResponseRedirect(reverse("watch"))

def close(request, listing_id):
    lists = Listings.objects.get(pk=listing_id)
    lists.active=False
    lists.save()
    return HttpResponseRedirect(reverse("index"))

def closed(request):
    lists = Listings.objects.filter(active=False)
    return render(request, "auctions/closed.html", {'listing':lists})

    

def watch(request):
    lists=Watchlist.objects.get(user=request.user).watchlist.all()
    return render(request, "auctions/watchlist.html", {'lists':lists})

def bidding(request, listing_id):
        if request.method=="POST":
            p=int(request.POST['bid'])
            
            lists = Listings.objects.get(pk=listing_id)
            if (Bid.objects.filter(item=listing_id).last()):
                x=int(Bid.objects.filter(item=listing_id).last().bid)
                
            else :
                x=lists.bid
            user = request.user
            
            if (p>lists.bid and p>x):
       
                if Bid.objects.filter(item=listing_id, user=user):
  
                    y=Bid.objects.filter(item=listing_id).get(user=user)
                    y.bid=p

                    y.save()

                else:
                    Bid(item=lists,bid=p,user=user).save()
                return HttpResponseRedirect(reverse('listing', args = [lists.id]))
            else:
                return render(request, "auctions/listing.html", {'listing':lists, 'user':request.user, 'price':x, "message":'Bid Price is low'})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

    
