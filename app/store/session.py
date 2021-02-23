from django.shortcuts import get_object_or_404
from .models import Sneaker


class Session:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        if not self.session.get('favorites'):
            self.session['favorites'] = []

    def add_to_favorites(self, sneaker):
        self.session['favorites'].append(sneaker.slug)
        self.save()

    def remove_from_favorites(self, sneaker):
        try:
            self.session['favorites'].remove(sneaker.slug)
            self.save()
        except ValueError:
            pass

    def get_favorites_sneakers(self):
        return list(map(lambda x: get_object_or_404(Sneaker, slug=x), self.session['favorites']))

    def save(self):
        self.session.modified = True
