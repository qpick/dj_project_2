from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("auctions/create/", views.CreateAdListingView.as_view(), name="create_ad_listing"),
    path("auctions/watchlist/", views.WatchAdListingView.as_view(), name="watch_ad_listing"),
    path("auctions/categories/", views.CategoriesView.as_view(), name="categories"),
    path("auctions/closelist/", views.CloseAdListingView.as_view(), name="close_ad_listing"),
    path("auctions/adlistingsbycategory/<str:category_id>", views.AdListingsByCategoryView.as_view(),
         name="ad_listings_by_category"),
    path("auctions/<str:ad_listing_id>/", views.AdListingView.as_view(), name="view_ad_listing"),
    path("auctions/addcomment/<str:ad_listing_id>/", views.AddCommentView.as_view(), name="add_comment"),
    path("auctions/offerbid/<str:ad_listing_id>/", views.OfferBidView.as_view(), name="offer_bid"),
]
