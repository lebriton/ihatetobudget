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

    # TEMP:
    def test_currency(self):
        template_code = "{{ amount|currency }}"

        for context, expected_rendered_string in [
            (dict(amount=20), "20,00 €"),
            (dict(amount=20.1), "20,10 €"),
            (dict(amount=20.11), "20,11 €"),
            (dict(amount=2000.11), "2 000,11 €"),
            (dict(amount=2000000.11), "2 000 000,11 €"),
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

    @not_implemented
    def test_is_current_month(self):
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

    def test_highlight_text(self):
        template_code = "{{ 'Lorem ipsum'|highlight_text:term }}"

        for context, expected_rendered_string in [
            #  General case
            (
                dict(term="rem"),
                'Lo<span class="text-highlight">rem</span> ipsum',
            ),
            #  Verify case-insensitivity
            (
                dict(term="lo"),
                '<span class="text-highlight">Lo</span>rem ipsum',
            ),
            #  Verify multiple occurrences
            (
                dict(term="m"),
                'Lore<span class="text-highlight">m</span> ipsu<span class="text-highlight">m</span>',  # noqa: E501
            ),
            #  Verify no search term
            (dict(term=""), "Lorem ipsum"),
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
