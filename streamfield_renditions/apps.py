from __future__ import unicode_literals

from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.template import TemplateDoesNotExist
from django.utils.six import iteritems

from .blocks.base import WAGTAIL_RENDITION_SETS
from .utils import verify_rendition_has_required_data, \
    verify_rendition_template


class MalformedRenditionSet(ImproperlyConfigured):
    pass


class StreamFieldRenditionsAppConfig(AppConfig):
    name = 'streamfield_renditions'
    verbose_name = "[Wagtail] StreamField Renditions"

    def ready(self):
        """
        Ensures that settings.WAGTAIL_RENDITION_SETS is properly
        configured.
        """
        for key, rendition_set in iteritems(WAGTAIL_RENDITION_SETS):
            for rendition_set_key, config in iteritems(rendition_set):
                if verify_rendition_has_required_data(config) is False:
                    raise MalformedRenditionSet(
                        "WAGTAIL_RENDITION_SETS['{}']['{}'] is an "
                        "improperly configured rendition. All renditions "
                        "must specify values for both 'verbose' and "
                        "'path_to_template'.".format(key, rendition_set_key)
                    )
                else:
                    if verify_rendition_template(config) is False:
                        raise TemplateDoesNotExist(
                            "WAGTAIL_RENDITION_SETS['{}']['{}']['{}'] points "
                            "to a template ('{}') that does not exist.".format(
                                key,
                                rendition_set_key,
                                'path_to_template',
                                config.get('template_path')
                            )
                        )
