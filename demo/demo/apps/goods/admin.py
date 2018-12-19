from django.contrib import admin
from . import models
from celery_tasks.generic_detail.tasks import generate_static_sku_detail_html


class SKUAdmin(admin.ModelAdmin):
    # 列表页属性
    # 编辑页属性
    list_display = ['id', 'name']

    # 新知识点:两个方法
    def save_model(self, request, obj, form, change):
        # 增加 修改时,会执行这个方法
        obj.save()
        # 新增逻辑,生成静态页面,写成celery任务的原因,可以直接返回列表页面
        generate_static_sku_detail_html(obj.id)


    def delete_model(self, request, obj):
        # 删除时,会执行这个方法

        pass


class SKUSpecificationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_sku_detail_html.delay(obj.sku.id)

    def delete_model(self, request, obj):
        sku_id = obj.sku.id
        obj.delete()
        generate_static_sku_detail_html.delay(sku_id)


class SKUImageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_sku_detail_html.delay(obj.sku.id)

        # 设置SKU默认图片
        sku = obj.sku
        if not sku.default_image_url:
            sku.default_image_url = obj.image.url
            sku.save()

    def delete_model(self, request, obj):
        sku_id = obj.sku.id
        obj.delete()
        generate_static_sku_detail_html.delay(sku_id)

admin.site.register(models.SKU, SKUAdmin)
admin.site.register(models.SKUSpecification, SKUSpecificationAdmin)
admin.site.register(models.SKUImage, SKUImageAdmin)
admin.site.register(models.GoodsCategory)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Goods)
admin.site.register(models.Brand)
admin.site.register(models.GoodsSpecification)
admin.site.register(models.SpecificationOption)


