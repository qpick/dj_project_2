from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from auctions import forms as auctions_forms
from .models import AdListing, Category, Comment, Bid
from .util import check_bid


class IndexView(View):

    def get(self, request):
        ad_listings = AdListing.objects.all().order_by('-created_at')

        context = {
            'ad_listings': ad_listings
        }

        return render(request, "auctions/index.html", context)


class AdListingView(LoginRequiredMixin, View):

    def get(self, request, ad_listing_id):
        try:
            ad_listing = AdListing.objects.get(pk=ad_listing_id)
        except Exception as e:
            assert e
            return redirect(reverse('auctions:index'))

        comment_form = auctions_forms.CommentForm
        comments = Comment.objects.filter(ad_listing=ad_listing).order_by('-created_at')
        offer_bid_form = auctions_forms.BidForm()
        message = request.GET.get('message') if request.GET.getlist('message') else None

        context = {
            'ad_listing': ad_listing,
            'comment_form': comment_form,
            'comments': comments,
            'offer_bid_form': offer_bid_form,
            'message': message
        }
        return render(request, 'auctions/view_ad_listing.html', context)


class CreateAdListingView(LoginRequiredMixin, View):

    def get(self, request):
        form = auctions_forms.AdListingForm()
        context = {
            'form': form
        }
        return render(request, 'auctions/create_ad_listing.html', context)

    def post(self, request):
        form = auctions_forms.AdListingForm(request.POST, request.FILES)

        if not form.is_valid():
            form = auctions_forms.AdListingForm(request.POST)
            context = {
                'form': form,
                'message': 'error'
            }
            return render(request, 'auctions/create_ad_listing.html', context)

        new_ad_listing = form.save(commit=False)
        new_ad_listing.owner = request.user
        new_ad_listing.save()

        return redirect(reverse('auctions:index'))


class WatchAdListingView(LoginRequiredMixin, View):

    def get(self, request):
        ad_listings = request.user.watched_listings.all()

        context = {
            'ad_listings': ad_listings
        }
        return render(request, 'auctions/watch_ad_listing.html', context)

    def post(self, request):
        ad_listings_watched = AdListing.objects.get(id=request.POST.get('ad_listing_id'))

        if request.user in ad_listings_watched.watchers.all():
            ad_listings_watched.watchers.remove(request.user)
        else:
            ad_listings_watched.watchers.add(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CategoriesView(LoginRequiredMixin, View):

    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'auctions/categories_page.html', context)


class AdListingsByCategoryView(LoginRequiredMixin, View):

    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)

        ad_listings = AdListing.objects.filter(category_id=category_id)
        context = {
            'category': category,
            'ad_listings': ad_listings
        }
        return render(request, 'auctions/ad_listings_by_category.html', context)


class AddCommentView(LoginRequiredMixin, View):

    def post(self, request, ad_listing_id):
        ad_listing = AdListing.objects.get(id=ad_listing_id)
        form = auctions_forms.CommentForm(request.POST)

        if not form.is_valid():
            return redirect(reverse('auctions:view_ad_listing', args=[ad_listing_id]))

        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.ad_listing = ad_listing
        new_form.save()

        return redirect(reverse('auctions:view_ad_listing', args=[ad_listing_id]))


class OfferBidView(LoginRequiredMixin, View):

    def post(self, request, ad_listing_id):
        ad_listing = AdListing.objects.get(id=ad_listing_id)

        if not check_bid(request.POST.get('price'), ad_listing):
            return redirect(
                reverse('auctions:view_ad_listing', args=[ad_listing_id]) + '?message=Please enter bigger offer than '
                                                                            'start price and actual price ')

        form = auctions_forms.BidForm(request.POST)

        if not form.is_valid():
            return redirect(reverse('auctions:view_ad_listing', args=[ad_listing_id]))

        new_bid = form.save(commit=False)
        new_bid.ad_listing = ad_listing
        new_bid.user = request.user
        new_bid.save()
        ad_listing.current_bid = request.POST.get('price')
        ad_listing.save()

        return redirect(reverse('auctions:view_ad_listing', args=[ad_listing_id]) + '?message=Successfully added bid.')


class CloseAdListingView(LoginRequiredMixin, View):

    def post(self, request):
        ad_listing = get_object_or_404(AdListing, id=request.POST.get('ad_listing_id'))

        if request.user != ad_listing.owner:
            return redirect(reverse('auctions:index'))

        ad_listing.active = False
        ad_listing.new_owner = Bid.objects.filter(ad_listing=ad_listing).last().user
        ad_listing.save()

        return redirect(reverse('auctions:view_ad_listing', args=[request.POST.get('ad_listing_id')]))
