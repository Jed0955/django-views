from django_views.views import Generic

class Login(Generic):
    template_name = 'login.html'

    def get_context_data(*args, **kwargs):
        return {}

login = Login.as_view()