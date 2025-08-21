from django.db import models

class ServerUpdate(models.Model):
    # Add a dummy field since Django requires at least one field
    last_updated = models.DateTimeField(auto_now=True, help_text="Last update timestamp")
    
    class Meta:
        verbose_name = "Server Update"
        verbose_name_plural = "Server Update"
        # Prevent creation of multiple records
        permissions = [
            ("can_update_server", "Can update server"),
        ]

    def __str__(self):
        return f"Server Update - Last: {self.last_updated}"