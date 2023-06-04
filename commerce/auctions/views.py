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


def place_bid(request):
    auction_id = request.POST["auction_id"]
    user_id = request.POST["user_id"]
    bid_value = request.POST["bid_value"]
    if bid_value == "":
        message = f"Bid value must be a valid number."
        request.session['add_bid_message'] = message
        return redirect('auction_details', auction_id=auction_id)
    try:
        bid_value = float(bid_value)
    except ValueError:
        message = f"{bid_value} is not recognizable as a number."
        request.session['add_bid_message'] = message
        return redirect('auction_details', auction_id=auction_id)
    user = User.objects.get(pk=user_id)
    auction = Auction.objects.get(pk=auction_id)
    if bid_value < auction.min_next_bid:
        message = f"Bid value must be at least US$ {auction.min_next_bid:.2f}"
    else:
        message = f'Bid of US$ {bid_value:.2f} successfully placed for "{auction.name}".'
        bid = Bid(user=user, auction=auction, value=bid_value)
        bid.save()
        if not user.watchlist.filter(pk=auction_id).exists():
            user.watchlist.add(auction)
            user.save()
            message += " Added item to your Watchlist."
    request.session['add_bid_message'] = message
    return redirect('auction_details', auction_id=auction_id)


def auction_details(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    bids = auction.bids.all()
    highest_bid = auction.bids.order_by('-value').first()
    highest_bid_value = highest_bid.value if highest_bid else None
    highest_bid_user = highest_bid.user if highest_bid else None
    comments = auction.comments.all()
    add_bid_message = request.session.pop('add_bid_message', "")
    add_comment_message = request.session.pop('add_comment_message', "")
    if request.user.id:
        is_authenticated = True
        auction_owner = True if request.user.id == auction.user.id else False
    else:
        is_authenticated = False
        auction_owner = False
    return render(request, 'auctions/auction_details.html', {
        'add_comment_message': add_comment_message,
        'add_bid_message': add_bid_message,
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


def add_comment(request):
    comment_text = request.POST["comment_text"]
    auction_id = request.POST["auction_id"]
    if comment_text == "":
        message = "Comment must not be empty."
        request.session['add_comment_message'] = message
        return redirect('auction_details', auction_id=auction_id)
    user_id = request.POST["user_id"]
    user = User.objects.get(pk=user_id)
    auction = Auction.objects.get(pk=auction_id)
    comment = Comment(user=user, auction=auction, text=comment_text)
    comment.save()
    return redirect('auction_details', auction_id=auction_id)


def remove_comment(request):
    auction_id = request.POST["auction_id"]
    comment_id = request.POST["comment_id"]
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('auction_details', auction_id=auction_id)


@login_required(redirect_field_name='login')
def watchlist(request):
    user = request.user
    watchlist_active_auctions = user.watchlist.filter(closed=False)
    watchlist_winner_auctions = Auction.objects.filter(winner=user)
    watchlist_winning_auctions = User.winning_auctions(user)
    return render(request, "auctions/watchlist.html", {
        'watchlist_active_auctions': watchlist_active_auctions,
        'watchlist_winner_auctions': watchlist_winner_auctions,
        'watchlist_winning_auctions': watchlist_winning_auctions,
    })


@login_required(redirect_field_name='login')
def auction_builder(request):
    user = request.user
    categories = Category.objects.all()
    return render(request, "auctions/auction_builder.html", {
        'user': user,
        'categories': categories
    })


@login_required(redirect_field_name='login')
def create_auction(request):
    create_auction_message = []
    auction_name = request.POST["auction_name"]
    if not auction_name:
        create_auction_message.append("Auction name must be provided.")
    user_id = request.POST["user_id"]
    user = User.objects.get(pk=user_id)
    description = request.POST["description"]
    if not description:
        create_auction_message.append("Description name must be provided.")
    image_url = request.POST["image_url"]
    image_url = None if image_url == "" else image_url
    try:
        minimum_bid = int(request.POST["minimum_bid"])
        if minimum_bid < 0:
            create_auction_message.append(
                f"Minimum bid ({minimum_bid:.2f}) must be equal or bigger than 0."
            )
    except ValueError:
        create_auction_message.append("Minimum bid must be a number.")
    try:
        bid_minimum_increase = int(request.POST["bid_minimum_increase"])
        if bid_minimum_increase <= 0:
            create_auction_message.append(
                f"Minimum bid increment ({bid_minimum_increase:.2f}) must be bigger than 0."
            )
    except ValueError:
        create_auction_message.append("Minimum bid increment must be a number.")
    category_id = request.POST["category"]
    category = Category.objects.get(pk=category_id) if category_id not in ["--", "", "No Category"] else None
    if not create_auction_message:
        try:
            auction = Auction(
                user=user,
                name=auction_name,
                description=description,
                category=category,
                closed=False,
                image_url=image_url,
                minimum_bid=minimum_bid,
                bid_minimum_increase=bid_minimum_increase
            )
            auction.save()
            auction_id = auction.id
        except Exception as e:
            create_auction_message.append(str(e))
    if create_auction_message:
        categories = Category.objects.all()
        return render(request, "auctions/auction_builder.html", {
            'user': user,
            'create_auction_message': create_auction_message,
            'categories': categories
        })
    else:
        user.watchlist.add(auction)
        return redirect('auction_details', auction_id=auction_id)
    

def withdraw_auction(request):
    auction_id = request.POST["auction_id"]
    auction = Auction.objects.get(pk=auction_id)
    auction.closed = True
    auction.save()
    return redirect('auction_details', auction_id=auction_id)


def accept_current_offer(request):
    auction_id = request.POST["auction_id"]
    auction = Auction.objects.get(pk=auction_id)
    user = Bid.current_bid_user(auction=auction)
    auction.closed = True
    auction.winner = user
    auction.save()
    return redirect('auction_details', auction_id=auction_id)
    

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
