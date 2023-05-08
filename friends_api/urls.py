from django.contrib import admin
from django.urls import path, include
from .views import get_api_docs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('friends.urls')),
    path('api/', get_api_docs, name='docs'),
]
