from accounts.models import *
from django.template.defaultfilters import slugify
from django.db import models
import uuid

class ModalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).order_by('-created_on')



class ExamCohort(models.Model):
    user        = models.ForeignKey(UserAccount, related_name="Author", on_delete=models.CASCADE)
    title       = models.CharField(max_length=50)
    examID      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members     = models.ManyToManyField(UserAccount, blank=True, null=True)
    is_published= models.BooleanField(default=False)
    created_on  = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects         = models.Manager()  # The default manager.
    posts            = ModalManager()  # The Dahl-specific manager.

    class Meta:
        verbose_name_plural = "Exam Cohort"

    def __str__(self):
        return self.title


### POLL REQUEST ###
class ExamQuestion(models.Model):
    QUESTION_STATUS = [ ('published', 'Published'), ('draft', 'Draft'), ]

    question_text = models.CharField(max_length=10000)
    question      = models.ForeignKey(ExamCohort, related_name="question", on_delete=models.DO_NOTHING)
    user          = models.ForeignKey(UserAccount, related_name="question_creator", on_delete=models.DO_NOTHING)
    status        = models.CharField(choices=QUESTION_STATUS, default='draft', max_length=10)
    end_on        = models.PositiveIntegerField(default=2)
    created_on    = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_on    = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects       = models.Manager()  # The default manager.
    posts         = ModalManager()  # The Dahl-specific manager.

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question      = models.ForeignKey(ExamQuestion, related_name="choices", on_delete=models.CASCADE)
    choice_text   = models.CharField(max_length=200)
    choice_currect= models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

    @property
    def choices(self):
        return self.choice_set.all()


class Vote(models.Model):
    choice        = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user          = models.ForeignKey(UserAccount, related_name="voter", on_delete=models.DO_NOTHING)
    created_on    = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_on    = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.user.username

