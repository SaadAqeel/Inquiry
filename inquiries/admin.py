from django.contrib import admin
from .models import City, InquiryType, SalesReference, Campaign, Status, Inquiry, Remark


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(InquiryType)
class InquiryTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(SalesReference)
class SalesReferenceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "inquiry_type",
        "status",
        "travel_date",
        "follow_up_date",
        "created_at",
    )
    search_fields = ("customer_name", "email", "city_area")
    list_filter = ("inquiry_type", "status", "city", "sales_person")


@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    list_display = ("id", "inquiry", "text", "created_at")
    search_fields = ("text",)
