from django import template
from django.utils.six import iterkeys

REQUIRED_RENDITION_KEYS = ('verbose', 'path_to_template')


def verify_rendition_has_required_data(rendition_config):
    if not all(
        rend_key in iterkeys(rendition_config)
        for rend_key in REQUIRED_RENDITION_KEYS
    ):
        return False
    else:
        return True


def verify_rendition_template(rendition_config):
    template_path = rendition_config['path_to_template']
    try:
        t = template.loader.get_template(
            template_path
        )
    except template.TemplateDoesNotExist:
        return False
    else:
        del t
        return True
