from django.contrib import admin
from django.urls import path,include
from social_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('social_app.urls')),
    path('accounts/',include('accounts.urls')),
    path('',views.home,name='home')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

