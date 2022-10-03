from django.db import models
from rest_framework import serializers


class MobileAuth(models.Model):
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=30)
    phone = models.CharField(db_column='phone', max_length=20)
    authorization_number = models.CharField(db_column='authorization_number', max_length=4)
    certified = models.BooleanField(db_column='certified', default=False)
    regist_at = models.DateTimeField(db_column='regist_at', auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'mobile_auth'


class MobileAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileAuth
        fields = '__all__'
