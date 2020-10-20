from django.http import QueryDict
from django.template import Context, Template
from django.test import TestCase

from . import not_implemented


#  ihatetobudget_extras.py
class ExtrasTestCase(TestCase):
    def assertRenderedCorrectly(
        self, template_code, context, expected_expected_rendered_string
    ):
        self.assertEqual(
            Template("{% load ihatetobudget_extras %}" + template_code).render(
                Context(context)
            ),
            expected_expected_rendered_string,
        )

    @not_implemented
    def test_order_queryset_by(self):
        pass

    def test_attrsum(self):
        class SomeObject:
            bar = 2

        self.assertRenderedCorrectly(
            "{{ foo|attrsum:'bar' }}",
            dict(foo=[SomeObject() for _ in range(10)]),
            "20",
        )

    def test_currency(self):
        template_code = "{{ amount|currency }}"

        for context, expected_rendered_string in [
            (dict(amount=20), "20€"),
            (dict(amount="20"), "20€"),
            (dict(amount="20.00"), "20,00€"),
        ]:
            with self.subTest(
                context=context,
                expected_rendered_string=expected_rendered_string,
            ):
                self.assertRenderedCorrectly(
                    template_code,
                    context,
                    expected_rendered_string,
                )

    def test_setvar(self):
        self.assertRenderedCorrectly(
            """
{% setvar "foobarbaz" as x %}
{{ x }}
{% setvar x|add:'spamhameggs' as x %}
{{ x }}
            """,
            {},
            """

foobarbaz

foobarbazspamhameggs
            """,
        )

    @not_implemented
    def test_is_future_date(self):
        pass

    def test_override_query_dict(self):
        template_code = "{{ query|override_query_dict:parameters }}"
        query = QueryDict("foo=spam&bar=ham")

        for context, expected_rendered_string in [
            #  No override
            (dict(query=query, parameters=""), "foo=spam&amp;bar=ham"),
            #  Override one
            (
                dict(query=query, parameters="foo=example"),
                "foo=example&amp;bar=ham",
            ),
            #  Append one
            (
                dict(query=query, parameters="baz=eggs"),
                "foo=spam&amp;bar=ham&amp;baz=eggs",
            ),
        ]:
            with self.subTest(
                context=context,
                expected_rendered_string=expected_rendered_string,
            ):
                self.assertRenderedCorrectly(
                    template_code,
                    context,
                    expected_rendered_string,
                )
