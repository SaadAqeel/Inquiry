from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Inquiry, Remark
from .forms import (
    InquiryFilterForm,
    InquiryForm,
    InquiryUpdateForm,
    RemarkForm,
    RemarkFormSet,
)
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView


@login_required
def inquiry_dashboard(request):
    inquiries = Inquiry.objects.all()
    filter_form = InquiryFilterForm(request.GET or None)

    # Filtering logic
    if filter_form.is_valid():
        if filter_form.cleaned_data["id"]:
            inquiries = inquiries.filter(id__icontains=filter_form.cleaned_data["id"])
        if filter_form.cleaned_data["customer_name"]:
            inquiries = inquiries.filter(
                customer_name__icontains=filter_form.cleaned_data["customer_name"]
            )
        if filter_form.cleaned_data["primary_contact"]:
            inquiries = inquiries.filter(
                primary_contact__icontains=filter_form.cleaned_data["primary_contact"]
            )
        if filter_form.cleaned_data["customer_name"]:
            inquiries = inquiries.filter(
                customer_name__icontains=filter_form.cleaned_data["customer_name"]
            )
        if filter_form.cleaned_data["city"]:
            inquiries = inquiries.filter(city=filter_form.cleaned_data["city"])
        if filter_form.cleaned_data["sales_reference"]:
            inquiries = inquiries.filter(
                sales_reference=filter_form.cleaned_data["sales_reference"]
            )
        if filter_form.cleaned_data["sales_person"]:
            inquiries = inquiries.filter(
                sales_person=filter_form.cleaned_data["sales_person"]
            )
        if filter_form.cleaned_data["campaign"]:
            inquiries = inquiries.filter(campaign=filter_form.cleaned_data["campaign"])
        if filter_form.cleaned_data["inquiry_type"]:
            inquiries = inquiries.filter(
                inquiry_type=filter_form.cleaned_data["inquiry_type"]
            )
        if filter_form.cleaned_data["travel_date"]:
            inquiries = inquiries.filter(
                travel_date=filter_form.cleaned_data["travel_date"]
            )
        if filter_form.cleaned_data["follow_up_date"]:
            inquiries = inquiries.filter(
                follow_up_date=filter_form.cleaned_data["follow_up_date"]
            )
        if filter_form.cleaned_data["status"]:
            inquiries = inquiries.filter(status=filter_form.cleaned_data["status"])

    return render(
        request,
        "inquiries/dashboard.html",
        {"inquiries": inquiries, "filter_form": filter_form},
    )


@login_required
def create_inquiry(request):
    if request.method == "POST":
        inquiry_form = InquiryForm(request.POST)
        remark_formset = RemarkFormSet(request.POST)

        if inquiry_form.is_valid() and remark_formset.is_valid():
            inquiry = inquiry_form.save()  # Save the inquiry

            # Save the remarks
            remarks = remark_formset.save(commit=False)
            for remark in remarks:
                remark.inquiry = inquiry  # Set the inquiry for each remark
                remark.user = request.user  # Set the user to the current logged-in user
                remark.save()

            return redirect("inquiry_dashboard")  # Redirect to the inquiry detail page

    else:
        inquiry_form = InquiryForm()
        remark_formset = RemarkFormSet()

    context = {
        "inquiry_form": inquiry_form,
        "remark_formset": remark_formset,
    }
    return render(request, "inquiries/create_inquiry.html", context)


@login_required
def create_remark(request):
    inquiries = Inquiry.objects.all()
    return render(
        request,
        "inquiries/add_remark.html",
        {"inquiries": inquiries},
    )

    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    remarks = inquiry.remarks.all()
    # Get all remarks related to this inquiry

    if request.method == "POST":
        inquiry_form = InquiryUpdateForm(request.POST, instance=inquiry)
        remark_formset = RemarkFormSet(request.POST)

        if inquiry_form.is_valid() and remark_formset.is_valid():
            # Update inquiry fields
            inquiry_form.save()

            # Create a new remark
            new_remark = remark_formset.save(commit=False)
            new_remark.inquiry = inquiry
            # Set the user to the current logged-in user

            # Save additional fields from the inquiry
            new_remark.status_remarks = (
                inquiry.status
            )  # Get the current status from the inquiry
            new_remark.follow_up_date_remark = (
                inquiry.follow_up_date
            )  # Get the current follow-up date
            new_remark.sales_person_remark = (
                inquiry.sales_person
            )  # Get the current salesperson

            new_remark.save()  # Save the remark with the additional fields

            return redirect(
                "inquiry_detail", inquiry_id=inquiry_id
            )  # Redirect to the same page

    else:
        inquiry_form = InquiryUpdateForm(instance=inquiry)
        remark_formset = RemarkFormSet

    context = {
        "inquiry_form": inquiry_form,
        "remark_formset": remark_formset,
        "inquiry": inquiry,
        "remarks": remarks,
    }
    return render(request, "inquiries/inquiry_detail.html", context)


@login_required
def inquiry_detail(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    remarks = inquiry.remarks.all()

    if request.method == "POST":
        inquiry_form = InquiryUpdateForm(request.POST, instance=inquiry)
        remark_form = RemarkForm(request.POST)

        if inquiry_form.is_valid() and remark_form.is_valid():
            # First update the inquiry
            updated_inquiry = inquiry_form.save()

            # Then create a new remark
            new_remark = remark_form.save(commit=False)
            new_remark.inquiry = updated_inquiry

            # Note: You don't need to manually set these fields because
            # your Remark.save() method already does this:
            # new_remark.status_remarks = updated_inquiry.status
            # new_remark.follow_up_date_remark = updated_inquiry.follow_up_date
            # new_remark.sales_person_remark = updated_inquiry.sales_person

            new_remark.save()

            return redirect("inquiry_detail", inquiry_id=inquiry_id)

    else:
        inquiry_form = InquiryUpdateForm(instance=inquiry)
        remark_form = RemarkForm()

    context = {
        "inquiry_form": inquiry_form,
        "remark_form": remark_form,
        "inquiry": inquiry,
        "remarks": remarks,
    }
    return render(request, "inquiries/inquiry_detail.html", context)
