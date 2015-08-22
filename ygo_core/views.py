
from django.views.generic import TemplateView
from .mixins import LoginRequiredMixin, BootstrapDataMixin


class PageView(TemplateView):

    http_method_names = ['get']


class AuthenticatedPageView(LoginRequiredMixin, PageView):

    pass


class CollectionPageView(BootstrapDataMixin,
                         AuthenticatedPageView):

    template_name = 'pages/collection.html'


class BrowsePageView(BootstrapDataMixin, AuthenticatedPageView):

    template_name = 'pages/browse.html'


class DeckListPageView(AuthenticatedPageView):

    template_name = 'pages/deck_list.html'

    def get_context_data(self, **kwargs):
        context = super(DeckListPageView, self).get_context_data(**kwargs)

        decks = (self.request.user.decks.all()
                 .order_by('name')
                 .prefetch_related('deck_cards'))

        context.update({
            'decks': decks
        })

        return context


class IndexPageView(PageView):

    template_name = 'pages/index.html'


class AboutPageView(PageView):

    template_name = 'pages/about.html'


class DonationsPageView(PageView):

    template_name = 'pages/donations.html'
