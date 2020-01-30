from django.contrib import admin

from mysite.models import DateEntries

from .models import AccountTypes, BdgCategories, BdgItems, BdgTypes, Entries


# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display   = ('bdgType', 'category', 'name')
    list_filter    = ('category', 'bdgType')
    ordering       = ('category', )
    search_fields  = ('name',)

class EntriesAdmin(admin.ModelAdmin):
    list_display   = ('accountType', 'item', 'date', 'amount')
    list_filter    = ('accountType', 'item', 'date')
    date_hierarchy = 'date'
    ordering       = ('date', )
    search_fields  = ('item', 'date')

admin.site.register(BdgTypes)
admin.site.register(BdgCategories)
admin.site.register(AccountTypes)
admin.site.register(BdgItems, ItemAdmin)
admin.site.register(Entries, EntriesAdmin)
admin.site.register(DateEntries)
