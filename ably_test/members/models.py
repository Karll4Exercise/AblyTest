from django.db import models
from rest_framework import serializers


class Member(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    email = models.CharField(db_column='email', unique=True, max_length=50)
    nickname = models.CharField(db_column='nickname', max_length=20)
    password = models.CharField(db_column='password', max_length=300)
    name = models.CharField(db_column='name', max_length=30)
    phone = models.CharField(db_column='phone', max_length=20)
    regist_at = models.DateTimeField(db_column='regist_at', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'member'


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class Token(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    member = models.ForeignKey(Member, models.DO_NOTHING)
    token = models.CharField(db_column='token', max_length=500)
    expired_at = models.DateTimeField(db_column='expired_at')
    regist_at = models.DateTimeField(db_column='regist_at', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'token'


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'

