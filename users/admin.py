from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    # On définit les groupes de champs à afficher dans la page d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Supplémentaires', {'fields': ('phone', 'avatar')}),
    )
    # Pour l'affichage dans la liste des utilisateurs
    list_display = ('email', 'username', 'phone', 'is_staff', 'avatar_thumbnail')

    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="height:80px;width:80px;object-fit:cover; border-radius:50%;" />', obj.avatar.url)
        return "—"
    avatar_thumbnail.short_description = 'Avatar'

# On enregistre le User avec notre configuration personnalisée
admin.site.register(User, CustomUserAdmin)
admin.site.register(Address)
