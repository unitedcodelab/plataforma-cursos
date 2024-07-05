from django.contrib import admin
from django.urls import path, include
from .settings import DEBUG, PRODUCTION

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('apps.core.urls')),
    path('autenticacao/', include('apps.authentication.urls')),
    path('cursos/', include('apps.courses.urls')),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if True:
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)