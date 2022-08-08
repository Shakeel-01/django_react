from rest_framework import generics
from rest_framework import permissions
from .models import *
from .serializers import *
from accounts.pagination import *
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
from rest_framework.generics import get_object_or_404

    # LIST API VIEWS 
class ExamCohortListView(generics.ListCreateAPIView):
    queryset = ExamCohort.objects.all().order_by('-created_on')
    permission_classes = (permissions.AllowAny, )
    serializer_class = ExamCohortSerializer
    lookup_field = 'examID'
    ordering_fields = ('created_on', 'updated_on') 
    search_fields = ('title', )
    pagination_class = StandardResultsSetPagination
    
# FORUM POST DETAILS
class ExamCohortDetail(generics.RetrieveAPIView):
    queryset = ExamCohort.objects.all()
    serializer_class = ExamCohortSerializer
    lookup_field = 'examID'
    permission_classes = (permissions.AllowAny, )


    # REMOVE GROUP LINK 
class ExamCohortDeleteView(generics.RetrieveDestroyAPIView):
    queryset = ExamCohort.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExamCohortSerializer

    # EDIT POST
class ExamCohortEditView(generics.UpdateAPIView):
    queryset = ExamCohort.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExamCohortSerializer




    # LIST EXAM QUESTION 
class ExamQuestionListView(generics.ListCreateAPIView):
    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializer
    lookup_field = 'id'
    permission_classes = (permissions.AllowAny, )
    pagination_class = StandardResultsSetPagination

class ExamQuestionDetail(generics.RetrieveAPIView):
    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializer
    lookup_field = 'id'
    permission_classes = (permissions.AllowAny, )

# Post Search
class ExamQuestionDetail(generics.RetrieveAPIView):
    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializer
    lookup_field = 'id'
    permission_classes = (permissions.AllowAny, )

# Post Search
class ExamQuestionChoiceListView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = ChoiceSerializer
    pagination_class = SmallResultsSetPagination
