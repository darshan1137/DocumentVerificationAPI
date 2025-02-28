from django.urls import path
from .views import SSCMarksheetVerification
from .views import CETMarksheetVerification

urlpatterns = [
    path('ssc/', SSCMarksheetVerification.as_view(), name='ssc-verification'),
    path('cet/', CETMarksheetVerification.as_view(), name='cet-verification'),
]
