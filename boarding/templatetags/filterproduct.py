from django import template, templatetags
from boarding.models import UserAccess, Products
from django.urls import reverse

def checkAccess(product, useraccess):

    if useraccess.filter(product=product.pk):
        return True

    return False

register = template.Library()

@register.simple_tag
def printAccess(product, useraccess):
    return "Has Access" if checkAccess(product, useraccess) else "No Access"

@register.simple_tag
def printAddRemove(product, useraccess):
    return "Delete" if checkAccess(product, useraccess) else "Add"

@register.simple_tag
def addOrRemove(product, useraccess, user):
    useraccessobject = useraccess.filter(product=product.pk)
    return reverse('remove', kwargs={'pk' : useraccessobject[0].pk}) if checkAccess(product, useraccess) else reverse('addaccess', kwargs={'userPK': user.pk, 'productPK': product.pk})
