from django import forms
from .models import Campaign, Inquiry, Remark, SalesReference
from .models import Inquiry, City, InquiryType, Status
from django.contrib.auth.models import User
from django.forms import DateInput
from django.forms import inlineformset_factory


class InquiryForm(forms.ModelForm):

    class Meta:
        model = Inquiry
        fields = "__all__"

    travel_date = forms.DateField(
        widget=DateInput(attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"],  # Specify the input format if needed
    )
    follow_up_date = forms.DateField(
        widget=DateInput(attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"],  # Specify the input format if needed
    )


class InquiryUpdateForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ["follow_up_date", "status"]
        widgets = {
            "follow_up_date": forms.DateInput(
                attrs={"type": "date"}
            ),  # Use HTML5 date input
        }


class RemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        fields = ["text"]


RemarkFormSet = inlineformset_factory(
    Inquiry,
    Remark,
    form=RemarkForm,
    extra=1,
    can_delete=False,
)


class InquiryFilterForm(forms.Form):
    id = forms.IntegerField(required=False, label="Inquiry Id")
    customer_name = forms.CharField(
        required=False, label="Customer Name", max_length=255
    )
    primary_contact = forms.CharField(
        required=False, label="Primary Contact", max_length=255
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), required=False, label="City"
    )
    sales_reference = forms.ModelChoiceField(
        queryset=SalesReference.objects.all(), required=False, label="Sales Reference"
    )
    sales_person = forms.ModelChoiceField(
        queryset=User.objects.all(), required=False, label="Sales Person"
    )
    campaign = forms.ModelChoiceField(
        queryset=Campaign.objects.all(), required=False, label="Campaign"
    )
    inquiry_type = forms.ModelChoiceField(
        queryset=InquiryType.objects.all(), required=False, label="Inquiry Type"
    )
    travel_date = forms.DateField(
        required=False,
        label="Travel Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    follow_up_date = forms.DateField(
        required=False,
        label="Follow-up Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(), required=False, label="Status"
    )
