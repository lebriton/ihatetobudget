import datetime

from django.test import TestCase

from ihatetobudget.tests import not_implemented

from ..models import Expense
from ..views import ExpenseDeleteView


class IndexTestCase(TestCase):
    #  TODO: also test context:
    # - `monthly_average_spend`
    # - `median_spend`
    # - `monthly_insights_dict`
    pass


class SheetViewTestCase(TestCase):
    @not_implemented
    def test_get_context_data(self):
        pass


class ExpenseCreateViewTestCase(TestCase):
    pass


class ExpenseUpdateViewTestCase(TestCase):
    pass


class ExpenseDeleteViewTestCase(TestCase):
    def test_get_success_url(self):
        # Single expense
        expense1 = Expense(
            date=datetime.date(2010, 1, 1), description="Lorem ispum", amount=20
        )
        expense1.save()
        view = ExpenseDeleteView(object=expense1)
        self.assertEqual(view.get_success_url(), view.success_url)

        # Two expenses, same month
        expense2 = Expense(
            date=datetime.date(2010, 2, 1), description="Lorem ispum", amount=20
        )
        expense2.save()
        expense3 = Expense(
            date=datetime.date(2010, 2, 2), description="Lorem ispum", amount=20
        )
        expense3.save()
        view = ExpenseDeleteView(object=expense2)
        self.assertEqual(view.get_success_url(), expense3.get_absolute_url())

        # Two expenses, different months
        expense4 = Expense(
            date=datetime.date(2010, 3, 1), description="Lorem ispum", amount=20
        )
        expense4.save()
        expense5 = Expense(
            date=datetime.date(2010, 4, 1), description="Lorem ispum", amount=20
        )
        expense5.save()
        view = ExpenseDeleteView(object=expense4)
        self.assertEqual(view.get_success_url(), view.success_url)


class ExpenseListViewTestCase(TestCase):
    @not_implemented
    def test_get_queryset(self):
        pass


class CategoryListViewTestCase(TestCase):
    pass


class CategoryCreateViewTestCase(TestCase):
    pass


class CategoryUpdateViewTestCase(TestCase):
    pass


class CategoryDeleteViewTestCase(TestCase):
    pass
