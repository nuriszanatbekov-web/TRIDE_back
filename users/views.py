from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

from .serializers import (
    RegisterStep1Serializer,
    VerifyEmailSerializer,
    ResendCodeSerializer,  # ← кошулду
    RegisterStep2Serializer,
    LoginSerializer,
    UserProfileSerializer,
)
from .utils import send_verification_email, verify_code

User = get_user_model()


@extend_schema(
    summary='1-кадам: Катталуу',
    description='Аты, фамилиясы, туулган күнү, жынысы, email киргизилет. Email\'га тастыктоо коду жөнөтүлөт.',
    tags=['Катталуу'],
    request=RegisterStep1Serializer,
)
class RegisterStep1View(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterStep1Serializer

    def post(self, request):
        serializer = RegisterStep1Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user, _ = User.objects.get_or_create(email=data['email'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.date_of_birth = data['date_of_birth']
        user.gender = data['gender']
        user.is_active = False
        user.is_email_verified = False
        user.save()

        send_verification_email(user)

        return Response(
            {'message': f'{data["email"]} emailине код жөнөтүлдү!'},
            status=status.HTTP_200_OK
        )


@extend_schema(
    summary='Email тастыктоо',
    description='Email\'га келген 6 орундуу кодду киргизип, emailди тастыктайт.',
    tags=['Катталуу'],
    request=VerifyEmailSerializer,
)
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        is_valid, user = verify_code(data['email'], data['code'])

        if not is_valid:
            return Response(
                {'error': 'Код туура эмес же мөөнөтү өттү!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_email_verified = True
        user.save()

        return Response(
            {'message': 'Email тастыкталды! 2-кадамга өтүңүз.'},
            status=status.HTTP_200_OK
        )


@extend_schema(
    summary='Кодду кайра жөнөтүү',
    description='Эгер код келбесе же мөөнөтү өтсө, email\'га жаңы код жөнөтөт.',
    tags=['Катталуу'],
    request=ResendCodeSerializer,  # ← кошулду
)
class ResendCodeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendCodeSerializer  # ← кошулду

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email киргизиңиз!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email, is_email_verified=False)
            send_verification_email(user)
            return Response({'message': 'Код кайра жөнөтүлдү!'})
        except User.DoesNotExist:
            return Response(
                {'error': 'Колдонуучу табылган жок!'},
                status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    summary='2-кадам: Катталуу',
    description='Салмак (кг), бой (см) жана сырсөз киргизилет. Аккаунт активдештирилип, JWT токен берилет.',
    tags=['Катталуу'],
    request=RegisterStep2Serializer,
)
class RegisterStep2View(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterStep2Serializer

    def post(self, request):
        serializer = RegisterStep2Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(email=data['email'], is_email_verified=True)
        except User.DoesNotExist:
            return Response(
                {'error': 'Алгач emailди тастыктаңыз!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.weight = data['weight']
        user.height = data['height']
        user.set_password(data['password'])
        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Каттоо ийгиликтүү! 🎉',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    summary='Кириш',
    description='Email жана сырсөз менен кирүү. Ийгиликтүү болсо JWT access жана refresh токен кайтарат.',
    tags=['Кириш'],
    request=LoginSerializer,
)
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response(
                {'error': 'Email же сырсөз туура эмес!'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(data['password']):
            return Response(
                {'error': 'Email же сырсөз туура эмес!'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Аккаунтту активдештириңиз!'},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)


@extend_schema(
    summary='Профиль',
    description='GET — профилди көрүү. PATCH — профилдеги маалыматтарды өзгөртүү. Token керек!',
    tags=['Профиль'],
)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)