from django.contrib import admin

from .models import User, Profile


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1


class UserAdmin(admin.ModelAdmin):
    # list_display = ('name', 'cinema_id', 'place_count', 'row_count', 'seat_count')
    # list_filter = ('cinema_id', )
    # search_fields = ('cinema_id', )
    inlines = (ProfileInline, )


admin.site.register(Profile)
admin.site.register(User, UserAdmin)
