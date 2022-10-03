import random

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from mobileauth.models import MobileAuth, MobileAuthSerializer
from rest_framework import exceptions


class MobileAuthService:
    AUTHORIZATION_TIME = 300

    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def create(self) -> int:
        name = self.request.data.get('name')
        phone = self.request.data.get('phone')

        authorization_number = self._get_random_auth_number()
        mobile_auth_serializer = MobileAuthSerializer(data={
            'name': name,
            'phone': phone,
            'authorization_number': authorization_number,
            'regist_at': timezone.now(),
        })

        if mobile_auth_serializer.is_valid():
            mobile_auth = mobile_auth_serializer.save()
        else:
            raise exceptions.ValidationError('모바일 인증 정보 생성 실패')

        return mobile_auth.pk

    def certified(self) -> int:
        pk = self.kwargs.get('pk')
        authorization_number = self.request.data.get('authorization_number')
        try:
            mobile_auth = MobileAuth.objects.get(id=pk)
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed

        if (timezone.now() - mobile_auth.regist_at).total_seconds() > self.AUTHORIZATION_TIME:
            raise exceptions.AuthenticationFailed

        if mobile_auth.authorization_number != authorization_number:
            raise exceptions.AuthenticationFailed

        mobile_auth.certified = True
        mobile_auth.save(update_fields=['certified'])

        return True

    def _get_random_auth_number(self, max_number: int = 4) -> str:
        result = ""
        for _ in range(max_number):
            result = f"{result}{random.randrange(1, 10)}"

        return result
