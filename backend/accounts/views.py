from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import permissions
from datetime import datetime, timedelta, timezone
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

time_threshold = datetime.now(timezone.utc) - timedelta(minutes = 5)

class UserAccountFilter(FilterSet):
    username = filters.CharFilter('username')
    email = filters.CharFilter('email')
    active = filters.CharFilter('is_active')
    
    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'is_active')


class UserList(generics.ListAPIView):
    queryset = UserAccount.objects.order_by('-created_on')
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserAccountSerializer
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_class= UserAccountFilter
    ordering_fields = ('created_on', 'updated_on') 
    search_fields = ('username', )

class UserDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserAccountSerializer
    lookup_field = ['username']

    def retrieve(self, request, username):
        queryset = UserAccount.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializers = UserAccountSerializer(user, context={"request": request})
        return Response(serializers.data)


class UserEmailFound(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        posted_data = self.request.data
        get_email = posted_data['email']
        queryset = UserAccount.objects.all()
        user = get_object_or_404(queryset, email=get_email)
        serializers = UserAccountSerializer(user, context={"request": request})        
        return Response(status=200, data=serializers.data)



# EMAIL VERIFICATION PAGINATION # 
class OnlineStatusPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'records'
    max_page_size = 15

    def get_paginated_response(self, data):
        return Response({
            'total': OnlineStatus.objects.filter(updated_on__gt= time_threshold).count(),
            'members': OnlineStatus.objects.filter(updated_on__gt= time_threshold, is_member = True).count(),
            'guests': OnlineStatus.objects.filter(updated_on__gt= time_threshold, is_member = False).count(),
            'results': data,
        })


class OnlineStatusList(generics.ListAPIView):
    queryset = OnlineStatus.objects.filter(updated_on__gt= time_threshold)
    permission_classes = (permissions.AllowAny, )
    serializer_class = OnlineStatusSerializer
    pagination_class = OnlineStatusPagination

    def post(self, request, format=None):
        queryset = OnlineStatus.objects.filter(updated_on__gt= time_threshold)
        serializer = OnlineStatusSerializer(data=request.data)
        user_ip = self.get_ip()
        results = queryset.filter(Q(ip__icontains=user_ip))
        if serializer.is_valid():
            if len(results)== 1:
                status_Ip = get_object_or_404(queryset, ip=user_ip)
                status_serializer = OnlineStatusSerializer(status_Ip, data=request.data)
                if status_serializer.is_valid():
                    status_serializer.save(ip=self.get_ip())
                print("Exist User")
            elif len(results)> 1:
                status_Ip = get_object_or_404(queryset, ip=user_ip)
                status_serializer = OnlineStatusSerializer(status_Ip, data=request.data)
                if status_serializer.is_valid():
                    status_serializer.save(ip=self.get_ip())
                print("User Exist more...")
            else: 
                serializer.save(ip=self.get_ip())
                print("New Unique User Added")  
            OnlineStatus.objects.exclude(updated_on__gt= time_threshold).delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ### For Ip Address ### 
    def get_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR',None)
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR',None)
        return ip