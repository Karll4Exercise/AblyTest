from django.db import transaction
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response

from .services.mobileauth_service import MobileAuthService


class MobileAuthViews(viewsets.GenericViewSet):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='이름'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='전화번호'),
            }
        ),
        responses={
            200: openapi.Response(
                description='모바일 인증 생성 요청',
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
                                'mobileAuthId': openapi.Schema(type=openapi.TYPE_STRING, description='모바일 인증 아이디')
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description='모바일 인증 생성 실패',
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
        모바일 인증 요청

        모바일 인증 요청
        """
        return Response({
            'mobileAuthId': MobileAuthService(request, kwargs).create(),
        })

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['authorization_number'],
            properties={
                'authorization_number': openapi.Schema(type=openapi.TYPE_STRING, description='인증번호'),
            }
        ),
        responses={
            200: openapi.Response(
                description='모바일 인증',
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
            403: openapi.Response(
                description='모바일 인증 실패',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'meta': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='결과 코드'),
                            }
                        ),
                    }
                )
            )
        },
    )
    @action(detail=True, methods=['PUT'], url_path='certified')
    @transaction.atomic()
    def certified(self, request, **kwargs):
        """
        모바일 인증

        모바일 인증
        """
        MobileAuthService(request, kwargs).certified()
        return Response()