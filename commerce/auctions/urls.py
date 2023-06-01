from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('auctions/<int:auction_id>/', views.auction_details, name='auction_details'),
    path("watchlist", views.watchlist, name="watchlist"),
]
