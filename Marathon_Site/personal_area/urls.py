from django.urls import path, include

urlpatterns = [
    path('admin_tools/', include('admin_tools.urls'))
]