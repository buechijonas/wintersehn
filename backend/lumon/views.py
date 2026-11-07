from django.http import Http404, HttpResponse

from . import fake, tmdb


def fake_poster(request, tmdb_id):
    title = fake.find(tmdb_id)
    if not tmdb.fake_mode() or not title:
        raise Http404
    return HttpResponse(fake.poster(title), content_type="image/svg+xml")


def fake_backdrop(request, tmdb_id):
    title = fake.find(tmdb_id)
    if not tmdb.fake_mode() or not title:
        raise Http404
    return HttpResponse(fake.backdrop(title), content_type="image/svg+xml")
