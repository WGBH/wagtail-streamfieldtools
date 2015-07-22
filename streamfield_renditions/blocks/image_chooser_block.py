from __future__ import unicode_literals

from django.utils.safestring import mark_safe

from wagtail.wagtailimages.blocks import ImageChooserBlock

from .base import RenditionMixIn


class RenditionAwareImageChooserBlock(RenditionMixIn, ImageChooserBlock):

    def get_image_rendition(self, value):
        if value:
            return value.get_rendition(
                self.rendition.image_rendition or 'original'
            )
        else:
            return ''

    def render_basic(self, value):
        image = self.get_image_rendition(value)
        if image:
            return image.img_tag()
        else:
            return ''


class RenditionAwareLazyLoadImageChooserBlock(RenditionAwareImageChooserBlock):

    def render_basic(self, value):
        image = self.get_image_rendition(value)
        if image:
            return mark_safe(
                '<img class="lazy" data-original="{url}" '
                'alt="{alt_text}"/>'.format(
                    url=image.url,
                    alt_text=value.title,
                )
            )

        else:
            return ''
