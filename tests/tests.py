from django.test import TestCase
from django.test.utils import override_settings

from streamfield_tools.registry import find_blocks


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
