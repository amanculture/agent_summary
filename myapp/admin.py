from django.contrib import admin, messages
from django.urls import path
from django.http import HttpResponseRedirect
from django.core.management import call_command
from .models import ServerUpdate

class ServerUpdateAdmin(admin.ModelAdmin):
    change_list_template = "admin/server_update.html"
    list_display = ['last_updated']
    
    # Hide "Add" button and restrict permissions
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

    def get_urls(self):
        urls = super().get_urls()   
        custom_urls = [
            path("run-update/", self.admin_site.admin_view(self.run_update), name="server-update"),
        ]
        return custom_urls + urls

    def run_update(self, request):
        try:
            call_command("update_from_zip")
            
            # Create or update a record to track last update
            obj, created = ServerUpdate.objects.get_or_create(pk=1)
            obj.save()  # This will update the timestamp
            
            self.message_user(request, "✅ Update successful!", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"❌ Update failed: {e}", level=messages.ERROR)
        return HttpResponseRedirect("../")

    def changelist_view(self, request, extra_context=None):
        # Ensure at least one record exists for display
        if not ServerUpdate.objects.exists():
            ServerUpdate.objects.create(pk=1)
        return super().changelist_view(request, extra_context)

admin.site.register(ServerUpdate, ServerUpdateAdmin)