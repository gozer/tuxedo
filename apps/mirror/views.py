import hashlib

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from lib.sort_headers import SortHeaders
from models import Location, LocationMirrorMap, Mirror
from forms import UptakeForm


UPTAKE_LIST_HEADERS = (
    ('Product', 'location__product__name'),
    ('OS', 'location__os__name'),
    ('Available', 'available'),
    ('Total', None)
)
LOCATION_STATS_LIST_HEADERS = (
    ('Status', 'active'),
    ('Host Name', 'mirror__name'),
    ('Address', 'mirror__baseurl'),
    ('Path', 'location__path')
)

def index(request):
    """Main index/summary page"""
    # generic front page
    if not request.user.is_authenticated():
        return render_to_response('mirror/index.html', context_instance=
                                  RequestContext(request))

    # personal summary page
    data = {}

    # gravatar
    emailhash = hashlib.md5(request.user.email).hexdigest()
    data['gravatar'] = 'http://www.gravatar.com/avatar/%s.jpg?'\
                       'd=identicon' % emailhash

    # mirror data
    mirrors = Mirror.objects.filter(contacts=request.user).order_by('name')
    data['mirrors'] = mirrors

    return render_to_response('mirror/summary.html', data, context_instance=
                              RequestContext(request))


@staff_member_required
def uptake(request):
    """Product Uptake on Mirrors"""
    if request.GET.get('p'):
        form = UptakeForm(request.GET)
    else:
        form = UptakeForm()

    data = {'form': form}

    if form.is_bound:
        sort_headers = SortHeaders(request, UPTAKE_LIST_HEADERS)
        products = [ int(p) for p in form.data.getlist('p') ]
        uptake = Location.get_mirror_uptake(
            products, order_by=sort_headers.get_order_by())
        data.update({'locations': uptake,
                     'headers': list(sort_headers.headers()),
                     'use_sorttable': True,
                    })

    return render_to_response('mirror/uptake.html', data, context_instance =
                              RequestContext(request))

@staff_member_required
def lstats(request):
    """Location Statistics"""
    if request.GET.get('p'):
        # using the same form as Uptake for now.
        form = UptakeForm(request.GET)
    else:
        form = UptakeForm()
    data = {'form': form}

    if form.is_bound:
        sort_headers = SortHeaders(request, LOCATION_STATS_LIST_HEADERS)
        products = [ int(p) for p in form.data.getlist('p') ]
        locations = LocationMirrorMap.objects \
            .filter(location__product__id__in=products) \
            .values('active', 'mirror__name', 'mirror__baseurl',
                    'location__path') \
            .order_by(sort_headers.get_order_by())
        data.update({'locations': locations,
                     'headers': list(sort_headers.headers()),
                     'use_sorttable': True,
                    })
    return render_to_response('mirror/lstats.html', data, context_instance =
                              RequestContext(request))

