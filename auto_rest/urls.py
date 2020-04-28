#from django.contrib import admin
from django.urls import path, include
from autoapi.core import RouterFactory


router = RouterFactory().get_default_router()

urlpatterns = [
    path('', include('autoapi.urls')),
]

urlpatterns += [
    path(r'api/', include((router.urls, 'api'))),
]
