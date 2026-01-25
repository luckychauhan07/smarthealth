from django.contrib import admin
from .models import GeneratedPlan


@admin.register(GeneratedPlan)
class GeneratedPlanAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "generated_at",
        "updated_at",
    )

    search_fields = ("user__username",)
