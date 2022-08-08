from django.contrib import admin
from django.urls import re_path as url
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path('auth/gettoken/', TokenObtainPairView.as_view(), name='gettoken'),
    path('auth/refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/user/', include('accounts.urls', namespace='accounts')),

    # CodeZen 
    path('api/exams/', include('exams.urls', namespace='exams')),

    # Services 
    # path('api/grouplink/', include('app_grouplink.urls', namespace='groups_link')),

    #Tools
    # path('api/email/', include('emails.urls', namespace='emails')),
    # path('api/calculator/', include('calculator.urls', namespace='calculator')),

    # Forums
    # path('api/forums/', include('forums.urls', namespace='forums')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
