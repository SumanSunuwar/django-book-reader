from django.contrib import admin

# Register your models here.
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'middle_name')
    ordering = ('last_name', 'first_name')
    list_filter = ('created_at',)