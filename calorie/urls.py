from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),  # your application's urls
    path('', include('pages.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
