from django.urls import path
from .views import inquiry_dashboard, create_inquiry, create_remark, inquiry_detail

urlpatterns = [
    path("", inquiry_dashboard, name="inquiry_dashboard"),
    path("create/", create_inquiry, name="create_inquiry"),
    path("inquiry/<int:inquiry_id>/", inquiry_detail, name="inquiry_detail"),
]
