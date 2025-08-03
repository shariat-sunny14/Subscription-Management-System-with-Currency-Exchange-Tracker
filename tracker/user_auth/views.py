from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import login
from currency_exchange_tracker.models import Subscription
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user

        # Check if user has an active subscription
        subscription = Subscription.objects.filter(user=user, end_date__gte=date.today()).first()

        if subscription:
            return '/currency-exchange/exchange_rate/'  # URL to your exchange rate view
        else:
            return '/currency-exchange/subscribe/'  # If no valid subscription, redirect to subscribe
        
class CustomLogoutView(LogoutView):
    next_page = 'login'