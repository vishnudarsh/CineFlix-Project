from django.urls import path

from .import views

urlpatterns = [

    path('subscription-list/',views.SubscriptionView.as_view(),name='subscription-list')
]