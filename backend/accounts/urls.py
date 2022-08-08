from .views import *
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path('list', UserList.as_view(), name='users'),
    path('email', UserEmailFound.as_view(), name='user_email'),
    path('online', OnlineStatusList.as_view(), name='online_status'),
    path('<str:username>', UserDetail.as_view(), name='single_user'),

]
