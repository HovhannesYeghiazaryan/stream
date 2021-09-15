from django.urls import path
from k8s_app.views import BaseView, StatusView


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('status/', StatusView.as_view(), name='status')
]
