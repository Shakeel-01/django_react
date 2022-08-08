from django.urls import path
from .views import *

app_name="exams"

urlpatterns = [
    path('posts', ExamCohortListView.as_view()),
    path('posts/<examID>', ExamCohortDetail.as_view()),
    path('posts/<examID>/edit', ExamCohortEditView.as_view()),
    path('posts/<examID>/delete', ExamCohortDeleteView.as_view()),

    # Questions
    path('question', ExamQuestionListView.as_view()),
    path('question/<int:id>', ExamQuestionDetail.as_view()),

    # path('posts/<examID>', ExamCohortDetail.as_view()),
    # path('posts/<examID>/edit', ExamCohortEditView.as_view()),
    # path('posts/<examID>/delete', ExamCohortDeleteView.as_view()),
]
