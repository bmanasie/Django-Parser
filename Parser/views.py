from django.db.models import Q
from django.views.generic import TemplateView , ListView

from .models import NEM13


class HomePageView ( TemplateView ) :
    template_name = 'home.html'


class SearchResultsView ( ListView ) :
    model = NEM13
    template_name = 'Search.html'

    def get_queryset(self) :
        query = self.request.GET.get ( 'q' )
        object_list = NEM13.objects.filter (
            Q ( nmi = query ) | Q ( serial_number = query )
        )
        return object_list