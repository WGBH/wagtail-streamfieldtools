from __future__ import unicode_literals

from django.conf import settings

WAGTAIL_RENDITION_SETS = getattr(settings, 'WAGTAIL_RENDITION_SETS', {})


class InvalidRendition(Exception):
    pass


class UnavailableRendition(Exception):
    pass


class RenditionMixIn(object):

    def __init__(self, *args, **kwargs):
        self._rendition = {}
        super(RenditionMixIn, self).__init__(*args, **kwargs)

    @property
    def rendition(self):
        return self._rendition or {}

    @rendition.setter
    def rendition(self, value):
        if not value:
            pass
        elif not isinstance(value, dict):
            raise InvalidRendition('Renditions must be dictionaries.')
        else:
            self._rendition = value
