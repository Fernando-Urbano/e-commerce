# E-Commerce
This is project number 2 of the CS50 Web Development course with Django and JavaScript lectured by Harvard CS department.

## Screencast of project
[https://www.youtube.com/watch?v=wkML34wZBQU](https://www.youtube.com/watch?v=FqzSTWCXzH0&feature=youtu.be)

## Create Listing
Users can visit a page to create a new listing. They should specify a title for the listing, a text-based description, and what the starting bid should be. Users can also provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

![image](https://github.com/Fernando-Urbano/cs50w-p2-commerce/assets/99626376/f17c6763-2359-4673-8801-56d6e89b1c90)

## Active Listing Page
The default route of your web application let users view all of the currently active auction listings. For each active listing, this page displais the title, description, current price, and photo (if one exists for the listing).

![image](https://github.com/Fernando-Urbano/cs50w-p2-commerce/assets/99626376/9ae43152-ae04-4b3b-82de-36b70ee0f4f9)

## Listing Page
Clicking on a listing takes the users to a page specific to that listing. On that page, users can view all details about the listing, including the current price for the listing.

![image](https://github.com/Fernando-Urbano/cs50w-p2-commerce/assets/99626376/9e1c2f6b-d4de-49b0-a9ac-f5948fb44ade)

- If the user is signed in, the user can add the item to their “Watchlist.” If the item is already on the watchlist, the user can remove it.
- If the user is signed in, the user can bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user is presented with an error.
- If the user is signed in and is the one who created the listing, the user has the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
- If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
- Users who are signed in can add comments to the listing page. The listing page displays all comments that have been made on the listing.

## Watchlist
Users who are signed in can visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing’s page.

<img width="957" alt="image" src="https://github.com/Fernando-Urbano/cs50w-p2-commerce/assets/99626376/5125a9ec-ddce-496c-856f-b5ea59faaeb9">

## Categories
Users can visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.

<img width="785" alt="image" src="https://github.com/Fernando-Urbano/cs50w-p2-commerce/assets/99626376/7d70c24e-5dc0-47d1-97b2-4bd32346666e">

## Django Admin Interface
Via the Django admin interface, a site administrator can view, add, edit, and delete any listings, comments, and bids made on the site.

<img width="436" alt="image" src="https://github.com/Fernando-Urbano/cs50w-p2-commerce/assets/99626376/f09f6183-294f-4ab7-b4ae-7834461b1886">
