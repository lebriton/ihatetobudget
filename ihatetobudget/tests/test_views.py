from django.test import TestCase

from . import TestLoginRequiredMixin, WithUserMixin


class IndexTestCase(TestLoginRequiredMixin, WithUserMixin, TestCase):
    pass
