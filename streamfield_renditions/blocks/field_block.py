from wagtail.wagtailcore.blocks import ChoiceBlock


class RenditionSetChoiceBlock(ChoiceBlock):

    def __init__(self, rendition_set_config, required=True, help_text=None,
                 **kwargs):

        choices = [
            (key, value.get('verbose'))
            for key, value in rendition_set_config.iteritems()
        ]

        super(RenditionSetChoiceBlock, self).__init__(
            choices=choices,
            required=required,
            help_text=help_text,
            **kwargs
        )
