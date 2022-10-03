from django.db import transaction
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response

from .services.member_service import MemberService


class MemberViews(viewsets.GenericViewSet):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mobileAuthId', 'email', 'nickname', 'password', 'name', 'phone'],
            properties={
                'mobileAuthId': openapi.Schema(type=openapi.TYPE_INTEGER, description='모바일 인증 아이디'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='이메일'),
                'nickname': openapi.Schema(type=openapi.TYPE_STRING, description='닉네임'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='이름'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='전화번호'),
            }
        ),
        responses={
            200: openapi.Response(
                description='회원 가입 완료',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'meta': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='결과 코드')
                            }
                        ),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'token': openapi.Schema(type=openapi.TYPE_STRING, description='토큰')
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description='회원 가입 실패',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'meta': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='결과 코드'),
                                'message': openapi.Schema(type=openapi.TYPE_STRING, description='실패 사유')
                            }
                        ),
                    }
                )
            )
        },
    )
    @transaction.atomic()
    def create(self, request, **kwargs):
        """
        회원 가입

        회원 가입
        """
        return Response({
            'Token': MemberService(request, kwargs).create(),
        })

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='이메일'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='전화번호'),
            }
        ),
        responses={
            200: openapi.Response(
                description='로그인 완료',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'meta': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='결과 코드')
                            }
                        ),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'token': openapi.Schema(type=openapi.TYPE_STRING, description='토큰')
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description='로그인 실패',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'meta': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='결과 코드'),
                                'message': openapi.Schema(type=openapi.TYPE_STRING, description='실패 사유')
                            }
                        ),
                    }
                )
            )
        },
    )
    @transaction.atomic()
    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request, **kwargs):
        """
        로그인

        로그인
        """
        return Response({
            'Token': MemberService(request, kwargs).login(),
        })

    def retrieve(self, request, **kwargs):
        """
        정보 보기

        정보 보기
        """
        return Response(MemberService(request, kwargs).info())

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mobileAuthId', 'password', 'phone'],
            properties={
                'mobileAuthId': openapi.Schema(type=openapi.TYPE_INTEGER, description='모바일 인증 아이디'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='전화번호'),
            }
        ),
        responses={
            200: openapi.Response(
                description='비밀번호 재설정 완료',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'meta': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='결과 코드')
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description='비밀번호 재설정 실패',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'meta': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='결과 코드'),
                                'message': openapi.Schema(type=openapi.TYPE_STRING, description='실패 사유')
                            }
                        ),
                    }
                )
            )
        },
    )
    @transaction.atomic()
    @action(detail=True, methods=['PUT'], url_path='password-reset')
    def password_reset(self, request, **kwargs):
        MemberService(request, kwargs).password_reset()
        return Response()