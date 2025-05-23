from django.contrib import admin, messages

from django.contrib.admin.decorators import action

class PortableModelAdmin(admin.ModelAdmin):
    actions = ['portable_model_export_items']

    @action(description='Export selected items')
    def portable_model_export_items(self, request, queryset):
        pass
