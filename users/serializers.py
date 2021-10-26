
from delivery.models import ShippingCity
from django.shortcuts import get_object_or_404
from delivery.serializers import ShippingCitySerializer
from re import T
from django.db import models
from django.db.models import fields, manager
from rest_framework import serializers
from users.models import Address, NewUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from customization.models import CustomPack
from cart.models import Cart
from .models import GuestUsers ,RegistrationConfig
from .mixins import UserNumbers

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class CustomUserSerializer(serializers.ModelSerializer):
    token =serializers.SerializerMethodField()
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True )
    password = serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model = NewUser
        fields = ('email', 'name','phone_number', 'password' , 'token')
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_token(self,obj):
        tokens=get_tokens_for_user(obj)
        return tokens


    def create(self, validated_data):
        device_id = validated_data.pop('device_id', None)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if NewUser.objects.filter(email=validated_data.pop('email',None)):
            raise serializers.ValidationError({'email':'This email is elready exited'})
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = NewUser
        fields = ['token']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        
        data.update({'id': self.user.id})
     
        return data


class LoginSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    class Meta:
        model = NewUser
        fields = ['email', 'password','tokens']
    def get_tokens(self, obj):
            user = NewUser.objects.get(email=obj['email'])
            return {
                'refresh': user.tokens()['refresh'],
                'access': user.tokens()['access']
            }
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({'detail':'Invalid credentzzials, try again'})
        if not user.is_email_verified and not user.verification_overridden:
            settings = RegistrationConfig.objects.get(is_active=True)
            if settings.is_email_confirmation:
                raise serializers.ValidationError({'detail':"your email is not active "})
        return super().validate(attrs)     


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = NewUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)



class AddressSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=30)
    class Meta  :
        model = Address
        fields = ['city' ,'details']

class UserContactSerializer(serializers.ModelSerializer):
    address_details =AddressSerializer(required = False)
    name = serializers.CharField(required = False , max_length=30 , min_length=2)
    class Meta:
        model = NewUser
        fields = ['phone_number','address_details' ,'name']
    def update(self, instance, validated_data):
        if validated_data.get('address_details',None) :
            address_details = validated_data.get('address_details')
            city = address_details['city']
            try :
                print(city)
                city =ShippingCity.objects.get(slug=city )
                print(city)
            except :
                raise NotFound(detail='This city is not in our delivery list')
            details =address_details['details']
            address=get_object_or_404(Address , user=instance)
            address.city=city
            address.details=details
            address.save()
        if validated_data.get('phone_number', None):
            instance.phone_number = validated_data.get('phone_number')
            instance.save()
        if validated_data.get('name', None):
            instance.name = validated_data.get('name')
            instance.save()
        return instance

class UserDetailsSerializer(serializers.ModelSerializer):
    address_details = AddressSerializer()
    class Meta:
        model = NewUser
        fields = ['email','name','phone_number','address_details']


"""class userNumbersAllSerializer(serializers.ModelSerializer):
    current_cart=serializers.ModelSerializer()
    orders_made=serializers.ModelSerializer()
    orders_in_process=serializers.ModelSerializer()
    orders_refunded=serializers.ModelSerializer()
    class Meta:
        model = NewUser
        fields=['current_cartitems' , 'orders_made' , 'orders_in_process' , 'orders_refunded' ]
    def get_current_cart (self,obj):
        current_cartitems=0
        try:
            cart=Cart.objects.get(cart__user=obj.email)
            current_cartitems = len(cart.cartitems)
        except:
            pass
    """
class userNumbersMiniSerializer(serializers.ModelSerializer , UserNumbers):
    nbOf_current_cartitems=serializers.SerializerMethodField()
    nbOf_orders_in_process=serializers.SerializerMethodField()
    class Meta:
        model = NewUser
        fields=['nbOf_current_cartitems' , 'nbOf_orders_in_process' ]
    def get_nbOf_current_cartitems(self, obj):
        return self.get_current_cartitems(obj)
    def get_nbOf_orders_in_process(self,obj):
        return self.get_orders_made(obj)
       
        




class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta :
        model = Address
        fields = ['name','phone_number']


class UserUpdateMiniSerializer(serializers.ModelSerializer):
    class Meta :
        model = NewUser
        fields = ['phone_number']

        


class UserMiniSerializer(serializers.ModelSerializer):
        class Meta:
            model = NewUser
            fields = ['phone_number']


class CustomPackInfoSerializer(serializers.ModelSerializer):
    class Meta : 
        model = CustomPack
        fields = ['id','title','sale_price','isCopy']

class CartinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields =['subtotal']


class FirstLoadSerializer (serializers.ModelSerializer):
    class Meta : 
        model = GuestUsers
        fields = ['device_id']