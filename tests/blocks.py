from streamfield_tools.blocks import (
    Rendition,
    MultiRenditionStructBlock,
    RenditionAwareLazyLoadImageChooserBlock,
    RenditionAwareImageChooserBlock,
    RenditionAwareListBlock
)

rendition_aware_test_block = MultiRenditionStructBlock(
    [
        (
            'image_lazy',
            RenditionAwareLazyLoadImageChooserBlock(
                icon='image',
                label='Lazy Image'
            )
        ),
        (
            'image',
            RenditionAwareImageChooserBlock(
                icon='image',
                label='Image'
            )
        ),
        (
            'image_list',
            RenditionAwareListBlock(
                RenditionAwareImageChooserBlock(
                    icon='image',
                    label='Image'
                )
            )
        )
    ],
    core_renditions=(
        Rendition(
            short_name='foo',
            verbose_name="Foo",
            description="Fooey!",
            path_to_template='rendition_aware_test_block/foo.html',
            image_rendition='max-100x100'
        ),
    ),
    addl_renditions_settings_key='rendition_aware_test_block'
)
