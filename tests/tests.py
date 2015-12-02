from django.core.exceptions import FieldError
from django.test import TestCase
from django.test.utils import override_settings

from streamfield_tools.fields import RegisteredBlockStreamField
from streamfield_tools.registry import (
    find_blocks,
    AlreadyRegistered,
    NotRegistered,
    InvalidBlock
)


class StreamFieldToolsTestCase(TestCase):

    @override_settings(
        INSTALLED_APPS=('tests.test_find_blocks',)
    )
    def test_find_blocks(self):
        """
        Ensures streamfield_tools.registry.find_blocks raises the
        appropriate exception when trying to import on registered_blocks.py
        modules.
        """
        self.assertRaises(
            ImportError,
            find_blocks
        )

    @override_settings(
        INSTALLED_APPS=('tests', 'tests.test_exception_alreadyregistered',)
    )
    def test_exception_alreadyregistered(self):
        """
        Ensures AlreadyRegistered is raised when trying to register a block
        with an already-registered block_type.
        """
        self.assertRaises(
            AlreadyRegistered,
            find_blocks
        )

    @override_settings(
        INSTALLED_APPS=('tests', 'tests.test_exception_invalidblock',)
    )
    def test_exception_invalidblock(self):
        """
        Ensures InvalidBlock raises when trying to register a block that is
        not an instance of wagtail.wagtailcore.blocks.Block
        """
        self.assertRaises(
            InvalidBlock,
            find_blocks
        )

    @override_settings(
        INSTALLED_APPS=('tests.test_exception_notregistered',)
    )
    def test_exception_notregistered(self):
        """
        Ensures NotRegistered raises when trying to unregister a block that is
        not yet registered.
        """
        self.assertRaises(
            NotRegistered,
            find_blocks
        )

    def test_exception_fielderror(self):
        """
        Ensures FieldError raises if a RegisteredBlockStreamField is defined
        that specifies both the `exclude_blocks` and `only_blocks` kwargs.
        """
        self.assertRaises(
            FieldError,
            lambda: RegisteredBlockStreamField(
                exclude_blocks=['foo'],
                only_blocks=['bar']
            )
        )

    @override_settings(
        INSTALLED_APPS=('tests.test_unregister_block',)
    )
    def test_unregister_block(self):
        """
        Ensures a registered block can be unregistered.
        """
        find_blocks()
