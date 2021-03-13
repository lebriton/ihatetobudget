from django.contrib import messages
from django.utils.safestring import mark_safe

from ..templatetags.ihatetobudget_extras import override_query_dict


# XXX: What a monstrous name!
class InitialDataAsGETOptionsMixin:
    def get_initial(self):
        initial = super().get_initial()

        for (
            option_name,
            interpret_option_value,
        ) in self.fields_with_initial_data_as_get_option.items():
            if option_value := self.request.GET.get(option_name):
                if interpret_option_value is None:
                    initial[option_name] = option_value
                else:
                    try:
                        initial[option_name] = interpret_option_value(
                            option_value
                        )
                    except Exception:
                        #  XXX: log this?
                        pass
        return initial


class SuccessMessageOnDeleteViewMixin:
    def delete(self, request, *args, **kwargs):
        #  XXX: SuccessMessageMixin not working with DeleteView
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class SortableListViewMixin:
    def get_ordering(self):
        ordering = self.request.GET.get("order")
        sortable_fields = self.sortable_fields
        if ordering in sortable_fields + ["-" + f for f in sortable_fields]:
            return ordering
        return super().get_ordering()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sortable_fields_dict"] = sortable_fields_dict = {}
        for field in self.sortable_fields:
            ordering = self.get_ordering()
            if isinstance(ordering, list):
                ordering = ordering[0]
            #  XXX: this f-string is awful
            #  Note: `parameters` is extracted from the f-string because of E501
            parameters = override_query_dict(
                self.request.GET,
                "order=" + ("-" + field if ordering == field else field),
            )
            sortable_fields_dict[field] = mark_safe(
                f"""
                <a href="?{parameters}">
                    {field.title()}
                    {
                        {
                            field: '<i class="fa fa-sort-up"></i>',
                            '-' + field: '<i class="fa fa-sort-down"></i>'
                        }.get(ordering, '')
                    }
                </a>
            """
            )
        return context
