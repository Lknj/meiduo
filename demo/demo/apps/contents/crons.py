from django.shortcuts import render
from django.conf import settings
from goods import models
from .models import ContentCategory, Content
from goods.utils import get_categories


def generate_index_html():
    # 1. 查询
    # 1.1 查分类数据
    categories = get_categories()
    # 1.2 查广告数据
    '''
    contents = {
        index_lbt: [此广告位的广告数据],
        ......
    }
    '''
    contents = {}
    contents_categories = ContentCategory.objects.all()
    for contents_category in contents_categories:
        contents[contents_category.key] = contents_category.contents.filter(status=True).order_by('sequence')

    # 2. 生成html字符串
    context = {
        'categories': categories,
        'contents': contents
    }
    response = render(None, 'index.html', context)
    html_str = response.content.decode()

    # 3. 写文件
    with open(settings.GENERATE_STATIC_DIR + 'index.html', 'w') as f:
        f.write(html_str)


