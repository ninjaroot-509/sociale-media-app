from django import template
from django.utils.safestring import mark_safe

from feed.models import Category

register = template.Library()

@register.simple_tag
def categories():
    items = Category.objects.filter(is_active=True).order_by('title')
    items_li = ""
    for i in items:
        items_li += """<a class="dropdown-item" href="/category/{}">{}</a>""".format(i.slug, i.title)
    return mark_safe(items_li)