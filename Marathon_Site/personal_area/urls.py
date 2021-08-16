from django.urls import path, include

urlpatterns = [
    path(r'^admin_tools/', include('admin_tools.urls'))
]