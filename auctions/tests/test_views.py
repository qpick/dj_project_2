from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from auctions.models import AdListing, Category
from datetime import datetime


class TestViews(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        # Create user, category, ad_listing, ad_listing_data for testing
        self.UserInstance = get_user_model().objects.create(
            username='test',
            email='test@test.com',
            password='testpassword'
        )

        self.category = Category.objects.create(
            name='shoes'
        )

        self.ad_listing = AdListing.objects.create(
            title='title_test_example',
            description='desc_test_example',
            start_bid=10,
            created_at=datetime.now(),
            active=True,
            owner=self.UserInstance,
            category=self.category
        )

        self.ad_listing_data = {
            'title': 'title',
            'description': 'desc_test_example',
            'start_bid': 10,
            'category': self.category.id
        }

    def test_user_can_see_index_page(self):
        url = reverse('auctions:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/index.html')

    def test_logged_in_user_can_see_ad_listing_page(self):
        url = reverse('auctions:view_ad_listing', args=[self.ad_listing.id])
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/view_ad_listing.html')

    def test_not_logged_in_user_can_not_see_ad_listing_page(self):
        url = reverse('auctions:view_ad_listing', args=[self.ad_listing.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_see_create_ad_listing_page(self):
        url = reverse('auctions:create_ad_listing')
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        response = self.client.get(url, format='text/html')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/create_ad_listing.html')

    def test_not_logged_in_user_can_not_see_create_ad_listing_page(self):
        url = reverse('auctions:create_ad_listing')

        response = self.client.get(url, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_create_new_ad_listing(self):
        url = reverse('auctions:create_ad_listing')
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        response = self.client.post(url, self.ad_listing_data, format='text/html')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(AdListing.objects.filter(title='title').first().title, 'title')

    def test_not_logged_in_user_can_not_create_new_ad_listing(self):
        url = reverse('auctions:create_ad_listing')

        response = self.client.post(url, self.ad_listing_data, format='text/html')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(AdListing.objects.all().count(), 1)

    def test_logged_in_user_can_see_watch_ad_listing_page(self):
        url = reverse('auctions:watch_ad_listing')
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        response = self.client.get(url, format='text/html')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/watch_ad_listing.html')

    def test_not_logged_in_user_can_not_see_watch_ad_listing_page(self):
        url = reverse('auctions:watch_ad_listing')

        response = self.client.get(url, format='text/html')

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_add_ad_listing_to_watch_ad_listing_page(self):
        url = reverse('auctions:watch_ad_listing')
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        ad_listing = AdListing.objects.get(id=self.ad_listing.id)
        response = self.client.post(url, {'ad_listing_id': ad_listing.id}, format='text/html', follow=True)

        self.assertTemplateNotUsed(response, 'users/login.html')

    def test_logged_in_user_can_see_categories_page(self):
        url = reverse('auctions:categories')
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        response = self.client.get(url, format='text/html')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/categories_page.html')

    def test_not_logged_in_user_can_not_see_categories_page(self):
        url = reverse('auctions:categories')

        response = self.client.get(url, format='text/html')

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_see_ad_listings_by_category_page(self):
        url = reverse('auctions:ad_listings_by_category', args=[self.category.id])
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        response = self.client.get(url, format='text/html')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/ad_listings_by_category.html')

    def test_not_logged_in_user_can_not_see_ad_listings_by_category_page(self):
        url = reverse('auctions:ad_listings_by_category', args=[self.category.id])

        response = self.client.get(url, format='text/html')

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_add_comment_to_ad_listing_page(self):
        url = reverse('auctions:add_comment', args=[self.ad_listing.id])
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        comment = {
            'content': 'comment content'
        }
        response = self.client.post(url, comment, format='text/html', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/view_ad_listing.html')

    def test_not_logged_in_user_can_not_add_comment_to_ad_listing_page(self):
        url = reverse('auctions:add_comment', args=[self.ad_listing.id])
        comment = {
            'content': 'comment content'
        }
        response = self.client.post(url, comment, format='text/html', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_logged_in_user_can_offer_bid_to_ad_listing_page(self):
        url = reverse('auctions:offer_bid', args=[self.ad_listing.id])
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        context = {
            'price': 11
        }
        response = self.client.post(url, context, format='text/html', follow=True)
        message = response.context['message']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(message[0]), 1)
        self.assertEqual(str(message), 'Successfully added bid.')

    def test_not_logged_in_user_can_not_offer_bid_to_ad_listing_page(self):
        url = reverse('auctions:offer_bid', args=[self.ad_listing.id])

        context = {
            'price': 11
        }
        response = self.client.post(url, context, format='text/html', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_logged_in_user_that_is_the_owner_can_close_ad_listing_page(self):
        url = reverse('auctions:close_ad_listing')
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        ad_listing = AdListing.objects.create(
            title='title_test_example',
            description='desc_test_example',
            start_bid=10,
            created_at=datetime.now(),
            active=True,
            owner=user,
            category=self.category
        )

        # user offer bid to the list (
        self.client.post(reverse('auctions:offer_bid', args=[ad_listing.id]), {'price': 11}, format='text/html')

        # close the list
        response = self.client.post(url, {'ad_listing_id': ad_listing.id}, format='text/html', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/view_ad_listing.html')

    def test_logged_in_user_that_is_not_the_owner_can_not_close_ad_listing_page(self):
        url = reverse('auctions:close_ad_listing')
        user = get_user_model().objects.get(username='admin-fixture')
        self.client.force_login(user)

        ad_listing = AdListing.objects.create(
            title='title_test_example',
            description='desc_test_example',
            start_bid=10,
            created_at=datetime.now(),
            active=True,
            owner=self.UserInstance,
            category=self.category
        )

        # user offer bid to the list (
        self.client.post(reverse('auctions:offer_bid', args=[ad_listing.id]), {'price': 11}, format='text/html')

        # close the list
        response = self.client.post(url, {'ad_listing_id': ad_listing.id}, format='text/html', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auctions/index.html')
