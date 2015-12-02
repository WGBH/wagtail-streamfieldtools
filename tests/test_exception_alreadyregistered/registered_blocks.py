from wagtail.wagtailcore.blocks import CharBlock

from streamfield_tools.registry import block_registry


block_registry.register_block(
    'heading',
    CharBlock()
)
