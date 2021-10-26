
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from customization.models import CustomPackArticle
from collections.models import Article, Pack
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomPackArticleUpdate, CustomPackSerializer, CustomPackUserImage, CustomPack, CustomPackArticleSerializer,CreateCustomPackArticleSerializer ,PackCopySerializer
from rest_framework.permissions import AND, SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError, PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from accounts.models import GuestUsers
from collections.serializers import PackSerializer
from media.models import CustomPackImage
from cart.models import CartItem
from .mixins import MethodSerializerView
from .serializers import CreateCustomPackSerializer




class CustomPackTotal(generics.RetrieveAPIView):
    queryset = CustomPack.objects.all()
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        total = obj.sale_price
        return Response(total)


class CustomPackImageDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = CustomPackImage.objects.filter(custompack__user=user)

            return queryset
        else:
            try:
                device_id = str(self.request.headers['deviceid'])
            except:
                raise NotFound({"detail": "user not found"})
            queryset = CustomPack.objects.filter(
                custompack__device_id=device_id)
            return queryset


class CustomPackList(MethodSerializerView,generics.ListCreateAPIView):

    method_serializer_classes = {
        ('GET', ): CustomPackSerializer,
        ('POST'): CreateCustomPackSerializer
    }
    def get_queryset(self):
        try:
            isCopy = self.request.query_params('isCopy')
        except:
            isCopy = False

        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = CustomPack.objects.filter(
                user=user, isCopy=isCopy)
            return queryset
        else:
            try:
                device_id = str(self.request.headers['deviceid'])
            except:
                raise NotFound({"detail": "user not found"})
            guestuser, created = GuestUsers.objects.get_or_create(
                device_id=device_id)
            queryset = CustomPack.objects.filter(
                device_id=guestuser, isCopy=isCopy) 
            return queryset
    def create(self, request, *args, **kwargs):
        try:
            pack_id = int(self.request.data['pack_id'])
        except:
            pass
        pack = get_object_or_404(Pack, pk=pack_id)
        boxe = pack.boxe
        title = pack.title
        main_image = pack.images.filter(main_image=True).first().image
        if self.request.user.is_authenticated:
            user = self.request.user
            CustomPack.objects.filter(
                user=user, isCopy=True, inCart=False).delete()
            customPack = CustomPack.objects.create(
                user=user, boxe=boxe, title=title, isCopy=True)
            CustomPackImage.objects.create(item=customPack, image=main_image)
            articles = pack.packarticle_set.all()
            for article in articles:
                CustomPackArticle.objects.create(
                    custompack=customPack, item=article.item, quantity=article.quantity)
        else:
            try:
                device_id = str(self.request.headers['deviceid'])
            except:
                raise NotFound({"detail": "user not found"})
            guestuser, created = GuestUsers.objects.get_or_create(
                device_id=device_id)
            CustomPack.objects.filter(
                device_id=guestuser, isCopy=True, inCart=False).delete()
            customPack = CustomPack.objects.create(
                device_id=guestuser, boxe=boxe, title=title, isCopy=True)
            CustomPackImage.objects.create(item=customPack, image=main_image)
            articles = pack.packarticle_set.all()
            for article in articles:
                CustomPackArticle.objects.create(
                    custompack=customPack, item=article.item, quantity=article.quantity)

        serializer = CustomPackSerializer(customPack)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class CustomPackDetails(generics.RetrieveAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = CustomPack.objects.filter(user=user)
            return queryset
        else:
            try:
                device_id = str(self.request.headers['deviceid'])
            except:
                raise NotFound({"detail": "user not found"})
            guestuser, created = GuestUsers.objects.get_or_create(
                device_id=device_id)
            queryset = CustomPack.objects.filter(
                device_id=guestuser)
            return queryset

    serializer_class = CustomPackSerializer





class CustomPackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomPack.objects.all()
    serializer_class = CustomPackSerializer
    def get_object(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            obj = CustomPack.objects.filter(
                user=user, isCopy=False, inCart=False).first()
            return obj
        else:
            try:
                device_id = str(self.request.headers['deviceid'])
            except:
                raise NotFound({"detail": "user not found"})
            guestuser, created = GuestUsers.objects.get_or_create(
                device_id=device_id)
            
            obj = CustomPack.objects.filter(
                device_id=guestuser, isCopy=False, inCart=False).first()
            return obj



class CustomPackArticleList(generics.CreateAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = CustomPackArticle.objects.filter(
                custompack__user=self.request.user)
            return queryset
        else:
            try:
                device_id = str(self.request.headers['deviceid'])
            except:
                raise NotFound({"detail": "user not found"})
            queryset = CustomPackArticle.objects.filter(
                custompack__device_id=device_id)
            return queryset
    serializer_class = CreateCustomPackArticleSerializer
    def create(self, request, *args, **kwargs):
        custom_pack = get_object_or_404(
            CustomPack, pk=request.data['custompack_id'])
        item = get_object_or_404(Article, pk=request.data['item_id'])
        custom_pack_article = self.get_queryset().filter(
            custompack=custom_pack, item=item)
        if custom_pack_article.exists():
            custom_pack_article = custom_pack_article.first()
            custom_pack_article.quantity += 1
            custom_pack_article.save()
            serializer = CustomPackArticleSerializer(custom_pack_article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            custom_pack_article = CustomPackArticle.objects.create(
                custompack=custom_pack, item=item)
            custom_pack_article = self.get_queryset().filter(
                custompack=custom_pack, item=item).first()

            serializer = CustomPackArticleSerializer(custom_pack_article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomPackArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomPackArticle.objects.all()
    serializer_class = CustomPackArticleUpdate
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        article_id = 0
        try:
            quantity = int(request.data['quantity'])
        except Exception as e:
            raise ValidationError("Please, input a vaild quantity")

        if quantity < 1:
            raise ValidationError("Please, input vaild quantity")

        if quantity > obj.item.inventory:
            raise NotAcceptable(
                "Your order quantity more than our inventory for now")
        try:
            article_id = int(request.data['article_id'])
        except:
            pass
        
        if article_id !=0:
            article=get_object_or_404(Article , pk=article_id)
            obj.item=article
        obj.quantity = quantity    
        obj.save()
        serializer = CustomPackArticleSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PackCopyCustomisation(generics.CreateAPIView):
    queryset = Pack.objects.all()
    serializer_class = PackCopySerializer
    def create(self, request, *args, **kwargs):
        try:
            original_pack_id = int(self.request.data['original_pack_id'])
        except:
            pass
        pack = get_object_or_404(Pack, pk=original_pack_id)
        title = pack.title
        main_image = pack.images.filter(main_image=True).first().image
        if self.request.user.is_authenticated:
            user = self.request.user
            CustomPack.objects.filter(
                user=user, isCopy=True, inCart=False).delete()
            customPack = CustomPack.objects.create(
                user=user, title=title, isCopy=True)
            CustomPackImage.objects.create(item=customPack, image=main_image)
            articles = pack.packarticle_set.all()
            for article in articles:
                a=CustomPackArticle.objects.create(
                    custompack=customPack, item=article.item, quantity=article.quantity)
                
            
        else:
            try:
                device_id = str(self.request.headers['deviceid'])
            except:
                raise NotFound({"detail": "user not found"})
            guestuser, created = GuestUsers.objects.get_or_create(
                device_id=device_id)
            CustomPack.objects.filter(
                device_id=guestuser, isCopy=True, inCart=False).delete()
            customPack = CustomPack.objects.create(
                device_id=guestuser, title=title, isCopy=True)
            CustomPackImage.objects.create(item=customPack, image=main_image)
            articles = pack.packarticle_set.all()
            for article in articles:
                CustomPackArticle.objects.create(
                    custompack=customPack, item=article.item, quantity=article.quantity)

        serializer = CustomPackSerializer(customPack)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response (status=status.HTTP_201_CREATED)
    


