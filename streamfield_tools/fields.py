from django.core.exceptions import FieldError
from django.utils.six import iteritems

from wagtail.wagtailcore.fields import StreamField

from .registry import block_registry, find_blocks

# Kicking-off block search
find_blocks()


class RegisteredBlockStreamField(StreamField):

    def __init__(self, addl_block_types=None, **kwargs):
        registry_iterator = iteritems(block_registry._registry)
        addl_block_types = addl_block_types or []

        exclude_blocks = kwargs.pop('exclude_blocks', [])
        only_blocks = kwargs.pop('only_blocks', [])
        if exclude_blocks and only_blocks:
            raise FieldError(
                "RegisteredBlockStreamField instances may define either "
                "`exclude_blocks` or `only_blocks`, not both."
            )
        elif exclude_blocks:
            block_types = [
                (block_type, block)
                for block_type, block in registry_iterator
                if block_type not in exclude_blocks
            ]
        elif only_blocks:
            block_types = [
                (block_type, block)
                for block_type, block in registry_iterator
                if block_type in only_blocks
            ]
        else:
            block_types = [
                (block_type, block)
                for block_type, block in registry_iterator
            ]
        if isinstance(addl_block_types, list):
            block_types = block_types + addl_block_types
        super(RegisteredBlockStreamField, self).__init__(block_types, **kwargs)
