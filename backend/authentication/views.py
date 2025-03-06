from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
# Create your views here.


class CustomLoginView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("dashboard")


    def get_success_url(self):
        return self.get_success_url()


login_view  = CustomLoginView.as_view()



logout_view = LogoutView.as_view(next_page="login")
