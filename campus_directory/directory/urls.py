from django.urls import path
from .views import home, search, three_d, search_logs

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('search-logs/', search_logs, name='search_logs'),
    path('3d/', three_d, name='three_d'),
]
