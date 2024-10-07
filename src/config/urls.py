from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('apps.books.urls', namespace='home')),
    path('reader/', include('apps.reader.urls', namespace='reader')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



admin.site.site_header = "BookReader Admin"
admin.site.site_title = "BookReader Admin Portal"
admin.site.index_title = "Welcome to BookReader Admin Portal"