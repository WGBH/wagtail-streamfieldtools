from wagtail.wagtailcore.blocks import CharBlock

from streamfield_tools.registry import block_registry


block_registry.register_block(
    'short_lived_block',
    CharBlock()
)

block_registry.unregister_block('short_lived_block')
