from django.urls import path
from .views import SSCMarksheetVerification

urlpatterns = [
    path('ssc/', SSCMarksheetVerification.as_view(), name='ssc-verification'),
]
