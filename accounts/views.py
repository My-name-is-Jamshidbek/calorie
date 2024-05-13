from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from django.shortcuts import redirect


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@require_POST  # This decorator makes sure the view only accepts POST requests
def logout_view(request):
    logout(request)
    return redirect('home')
