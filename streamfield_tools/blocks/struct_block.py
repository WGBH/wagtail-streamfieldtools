from __future__ import unicode_literals
from collections import OrderedDict

from django.template.loader import render_to_string
from django.utils import six

from wagtail.wagtailcore.blocks import StructBlock, StructValue, TextBlock

from .base import (
    InvalidRendition,
    Rendition,
    RenditionMixIn,
    WAGTAIL_RENDITION_SETS
)
from .field_block import RenditionSetChoiceBlock


class TemplateRequired(Exception):
    pass


class MultiRenditionStructBlock(StructBlock):

    def __init__(self, local_blocks, core_renditions,
                 addl_renditions_settings_key=None, **kwargs):
        rendition_set_config = OrderedDict()
        for rendition in core_renditions:
            if isinstance(rendition, Rendition):
                rendition_set_config[rendition.short_name] = rendition
            else:
                raise InvalidRendition(
                    "Only instances of streamfield_tools.blocks."
                    "Rendition can be passed as `core_renditions`."
                )

        addl_rendition_set_config = WAGTAIL_RENDITION_SETS.get(
            addl_renditions_settings_key
        )
        if addl_rendition_set_config:
            for short_name, config in six.iteritems(addl_rendition_set_config):
                r = Rendition(short_name, **config)
                rendition_set_config[r.short_name] = r

        self._rendition_set_config = rendition_set_config
        local_blocks.append(
            (
                'addl_classes',
                TextBlock(
                    label='Additional Classes',
                    required=False,
                    help_text="Enter any additional classes you'd like to add "
                              "to this module's containing div."
                )
            )
        )
        local_blocks.append(
            (
                'render_as',
                RenditionSetChoiceBlock(
                    rendition_set_config=rendition_set_config,
                    label='Render As',
                    required=True,
                    help_text='How this module should be rendered.'
                )
            )
        )

        super(MultiRenditionStructBlock, self).__init__(
            local_blocks=local_blocks,
            **kwargs
        )

    def get_rendition(self, value):
        """Return the rendition associated with `value`."""
        return self._rendition_set_config.get(
            value['render_as']
        )

    def get_context(self, value):
        context = super(MultiRenditionStructBlock, self).get_context(
            value
        )
        rendition = self._rendition_set_config.get(
            value['render_as']
        )
        context['image_rendition'] = rendition.image_rendition or 'original'
        context['addl_classes'] = value['addl_classes']
        return context

    def render(self, value):
        rendition = self.get_rendition(value)
        return rendition.template.render(
            self.get_context(value)
        )

    def to_python(self, value):
        # This is where the rendition needs to be injected.
        # Blocks used by RenditionStructBlock must have a to_python method
        # that can either accept **kwargs or an extra kwarg named `rendition`
        struct_value_list = []
        for name, child_block in self.child_blocks.items():
            if name in value:
                child_block.rendition = self._rendition_set_config.get(
                    value['render_as']
                )
                to_append = child_block.to_python(value[name])
            else:
                to_append = child_block.get_default()
            struct_value_list.append((name, to_append))
        return StructValue(self, struct_value_list)


class RenditionAwareStructBlock(RenditionMixIn, StructBlock):

    class Meta:
        template = None

    def get_context(self, value):
        """Ensure `image_rendition` is added to the global context."""
        context = super(RenditionAwareStructBlock, self).get_context(value)
        context['image_rendition'] = self.rendition.\
            image_rendition or 'original'
        return context

    def render(self, value):
        if self.meta.template is None:
            raise TemplateRequired(
                "{} does not specify a template. "
                "RenditionAwareStructBlock subclasses must specify "
                "a template.".format(self.__class__.__name__)
            )
        else:
            try:
                template = getattr(
                    self.meta,
                    'template_{}'.format(self.rendition.short_name)
                )
            except AttributeError:
                template = self.meta.template

            return render_to_string(template, self.get_context(value))
