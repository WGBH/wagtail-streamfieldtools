from __future__ import unicode_literals

from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django import template
from django.utils.six import iteritems, iterkeys

from .blocks.base import WAGTAIL_RENDITION_SETS

REQUIRED_KEYS = ('verbose', 'path_to_template')


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
                if not all(
                    rend_key in iterkeys(config) for rend_key in REQUIRED_KEYS
                ):
                    raise MalformedRenditionSet(
                        "WAGTAIL_RENDITION_SETS['{}']['{}'] is an "
                        "improperly configured rendition. All renditions "
                        "must specify values for both 'verbose' and "
                        "'path_to_template'.".format(key, rendition_set_key)
                    )
                else:
                    template_path = config['path_to_template']
                    try:
                        t = template.loader.get_template(
                            template_path
                        )
                    except template.TemplateDoesNotExist:
                        raise template.TemplateDoesNotExist(
                            "WAGTAIL_RENDITION_SETS['{}']['{}']['{}'] points "
                            "to a template ('{}') that does not exist.".format(
                                key,
                                rendition_set_key,
                                'path_to_template',
                                template_path
                            )
                        )
                    else:
                        del t
