from django.contrib import admin
from .models import ReaderProfile, ReadingList, BookStatus

class BaseAdmin(admin.ModelAdmin):
    """
    BaseAdmin provides common functionality for all admin classes,
    including read-only fields for timestamps and user tracking.
    """
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)
        super().save_model(request, obj, form, change)


class ReadingListInline(admin.TabularInline):
    """
    Inline for ReadingList to manage the relationship with books,
    allowing inline editing of the reading list within the reader profile.
    """
    model = ReadingList
    extra = 1
    autocomplete_fields = ['book']
    fields = ('book', 'status')


class ReaderProfileAdmin(BaseAdmin):
    """
    Admin interface for ReaderProfile, managing user profiles in the library system.
    Displays user information and favorite genre with related timestamps.
    """
    list_display = ('user', 'favorite_genre', 'created_at', 'updated_at')
    search_fields = ('user__username', 'favorite_genre__name')
    ordering = ('user__username',)
    list_filter = ('favorite_genre',)
    inlines = [ReadingListInline]


class ReadingListAdmin(BaseAdmin):
    """
    Admin interface for ReadingList, displaying books associated with a reader
    along with their status and timestamps.
    """
    list_display = ('reader', 'book', 'status', 'created_at')
    ordering = ('-created_at',)
    list_filter = ('status',)


class BookStatusAdmin(BaseAdmin):
    """
    Admin interface for BookStatus, managing the status of books in the library system.
    """
    list_display = ('name', 'created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(ReaderProfile, ReaderProfileAdmin)
admin.site.register(ReadingList, ReadingListAdmin)
admin.site.register(BookStatus, BookStatusAdmin)
