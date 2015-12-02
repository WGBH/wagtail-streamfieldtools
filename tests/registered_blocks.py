from wagtail.wagtailcore.blocks import CharBlock

from streamfield_tools.registry import block_registry

from .blocks import rendition_aware_test_block

block_registry.register_block(
    'heading',
    CharBlock(classname="full title", icon='title')
)

block_registry.register_block(
    'rendition_aware_test_block',
    rendition_aware_test_block
)
