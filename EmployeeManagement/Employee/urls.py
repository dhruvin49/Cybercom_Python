from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import EmployeeProfileView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('profile2/', EmployeeProfileView.as_view(), name='employee_profile'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)