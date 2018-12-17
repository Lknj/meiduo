from . import models


def get_categories():
    '''
    categories = {
        1: { # 组1
            'channels': [{'id':, 'name':, 'url':},{}, {}...],
            'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
        },
        2: { # 组2

        }
    }
    '''
    channels = models.GoodsChannel.objects.order_by('group_id').order_by('sequence')
    categories = {}
    for channel in channels:
        # 判断当前频道是否存在, 如果不存在则新增此频道
        if channel.group_id not in categories:
            categories[channel.group_id] = {
                'channels': [],  # 指定频道的一级分类
                'sub_cats': []  # 指定频道的二级分类
            }
        # 频道存在时, 向频道添加一级分类
        categories[channel.group_id]['channels'].append({
            'id': channel.category.id,
            'name': channel.category.name,
            'url': channel.url
        })
        # 频道存在时,向频道中添加二级分类
        # 遍历此频道一级分类的所有二级分类
        for sub_cat2 in channel.category.subs.all():
            # print(sub_cat2)
            # 添加三级分类
            sub_cats3 = []
            # 遍历此频道二级分类的所有三级分类
            for sub_cat3 in sub_cat2.subs.all():
                sub_cats3.append(sub_cat3)
            sub_cat2.sub_cats = sub_cats3

            # 向频道中添加二级分类
            categories[channel.group_id]['sub_cats'].append(sub_cat2)
    return categories