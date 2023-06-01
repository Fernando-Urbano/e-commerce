from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    minimum_bid = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True, max_length=500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        category = self.category if self.category is not None else "No Category"
        return f"{self.name} ({category})"

    @property
    def current_bid(self):
        bid_values = list(self.bids.all().values_list('value', flat=True))
        if bid_values:
            return max(bid_values)
        else:
            return 0


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        text_begin = self.text[:17] + "..." if len(self.text) > 20 else self.text 
        return f"{self.auction} comment - {self.user}: {text_begin}"

    def clean(self):
        if len(self.text) == 0:
            raise ValidationError("Empty comments cannot be posted.")


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    date_created = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.auction} bid - {self.user}: {self.value:.2f}"

    def clean(self):
        if self.value <= 0:
            raise ValidationError("Bid value must be bigger than 0.")
        elif self.value < self.auction.minimum_bid:
            raise ValidationError(f"Bid value must be bigger than {self.auction} action minimum bid ({self.auction.minimum_bid:.2f}).")


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='watchlist')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.user.id} watching {self.auction.name} ({self.auction.id})"

