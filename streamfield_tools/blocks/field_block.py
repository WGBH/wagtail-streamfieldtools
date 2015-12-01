from django.utils.six import iteritems

from wagtail.wagtailcore.blocks import ChoiceBlock


class RenditionSetChoiceBlock(ChoiceBlock):

    def __init__(self, rendition_set_config, required=True, help_text=None,
                 **kwargs):

        choices = [
            (rendition.short_name, rendition.verbose_name)
            for rendition_key, rendition in iteritems(rendition_set_config)
        ]

        super(RenditionSetChoiceBlock, self).__init__(
            choices=choices,
            required=required,
            help_text=help_text,
            **kwargs
        )
