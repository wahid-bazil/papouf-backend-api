from customization.models import CustomPack
from delivery.models import ShippingCity
from django.http import request
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AddressSerializer, CustomUserSerializer, EmailVerificationSerializer, CustomTokenObtainPairSerializer, UserMiniSerializer, UserSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, UserUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AND, AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .models import Address, NewUser, GuestUsers
from .serializers import LoginSerializer, UserHistoriqueSerializer, GuestHistoriqueSerializer

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views, permissions
from django.core.mail import send_mail

import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError, PermissionDenied
from rest_framework import status
from cart.models import *



class AddressDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(Address, user=self.request.user)
        return obj
    serializer_class = AddressSerializer

    def update(self, request, *args, **kwargs):
        user = self.request.user
        address = self.request.data['address']
        city = self.request.data['city']
        city = get_object_or_404(ShippingCity, title=city)
        user_adress, created = Address.objects.get_or_create(user=user)
        user_adress.address = address
        user_adress.city = city
        user_adress.save()
        return Response(status.HTTP_200_OK)


class UserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            obj = get_object_or_404(NewUser, email=self.request.user)
            return obj


class UserMiniDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = NewUser.objects.all()
    serializer_class = UserMiniSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            obj = get_object_or_404(NewUser, email=self.request.user)
            return obj


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = NewUser.objects.get(email=user_data['email'])
            try:
                device_id = str(self.request.headers['deviceid'])
                cart = Cart.objects.filter(device_id=device_id, active=True).first()
                #custompack = CustomPack.objects.filter(device_id=device_id ,isCopy=False , inCart=False).first()
                if cart :
                    cart.user=user
                    #custompack.user=user
                    cart.save()
                    #custompack.save()
                else:
                    Cart.objects.create(user=user)
            except:
                pass

            tokens=get_tokens_for_user(user)
        
            """
                
                token = get_tokens_for_user(user)['access']
                current_site = get_current_site(request).domain
                relativeLink = reverse('email-verify')
                absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
                Subject = 'Bonjour  ' + user.name + '\n' 'Vous venez de vous inscrire sur notre site Papouf. Afin d’activer votre compte veuillez appuyer sur le lien suivant. \n'+ absurl
                
                send_mail('Papouf', Subject, 'bazil.wahid1@gmail.com',[user_data['email']], fail_silently=False)
                """
            return Response(tokens, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):

    def get(self, request):
        token = request.GET.get('token')

        payload = jwt.decode(token, settings.SECRET_KEY)
        user = NewUser.objects.get(id=payload['user_id'])
        try:
            if not user.active:
                user.active = True
                user.save()
                return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activastion Expired'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if NewUser.objects.filter(email=email).exists():
            user = NewUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            absurl = 'https://frontendpapouf.herokuapp.com/Change_Password' + \
                "?token="+str(token) + "&uidb64="+str(uidb64)
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            send_mail('Papouf', email_body, 'bazil.wahid1@gmail.com',
                      [user.email], fail_silently=False)

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = NewUser.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': 'Token in not valid'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Success': True, 'message': 'crendentials valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class UserGuestHistorique(generics.RetrieveAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = NewUser.objects.all()
            return queryset
        else:
            queryset = GuestUsers.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return UserHistoriqueSerializer
        else:
            return GuestHistoriqueSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            print(self.request.user)
            obj = get_object_or_404(NewUser, email=self.request.user)

        else:
            try:
                device_id = str(self.request.COOKIES['device_id'])
            except:
                raise NotFound({"detail": "user not found"})

            obj, created = GuestUsers.objects.get_or_create(
                device_id=device_id)

        return obj


"""class UserGuestHistorique(generics.RetrieveAPIView):
    queryset = GuestUsers.objects.all()
    serializer_class =GuestHistoriqueSerializer    
    def get_object(self):
        try:
                device_id = str(self.request.COOKIES['device_id'])  
        except:
                raise NotFound({"detail":"user not found"})
           

        obj=get_object_or_404(GuestUsers,pk=device_id)
        return obj
    
"""
