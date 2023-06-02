from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Auction, Bid, Comment, Category


def index(request):
    auctions = Auction.objects.filter(closed=False)
    return render(request, "auctions/index.html", {
        'auctions': auctions
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        'categories': categories
    })


def category_auctions(request, category_id):
    category = Category.objects.get(pk=int(category_id))
    auctions = category.auctions.filter(closed=False)
    return render(request, "auctions/category_auctions.html", {
        'category': category,
        'auctions': auctions
    })


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
    

def change_watchlist(request):
    auction_id = request.POST["auction_id"]
    user_id = request.POST["user_id"]
    user = User.objects.get(pk=user_id)
    auction = Auction.objects.get(pk=auction_id)
    if user.watchlist.filter(pk=auction_id).exists():
        user.watchlist.remove(auction)
    else:
        user.watchlist.add(auction)
    user.save()
    return redirect('auction_details', auction_id=auction_id)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def auction_details(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    bids = auction.bids.all()
    highest_bid = auction.bids.order_by('-value').first()
    highest_bid_value = highest_bid.value if highest_bid else None
    highest_bid_user = highest_bid.user if highest_bid else None
    comments = auction.comments.all()
    if request.user.id:
        is_authenticated = True
        auction_owner = True if request.user.id == auction.user.id else False
    else:
        is_authenticated = False
        auction_owner = False
    return render(request, 'auctions/auction_details.html', {
        'user': request.user,
        'user_watchlist': request.user.watchlist.all(),
        'auction': auction,
        'highest_bid_value': highest_bid_value,
        'highest_bid_user': highest_bid_user,
        'image_url': auction.image_url,
        'bids': bids,
        'comments': comments,
        'is_authenticated': is_authenticated,
        'auction_owner': auction_owner,
        'auction_closed': auction.closed
    })


@login_required(redirect_field_name='login')
def watchlist(request):
    user = request.user
    watchlist_auctions = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        'watchlist': watchlist_auctions
    })
    

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
