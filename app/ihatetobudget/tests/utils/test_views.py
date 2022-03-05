from django.http import QueryDict
from django.test import TestCase
from django.views.generic import ListView
from django.views.generic.edit import FormView

from ihatetobudget.utils.views import (
    InitialDataAsGETOptionsMixin,
    SortableListViewMixin,
)

from .. import not_implemented


class InitialDataAsGETOptionsMixinTestCase(TestCase):
    #  XXX: `FormView` is probably deep enough MRO
    class DummyView(InitialDataAsGETOptionsMixin, FormView):
        fields_with_initial_data_as_get_option = {
            "foo": None,
            "bar": lambda option_value: option_value.upper(),
        }

    def test_mixin(self):
        dummy_view = self.DummyView()

        #  XXX: hack to create a query dict on the fly
        dummy_view.request = request = lambda: None

        for query_string, expected in [
            ("", {}),
            ("baz=eggs", {}),
            ("foo=spam", {"foo": "spam"}),
            ("bar=ham", {"bar": "HAM"}),
        ]:
            with self.subTest(query_string=query_string, expected=expected):
                request.GET = QueryDict(query_string)
                self.assertEqual(expected, dummy_view.get_initial())


class SuccessMessageOnDeleteViewMixinTestCase(TestCase):
    @not_implemented
    def test_mixin(self):
        pass


class SortableListViewMixinTestCase(TestCase):
    class DummyView(SortableListViewMixin, ListView):
        sortable_fields = ["foo"]

    def test_mixin(self):
        dummy_view = self.DummyView()

        #  XXX: hack to create a query dict on the fly
        dummy_view.request = request = lambda: None
        #  XXX: hack
        dummy_view.object_list = []

        for query_string, expected_order, expected_href in [
            ("", None, "?order=foo"),
            ("order=foo", "foo", "?order=-foo"),
            ("order=-foo", "-foo", "?order=foo"),
            ("order=bar", None, "?order=foo"),
        ]:
            with self.subTest(
                query_string=query_string,
                expected_order=expected_order,
                expected_href=expected_href,
            ):
                request.GET = QueryDict(query_string)

                self.assertEqual(dummy_view.get_ordering(), expected_order)
                #  XXX: this is good enough
                self.assertIn(
                    expected_href,
                    dummy_view.get_context_data()["sortable_fields_dict"][
                        "foo"
                    ],
                )
