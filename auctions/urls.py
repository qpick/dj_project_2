from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("auctions/create/", login_required(views.CreateListView.as_view(), login_url='auctions:index'),
         name="create_list"),
    path("auctions/watchlist/", login_required(views.WatchListView.as_view(), login_url='auctions:index'),
         name="watch_list"),
    path("auctions/categories/", login_required(views.CategoriesView.as_view(), login_url='auctions:index'),
         name="categories"),
    path("auctions/closelist/", login_required(views.CloseListView.as_view(), login_url='auctions:index'),
         name="close_list"),
    path("auctions/listsbycategory/<str:category_id>",
         login_required(views.ListsByCategoryView.as_view(),  login_url='auctions:index'), name="lists_by_category"),
    path("auctions/<str:list_id>/", login_required(views.ListView.as_view(), login_url='auctions:index'),
         name="view_list"),
    path("auctions/addcomment/<str:list_id>/", login_required(views.AddCommentView.as_view(), login_url='auctions:index'),
         name="add_comment"),
    path("auctions/offerbid/<str:list_id>/", login_required(views.OfferBidView.as_view(), login_url='auctions:index'),
         name="offer_bid"),
]
