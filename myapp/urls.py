# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),  # login_view는 실제 뷰 함수의 이름에 따라 변경
    path("signup/", views.signup_view, name="signup"),  # signup_view도 실제 뷰 함수의 이름에 따라 변경
]
