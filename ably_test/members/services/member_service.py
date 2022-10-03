import datetime
import hashlib

from django.core.exceptions import ObjectDoesNotExist

from members.models import Member, MemberSerializer, TokenSerializer, Token, MemberInfoSerializer
from django.db.models import Q
from rest_framework import exceptions
from mobileauth.models import MobileAuth


class MemberService:
    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def create(self) -> str:
        if self._exists():
            raise exceptions.ValidationError('이미 존재하는 회원정보 입니다.')

        mobile_auth_id = self.request.data.get('mobileAuthId')
        email = self.request.data.get('email')
        nickname = self.request.data.get('nickname')
        password = self.request.data.get('password')
        name = self.request.data.get('name')
        phone = self.request.data.get('phone')

        if None in [mobile_auth_id, email, nickname, password, name, phone]:
            raise exceptions.ValidationError('필수값 누락')

        try:
            mobile_auth = MobileAuth.objects.get(id=mobile_auth_id)
        except ObjectDoesNotExist:
            raise exceptions.ValidationError('존재하지 않는 모바일 인증 아이디입니다.')

        if not mobile_auth.certified:
            raise exceptions.ValidationError('모바일 미인증')

        member_serializer = MemberSerializer(data={
            'email': email,
            'nickname': nickname,
            'password': password,
            'name': name,
            'phone': phone,
        })

        if member_serializer.is_valid():
            member = member_serializer.save()
        else:
            raise exceptions.ValidationError('회원 가입 실패')

        token_serializer = TokenSerializer(data={
            'member': member.id,
            'token': self._get_token(member),
            'regist_at': datetime.datetime.now(),
            'expired_at': datetime.datetime.now() + datetime.timedelta(minutes=5),
        })

        if token_serializer.is_valid():
            token = token_serializer.save()
        else:
            raise exceptions.ValidationError('회원 가입 실패')

        return token.token

    def login(self) -> str:
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        phone = self.request.data.get('phone')

        queryset = Member.objects.filter(Q(email=email) | Q(phone=phone))
        if len(queryset) == 0:
            raise exceptions.ValidationError('일치하는 회원 정보가 없습니다.')

        members = MemberSerializer(queryset, many=True)
        if len(members.data) > 1:
            raise exceptions.ValidationError('비밀번호를 잘못 입력하였습니다.')

        member = Member.objects.get(pk=members.data[0].get('id'))

        if member.password != password:
            raise exceptions.ValidationError('비밀번호를 잘못 입력하였습니다.')

        new_token = self._get_token(member)
        queryset = Token.objects.filter(Q(member_id=member.id))
        tokens = TokenSerializer(queryset, many=True).data
        token = Token.objects.get(pk=tokens[0].get('id'))
        token.token = new_token
        token.expired_at = datetime.datetime.now() + datetime.timedelta(minutes=5)
        token.save()
        return new_token

    def info(self) -> dict:
        pk = self.kwargs.get('pk')
        try:
            member = Member.objects.get(pk=pk)
            member_info = MemberInfoSerializer(member).data
        except ObjectDoesNotExist:
            raise exceptions.ValidationError('존재하지 않는 회원')

        queryset = Token.objects.filter(Q(member_id=member.id))
        tokens = TokenSerializer(queryset, many=True).data
        regist_token = Token.objects.get(pk=tokens[0].get('id')).token
        token = self.request.META.get('HTTP_A_TOKEN')

        if regist_token != token:
            raise exceptions.AuthenticationFailed

        return member_info


    def _get_token(self, member: Member) -> str:
        now = datetime.datetime.now()
        encode_str = f"{member.id}{now}".encode()
        return hashlib.sha256(encode_str).hexdigest()

    def _exists(self) -> bool:
        email = self.request.data.get('email')
        phone = self.request.data.get('phone')

        queryset = Member.objects.filter(Q(email=email) | Q(phone=phone))
        return len(queryset) > 0