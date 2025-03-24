from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InquiryType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SalesReference(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    primary_contact = models.CharField(max_length=20)
    secondary_contact = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    city_area = models.CharField(max_length=255)
    travel_date = models.DateField()
    follow_up_date = models.DateField()
    inquiry_type = models.ForeignKey(InquiryType, on_delete=models.CASCADE)
    branch = models.CharField(max_length=255)
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE)
    sales_reference = models.ForeignKey(SalesReference, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.inquiry_type.name}"


class Remark(models.Model):
    id = models.AutoField(primary_key=True)
    inquiry = models.ForeignKey(
        Inquiry, on_delete=models.CASCADE, related_name="remarks"
    )

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status_remarks = models.ForeignKey(
        Status, on_delete=models.CASCADE
    )  # Adjust max_length as needed
    follow_up_date_remark = models.DateField(null=True, blank=True)
    sales_person_remark = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    def save(self, *args, **kwargs):
        # Automatically set author_name and author_email from the related Author instance
        if self.inquiry:
            self.status_remarks = self.inquiry.status
            self.follow_up_date_remark = self.inquiry.follow_up_date
            self.sales_person_remark = self.inquiry.sales_person
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Remark for {self.inquiry.customer_name} on {self.created_at.strftime('%Y-%m-%d')}"
