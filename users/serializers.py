from delivery.serializers import ShippingCitySerializer
from re import T
from django.db import models
from django.db.models import fields, manager
from rest_framework import serializers
from users.models import Address, NewUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from customization.models import CustomPack
from cart.models import Cart
from .models import GuestUsers

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True )
    password = serializers.CharField(min_length=8, write_only=True)
    

    class Meta:
        model = NewUser
        fields = ('email', 'name','phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
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
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    name = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = NewUser.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = NewUser
        fields = ['email', 'password', 'name', 'tokens','id']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        print(email,password)
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({'error':'Invalid credentials, try again'})
        if not user.is_active:
            raise serializers.ValidationError({'error':"your account is not verified "})

        return {
            'id':user.id,
            'email': user.email,
            'name': user.name,
           
            'tokens': user.tokens()
        }

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
    city=ShippingCitySerializer()
    class Meta:
        model = Address
        fields = ['address','city']

class UserSerializer(serializers.ModelSerializer):
    address_details = AddressSerializer(read_only=True ,)
    class Meta:
        model = NewUser
        fields = ['email','name','name2','phone_number','address_details']
        read_only_fields = ['address_details','email']
    def update(self, instance, validated_data):
        validated_data.pop('address_details', None)
        user=super(UserSerializer, self).update(instance, validated_data)
        return user



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta :
        model = Address
        fields = ['name', 'name2','phone_number']


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

class UserHistoriqueSerializer(serializers.ModelSerializer):
    cart_set = CartinfoSerializer(many=True)
    custompack_set = CustomPackInfoSerializer(many=True)
    class Meta:
        model = NewUser
        fields = ['name','email','cart_set','custompack_set']



class GuestHistoriqueSerializer(serializers.ModelSerializer):
    cart_set = CartinfoSerializer(many=True)
    custompack_set = CustomPackInfoSerializer(many=True)
    class Meta:
        model = GuestUsers
        fields = ['cart_set','custompack_set']