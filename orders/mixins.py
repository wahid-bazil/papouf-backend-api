from django.contrib.auth import models
from rest_framework import exceptions

from django.db import models
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from store__papouf.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage


class MethodSerializerView(object):
    '''
    Utility class for get different serializer class by method.
    For example:
    method_serializer_classes = {
        ('GET', ): MyModelListViewSerializer,
        ('PUT', 'PATCH'): MyModelCreateUpdateSerializer
    }
    '''
    method_serializer_classes = None

    def get_serializer_class(self):
        assert self.method_serializer_classes is not None, (
            'Expected view %s should contain method_serializer_classes '
            'to get right serializer class.' %
            (self.__class__.__name__, )
        )
        for methods, serializer_cls in self.method_serializer_classes.items():
            if self.request.method in methods:
                return serializer_cls

        raise exceptions.MethodNotAllowed(self.request.method)


def send_order_email(ctx ,client_email ,subject) :
    message = get_template("order_email.html").render(ctx)
    mail = EmailMessage(
    subject=subject,
    body=message,
    from_email=EMAIL_HOST_USER,
    to=[client_email],
    reply_to=[EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    print('done')
    return mail.send()

       