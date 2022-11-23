from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError as coreValidationError
from rest_framework import status
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from agent.models import User
from authentication.serializers import MyTokenObtainPairSerializer, ChangePasswordSerializer, RegisterSerializer
from quiz_app.cons import ERROR_TYPE, VALIDATION_ERROR, ERRORS, MESSAGE, OTHER, FIELD_ERROR


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as to:
            raise InvalidToken(to.args[0])
        except ValidationError as ve:
            return Response(
                {ERROR_TYPE: VALIDATION_ERROR, ERRORS: ve.get_full_details(), MESSAGE: 'Wrong Credentials!'},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({ERROR_TYPE: OTHER, ERRORS: '{}'.format(e), MESSAGE: 'Wrong Credentials!'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    """
    API to change user's password.
    """
    serializer_class = ChangePasswordSerializer
    model = User

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({
                    ERROR_TYPE: FIELD_ERROR,
                    ERRORS: {'old_password': [{'message': 'The old password is wrong.'}]},
                    MESSAGE: 'The old password is wrong.'
                }, status=status.HTTP_400_BAD_REQUEST)

            new_password = serializer.data.get("new_password")
            try:
                password_validation.validate_password(password=new_password, user=User)

            except coreValidationError as ve:
                return Response({
                    ERROR_TYPE: FIELD_ERROR,
                    ERRORS: {'new_password': [{'message': ve.messages[0]}]},
                    MESSAGE: ve.messages[0]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({MESSAGE: 'Your password was changed successfully.'}, status=status.HTTP_200_OK)

        return Response({
            ERROR_TYPE: OTHER,
            ERRORS: serializer.errors,
            MESSAGE: 'Internal problem.'
        }, status=status.HTTP_400_BAD_REQUEST)


class Register(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
