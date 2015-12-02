from __future__ import unicode_literals

from django.utils.safestring import mark_safe

from wagtail.wagtailimages.blocks import ImageChooserBlock

from .base import RenditionMixIn


class RenditionAwareImageChooserBlock(RenditionMixIn, ImageChooserBlock):

    def get_image_rendition(self, value):
        to_return = ''
        if value:
            to_return = value.get_rendition(
                getattr(self.rendition, 'image_rendition', 'original')
            )
        return to_return

    def render_basic(self, value):
        image = self.get_image_rendition(value)
        to_return = ''
        if image:
            to_return = image.img_tag()
        return to_return


class RenditionAwareLazyLoadImageChooserBlock(RenditionAwareImageChooserBlock):

    def render_basic(self, value):
        image = self.get_image_rendition(value)
        to_return = ''
        if image:
            to_return = mark_safe(
                '<img class="lazy" data-original="{url}" width="{width}" '
                'height="{height}" alt="{alt_text}"/>'.format(
                    url=image.url,
                    alt_text=value.title,
                    width=image.width,
                    height=image.height
                )
            )

        return to_return
