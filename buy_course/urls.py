from django.urls import path, include
from buy_course import views

urlpatterns = [
    path('buy_course/', views.UsersCourseView.as_view()),
    path('buy_course/<int:pk>/', views.UsersCourseView.as_view()),
]
