from django.core.exceptions import FieldError
from django.template import Context
from django.template.loader import TemplateDoesNotExist
from django.test import TestCase
from django.test.utils import override_settings

from wagtail.wagtailimages.models import get_image_model
from wagtail.wagtailcore.blocks import CharBlock

from streamfield_tools.blocks import (
    InvalidRendition,
    InvalidRenditionShortName,
    MultiRenditionStructBlock,
    NoTemplateProvided,
    Rendition,
    RenditionAwareImageChooserBlock,
    RenditionAwareLazyLoadImageChooserBlock,
    RenditionAwareStreamBlock,
    RenditionAwareStructBlock,
    TemplateRequired,
)

from streamfield_tools.fields import RegisteredBlockStreamField
from streamfield_tools.registry import (
    find_blocks,
    AlreadyRegistered,
    NotRegistered,
    InvalidBlock
)

from .blocks import rendition_aware_test_block


class StreamFieldToolsTestCase(TestCase):
    fixtures = ['wagtail_images']

    @override_settings(
        INSTALLED_APPS=('tests.test_find_blocks',)
    )
    def test_find_blocks(self):
        """
        Ensure streamfield_tools.registry.find_blocks raises the
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
        Ensure AlreadyRegistered is raised when trying to register a block
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
        Ensure InvalidBlock raises when trying to register a block that is
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
        Ensure NotRegistered raises when trying to unregister a block that is
        not yet registered.
        """
        self.assertRaises(
            NotRegistered,
            find_blocks
        )

    def test_exception_fielderror(self):
        """
        Ensure FieldError raises if a RegisteredBlockStreamField is defined
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
        Ensure a registered block can be unregistered.
        """
        find_blocks()

    def test_rendition(self):
        """
        Test Rendition constructor, exceptions and methods.
        """
        self.assertRaises(
            InvalidRenditionShortName,
            lambda: Rendition(
                short_name='foo9-bar*',
                verbose_name='Foo Bar',
                description='This is misconfigured Rendition instance.'
            )
        )

        self.assertRaises(
            TemplateDoesNotExist,
            lambda: Rendition(
                short_name='foo_bar',
                verbose_name='Foo Bar',
                description='This is another misconfigured Rendition '
                            'instance.',
                path_to_template='foo/bar.html'
            )
        )

        self.assertRaises(
            NoTemplateProvided,
            lambda: Rendition(
                short_name='foo_bar',
                verbose_name='Foo Bar',
                description='This is yet another misconfigured Rendition '
                            'instance.'
            )
        )

        template_from_string = Rendition(
            short_name='foo_bar',
            verbose_name='Foo Bar',
            description='This is another misconfigured Rendition '
                        'instance.',
            template_string='<h1>{{ title }}</h1>'
        )
        self.assertEqual(
            template_from_string.template.render(
                Context({'title': 'OH HAI!'})
            ),
            '<h1>OH HAI!</h1>'
        )
        self.assertEqual(
            template_from_string.__str__(),
            'Foo Bar'
        )

    def test_exception_invalidrendition(self):
        """Ensure InvalidRendition raises appropriately."""
        def assign_bad_rendition():
            rendition_aware_test_block.child_blocks.get(
                'image'
            ).rendition = 'foo'
        self.assertRaises(
            InvalidRendition,
            assign_bad_rendition
        )

        self.assertRaises(
            InvalidRendition,
            lambda: MultiRenditionStructBlock(
                [('foo', CharBlock())],
                core_renditions=([],)
            )
        )

    def test_renditionawareness(self):
        """
        Test that 'Rendition Aware' blocks render as they should.
        Also tests the 'renditionaware_image_tags' templatetag.
        """
        html = rendition_aware_test_block.render(
            rendition_aware_test_block.to_python({
                'image_lazy': 1,
                'image': 1,
                'render_as': 'foo',
                'image_list': [1, 1, 1]
            })
        )
        self.assertHTMLEqual(
            html,
            """
<div class="image-container">
    <img src="/media/images/test_image.max-100x100.png"/>
</div>
<div class="lazy-image-container">
    <img src="/media/images/test_image.max-100x100.png" width="100"
         height="100" alt="Test Image">
</div>
<div class="in-template-rendition-image-container">
    <img src="/media/images/test_image.max-250x250.png" width="250"
         height="250" alt="Test Image">
</div>"""
        )
        self.assertEqual(
            rendition_aware_test_block.child_blocks.get(
                'image'
            ).rendition.verbose_name,
            'Foo'
        )

    def test_image_chooser_blocks(self):
        """Test the 'Rendition Aware' Image Chooser blocks"""
        x = RenditionAwareLazyLoadImageChooserBlock()
        y = RenditionAwareImageChooserBlock()
        img_model = get_image_model()
        self.assertHTMLEqual(
            x.render_basic(img_model.objects.get(pk=1)),
            '<img class="lazy" data-original="/media/images/test_image.'
            'original.png" width="300" height="300" alt="Test Image"/>'
        )
        self.assertHTMLEqual(
            y.render_basic(img_model.objects.get(pk=1)),
            '<img src="/media/images/test_image.original.png" width="300" '
            'height="300" alt="Test Image">'
        )

    def test_renditionawarestreamblock(self):
        """
        Test streamfield_tools.blocks.RenditionAwareStreamBlock
        """
        test_stream_block = RenditionAwareStreamBlock(
            [('bar', CharBlock()), ('baz', CharBlock())]
        )

        test_rendition = Rendition(
            short_name='foo',
            verbose_name="Foo",
            description="Foo Rendition",
            path_to_template='rendition_aware_struct_block/foo.html'
        )

        test_stream_block.rendition = test_rendition
        html = test_stream_block.render(
            test_stream_block.to_python([
                {'type': 'bar', 'value': 'Bar'},
                {'type': 'baz', 'value': 'Baz'},
            ])
        )
        self.assertHTMLEqual(
            html,
            """
<div class="block-bar">Bar</div>
<div class="block-baz">Baz</div>"""
        )

    def test_multirenditionstructblock(self):
        """Test streamfield_tools.blocks.RenditionAwareStructBlock"""
        missing_template_block = RenditionAwareStructBlock(
            [('bar', CharBlock()), ('baz', CharBlock())],
        )
        self.assertRaises(
            TemplateRequired,
            lambda: missing_template_block.render(
                missing_template_block.to_python({
                    'bar': 'Test Bar',
                    'baz': 'Test Baz'
                })
            )
        )
        test_block = MultiRenditionStructBlock(
            [
                ('foo', CharBlock()),
                (
                    'struct_block', RenditionAwareStructBlock(
                        [('bar', CharBlock()), ('baz', CharBlock())],
                        template='rendition_aware_struct_block/'
                                 'nested_struct_foo.html',
                        template_bar='rendition_aware_struct_block/'
                                     'nested_struct_bar.html'
                    )
                )
            ],
            core_renditions=(
                Rendition(
                    short_name='foo',
                    verbose_name="Foo",
                    description="Foo Rendition",
                    path_to_template='rendition_aware_struct_block/foo.html'
                ),
                Rendition(
                    short_name='bar',
                    verbose_name="Bar",
                    description="Bar Rendition",
                    path_to_template='rendition_aware_struct_block/bar.html'
                ),
            )
        )
        html = test_block.render(
            test_block.to_python({
                'render_as': 'foo',
                'struct_block': {
                    'bar': 'Bar',
                    'baz': 'Baz'

                }
            })
        )
        self.assertHTMLEqual(
            html,
            """
<h1>Foo Template</h1>
<div class="nested-foo">
    <p>Bar</p>
    <p>Baz</p>
</div>
            """
        )
