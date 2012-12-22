from gao.models import Account, Good, Record
from django.contrib import admin

class AccountInline(admin.TabularInline):
    model = Account

class GoodInline(admin.TabularInline):
    model = Good

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')
    list_filter = ['name']
    search_fields = ['name']
    inline = [GoodInline]

class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'deadline')
    list_filter = ['name']
    search_fields = ['name']
    date_hierarchy = 'deadline'
    inline = [AccountAdmin]

class RecordAdmin(admin.ModelAdmin):
    list_display = ('account_from', 'account_to', 'amount', 'comment')
    list_filter = ['account_from', 'account_to', 'amount', 'comment']
    search_fields = ['account_from', 'account_to', 'amount', 'comment']
    date_hierarchy = 'created_at'

admin.site.register(Account, AccountAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(Record, RecordAdmin)