from django.contrib import admin
from django import forms

from .models import Landing, SocialMedia

# Constants
FORM_ATTRS = {
    "rows": 6,
    "cols": 60,
    "style": "font-family: monospace;",
}

class SocialMediaInline(admin.StackedInline):
    """Inline admin for social media links."""

    model = SocialMedia
    extra = 0
    fields = ("title", "url_link")


@admin.register(Landing)
class LandingAdmin(admin.ModelAdmin):
    """Admin interface for blog settings."""

    inlines = [SocialMediaInline]
    list_display = ["title", "desc", "footer", "avatar"]
    search_fields = ["title", "desc"]

    def has_add_permission(self, request):
        """Allow only one instance of blog settings."""
        return Landing.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of blog settings."""
        return False

    def get_form(self, request, obj=None, **kwargs):
        """Customize form widgets."""
        form = super().get_form(request, obj, **kwargs)

        # Customize blog description field
        if "desc" in form.base_fields:
            form.base_fields["desc"].widget = forms.Textarea(
                attrs=FORM_ATTRS
            )

        return form

    def save_formset(self, request, form, formset, change):
        """
        Save the parent instance before saving the formset.
        """
        if formset.model == SocialMedia:
            # First, save the parent object (BlogSettings)
            form.instance.save()
            # Then, save the inline objects (SocialMedia)
            formset.save()
        else:
            super().save_formset(request, form, formset, change)
