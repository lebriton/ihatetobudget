from django.views.generic.edit import FormView


# XXX: What a monstrous name!
class InitialDataAsGETOptionsMixin(FormView):
    def get_initial(self):
        initial = super().get_initial()

        for (
            option_name,
            interpret_option_value,
        ) in self.fields_with_initial_data_as_get_option:
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
