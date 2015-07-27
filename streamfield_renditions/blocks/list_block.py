from wagtail.wagtailcore.blocks import ListBlock

from .base import RenditionMixIn


class RenditionAwareListBlock(RenditionMixIn, ListBlock):

    def to_python(self, value):
        self.child_block.rendition = self.rendition
        return super(RenditionAwareListBlock, self).to_python(value)
