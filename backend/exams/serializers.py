from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import *
from accounts.models import *
from accounts.serializers import *
from datetime import datetime, timedelta, timezone
from django.db import transaction






# ### POLL ###
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = [
            "user",
        ]
        read_only_fields = ( 'choice', )

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            'id',
            'question',
            'choice_text',
            'choice_currect',
        ]
        read_only_fields = ('question',)

    def to_representation(self, instance):
        votes = Vote.objects.filter(choice=instance.id)
        response = super().to_representation(instance)
        response['votes'] = VoteSerializer(votes, many=True).data
        return response

class ExamQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    class Meta:
        model = ExamQuestion
        fields = [
            'id', 
            'question_text', 
            'question',
            'user',
            'end_on',
            'status',
            'choices',
        ]

    @transaction.atomic
    def create(self, validated_data):
        choices_data= validated_data.pop('choices')
        question = ExamQuestion.objects.create(**validated_data)

        for choice in choices_data:
            Choice.objects.create(question=question, **choice)
        return question

    def to_representation(self, instance):
        choices = Choice.objects.filter(question=instance.id)
        response = super().to_representation(instance)
        response['user'] = UserAccountSerializer(instance.user, context=self.context).data
        response['total_votes'] = ChoiceSerializer(choices, many=True).data
        return response

        

class ExamCohortSerializer(serializers.ModelSerializer):
    members = UserAccountSerializer(read_only=True, many=True)
    question = ExamQuestionSerializer(read_only=True, many=True)

    class Meta:
        model = ExamCohort
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['total_members'] = instance.members.count()
        response['user'] = UserAccountSerializer(instance.user).data
        return response

