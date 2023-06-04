from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('auctions/<int:auction_id>/', views.auction_details, name='auction_details'),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>/", views.category_auctions, name="category_auctions"),
    path("change-watchlist", views.change_watchlist, name="change_watchlist"),
    path("place-bid", views.place_bid, name="place_bid"),
    path("add-comment", views.add_comment, name="add_comment"),
    path("remove-comment", views.remove_comment, name="remove_comment"),
    path("auction-builder", views.auction_builder, name="auction_builder"),
    path("create-auction", views.create_auction, name="create_auction"),
    path("withdraw-auction", views.withdraw_auction, name="withdraw_auction"),
    path("accept-current-offer", views.accept_current_offer, name="accept_current_offer"),
]