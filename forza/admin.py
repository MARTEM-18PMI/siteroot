from django.contrib import admin
from django.db.models import Max
from . import models


class PostInline(admin.TabularInline):
    model = models.Post

    def is_edited(self, obj):
        return self.is_edited()

    is_edited.boolean = True

    field = ('subject', 'text', 'created_at', 'is_edited')
    readonly_fields = ('subject', 'text', 'created_at')
    ordering = ('-created_at',)
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


class BlogAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(updated_at=Max('post__updated_at'))

    def updated_at(self, obj):
        return obj.updated_at
    updated_at.admin_order_field = 'updated_at'

    def has_add_permission(self, request):
        return False

    list_display = ('title', 'author', 'updated_at')
    ordering = ('title',)
    fields = ('title', 'author', 'created_at')
    readonly_fields = ('author', 'created_at')
    view_on_site = True
    inlines = [PostInline]


class PostAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    list_display = ('subject', 'created_at', 'text')
    ordering = ('subject',)
    fields = ('subject', 'created_at', 'text')
    readonly_fields = ('created_at',)
    view_on_site = True


admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Post, PostAdmin)