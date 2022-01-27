from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/accounts/', include('account.urls')),
    path('api/', include('quiz.urls')),
]
