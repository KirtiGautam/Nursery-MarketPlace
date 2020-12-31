from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signup/nursery/', views.nurserySignup, name="signup"),
    path('login/', views.login, name="signup"),
]
