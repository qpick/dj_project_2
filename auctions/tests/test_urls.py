from django.test import SimpleTestCase
from django.urls import reverse, resolve
from auctions import views


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('auctions:index')
        self.assertTrue(resolve(url).func.view_class, views.IndexView)

    def test_create_ad_listing_url_resolves(self):
        url = reverse('auctions:create_ad_listing')
        self.assertTrue(resolve(url).func.view_class, views.CreateAdListingView)

    def test_watch_ad_listing_url_resolves(self):
        url = reverse('auctions:watch_ad_listing')
        self.assertTrue(resolve(url).func.view_class, views.WatchAdListingView)

    def test_categories_url_resolves(self):
        url = reverse('auctions:categories')
        self.assertTrue(resolve(url).func.view_class, views.CategoriesView)

    def test_close_ad_listing_url_resolves(self):
        url = reverse('auctions:close_ad_listing')
        self.assertTrue(resolve(url).func.view_class, views.CloseAdListingView)

    def test_ad_listings_by_category_url_resolves(self):
        url = reverse('auctions:ad_listings_by_category', args=['some-category'])
        self.assertTrue(resolve(url).func.view_class, views.AdListingsByCategoryView)

    def test_view_ad_listing_url_resolves(self):
        url = reverse('auctions:view_ad_listing', args=['example-list-id-1'])
        self.assertTrue(resolve(url).func.view_class, views.AdListingView)

    def test_add_comment_url_resolves(self):
        url = reverse('auctions:add_comment', args=['example-list-id-1'])
        self.assertTrue(resolve(url).func.view_class, views.AddCommentView)

    def test_offer_bid_url_resolves(self):
        url = reverse('auctions:offer_bid', args=['example-list-id-1'])
        self.assertTrue(resolve(url).func.view_class, views.OfferBidView)
