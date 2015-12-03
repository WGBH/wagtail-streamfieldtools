from wagtail.wagtailcore.blocks import StreamBlock, StreamValue

from .base import RenditionMixIn


class RenditionAwareStreamValue(RenditionMixIn, StreamValue):

    def __init__(self, stream_block, stream_data,
                 raw_text=None, rendition=None):
        super(RenditionAwareStreamValue, self).__init__(
            stream_block=stream_block,
            stream_data=stream_data,
            is_lazy=True,
            raw_text=raw_text
        )
        self.rendition = rendition

    def __getitem__(self, i):
        if i not in self._bound_blocks:
            if self.is_lazy:
                raw_value = self.stream_data[i]
                type_name = raw_value['type']
                child_block = self.stream_block.child_blocks[type_name]
                value = child_block.to_python(raw_value['value'])
            child_block.rendition = self.rendition
            self._bound_blocks[i] = StreamValue.StreamChild(child_block, value)
        return self._bound_blocks[i]


class RenditionAwareStreamBlock(RenditionMixIn, StreamBlock):

    def to_python(self, value):
        return RenditionAwareStreamValue(
            self,
            [
                child_data
                for child_data in value
                if child_data['type'] in self.child_blocks.keys()
            ],
            rendition=self.rendition
        )
