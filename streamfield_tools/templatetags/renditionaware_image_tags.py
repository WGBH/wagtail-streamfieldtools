from django import template

from wagtail.wagtailimages.templatetags.wagtailimages_tags import (
    ImageNode
)

register = template.Library()


@register.tag(name="image")
def image(parser, token):
    bits = token.split_contents()[1:]
    image_expr = parser.compile_filter(bits[0])
    filter_spec = bits[1]
    bits = bits[2:]

    if len(bits) == 2 and bits[0] == 'as':
        # token is of the form {% image self.photo max-320x200 as img %}
        return VariableOrStringLiteralImageNode(
            image_expr,
            filter_spec,
            output_var_name=bits[1]
        )
    else:
        # token is of the form {% image self.photo max-320x200 %} - all additional tokens
        # should be kwargs, which become attributes
        attrs = {}
        for bit in bits:
            try:
                name, value = bit.split('=')
            except ValueError:
                raise template.TemplateSyntaxError(
                    "'image' tag should be of the form {% image self.photo "
                    "max-320x200 [ custom-attr=\"value\" ... ] %} or "
                    "{% image self.photo max-320x200 as img %}"
                )
            # setup to resolve context variables as value
            attrs[name] = parser.compile_filter(value)

        return VariableOrStringLiteralImageNode(
            image_expr,
            filter_spec,
            attrs=attrs
        )


class VariableOrStringLiteralImageNode(ImageNode):

    def __init__(self, image_expr, filter_spec, output_var_name=None,
                 attrs={}):
        self.image_expr = image_expr
        self.output_var_name = output_var_name
        self.attrs = attrs
        self.filter_spec_raw = filter_spec
        self.filter_spec_as_var = template.Variable(filter_spec)

    def render(self, context):
        try:
            filter_spec = self.filter_spec_as_var.resolve(context)
        except template.VariableDoesNotExist:
            filter_spec = self.filter_spec_raw
        finally:
            self.filter_spec = filter_spec

        return super(VariableOrStringLiteralImageNode, self).render(context)
