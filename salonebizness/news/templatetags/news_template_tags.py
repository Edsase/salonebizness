from django import template
from news.models import Category

#register this module as a template library
register = template.Library()

#add template tag by wrapping the inclusion template tag
#the action of this inclusion tag will be wrapped up in the template cat.html
@register.inclusion_tag('news/cat.html')
def get_category_list(cat = None):

    """function returns all categories in the db"""

    return {'cats': Category.objects.all(), 'act_cat': cat}


