from django.conf import settings
from django.db.models import Count, Max, Min
from django.core.cache import cache

from chronam.core import models, index, forms


def extra_request_info(request):
    """
    Add some extra useful stuff into the RequestContext.
    """
    return {
        'site_title': 'Chronicling America',
        'omniture_url': settings.OMNITURE_SCRIPT,
        'sharetool_url': settings.SHARETOOL_URL if "SHARETOOL_URL" in dir(settings) else None,
        }


def cors(request):
    """
    Add CORS headers so that the JSON can be used easily from JavaSript
    without requiring proxying.
    """
    pass


def get_search_form (request):
    params = request.GET if request.GET else None
    form = forms.SearchPagesForm(params)
    adv_form = forms.AdvSearchPagesForm(params)
    return {'search_form': form, 'adv_search_form': adv_form,}


def newspaper_info(request):
    info = cache.get("newspaper_info")
    if info is None:
        total_page_count = index.page_count()
        titles_with_issues = models.Title.objects.filter(has_issues=True)
        titles_with_issues_count = titles_with_issues.count()

        _places = models.Place.objects.filter(titles__in=titles_with_issues)
        states_with_issues = sorted(set(place.state for place in _places if place.state is not None))

        _languages = models.Language.objects.filter(titles__in=titles_with_issues)
        languages_with_issues = sorted(set((lang.code, lang.name) for lang in _languages))

        # TODO: might make sense to add a Ethnicity.has_issue model field
        # to save having to recompute this all the time, eventhough it 
        # shouldn't take more than 1/2 a second, it all adds up eh?
        ethnicities_with_issues = []
        for e in models.Ethnicity.objects.all():
            # fliter out a few ethnicities, not sure why really
            # https://rdc.lctl.gov/trac/chronam/ticket/724#comment:22
            if e.has_issues and e.name not in ["African", "Canadian", "Welsh"]:
                ethnicities_with_issues.append(e.name)

        info = {'titles_with_issues_count': titles_with_issues_count,
                'states_with_issues': states_with_issues,
                'languages_with_issues': languages_with_issues,
                'ethnicities_with_issues': ethnicities_with_issues,
                'total_page_count': total_page_count}

        cache.set("newspaper_info", info)        
    
    return info

