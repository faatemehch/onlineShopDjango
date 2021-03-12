from django.db import models
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from eshop_products.models import Product


class Tag( models.Model ):
    title = models.CharField( max_length=120 )
    slug = models.SlugField()
    timestamp = models.DateTimeField( auto_now=True )
    active = models.BooleanField( default=True )
    product = models.ManyToManyField( Product, null=True, blank=True )

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ‌های محصولات'

    def __str__(self):
        return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator( instance )


pre_save.connect( tag_pre_save_receiver, sender=Tag )
