from django.shortcuts import render, redirect
from datetime import date
from django.views.generic import TemplateView
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


class EmployeeProfileView(TemplateView):
    template_name = 'employee_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the logged in employee
        employee = Employee.objects.get(user=self.request.user)
        # Get holidays for the current year
        current_year = date.today().year
        holidays = Holiday.objects.filter(year=current_year)
        # Add context data
        context['employee'] = employee
        context['holidays'] = holidays
        context['years'] = range(current_year - 1, current_year + 1)
        context['current_year'] = current_year
        return context
    


def login(request):

    if request.method == 'POST':
        emp = Employee.objects.all()
        holidays = Holiday.objects.all()



        username = request.POST['username']
        password = request.POST['password']
        for i in range(len(emp)):
            if emp[i].username == username and emp[i].password == password:
                user = Employee.objects.filter(username=emp[i].username)
                return render(request, 'profile.html', {'authUser':user})
            else:
                return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    
    else:
        return render(request, 'login.html')


@login_required
def profile(request):
    
    return render(request, 'profile.html')
    



