from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class MainCategoryListFilter(admin.SimpleListFilter):
    title = _('All categories and subcategories')
    parameter_name = 'All categories and subcategories'
    def lookups(self, request, model_admin):
        return (
            ('yes', _('Only principal categories')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_main=True)
        else :
            return queryset.all()

class ActiveCategoryListFilter(admin.SimpleListFilter):
    title = _('All active and deactivated categories')
    parameter_name = 'All active and deactivated categories'
    def lookups(self, request, model_admin):

        return (
            ('', 'All categories and subcategories'),
            ('active', _('Only active categories')),
            ('desactived', _('Only deactivated categories')),
           
        )
    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'desactived':
            return queryset.filter(is_active=False)


