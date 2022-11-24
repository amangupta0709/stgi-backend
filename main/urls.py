from django.urls import path

from main.views import ExecutorAPIView, GeneratorAPIView

urlpatterns = [
    path("generator/", GeneratorAPIView.as_view(), name="generator"),
    path("executor/", ExecutorAPIView.as_view(), name="executor"),
]
