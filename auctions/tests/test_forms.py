from django.test import TestCase
from auctions import forms
from auctions.models import Category


class TestForms(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='shoes'
        )

    def test_ad_listing_form_valid_data(self):
        category = Category.objects.filter(name='shoes').first()

        form = forms.AdListingForm(data={
            'title': 'test title',
            'description': 'test description',
            'start_bid': 10,
            'category': category.id
        })

        self.assertTrue(form.is_valid())

    def test_comment_form_valid_data(self):
        form = forms.CommentForm(data={
            'content': 'test comment content',
        })
        # print('form errors are: ', form.errors)

        self.assertTrue(form.is_valid())

    def test_bid_form_valid_data(self):
        form = forms.BidForm(data={
            'price': 10,
        })

        self.assertTrue(form.is_valid())
