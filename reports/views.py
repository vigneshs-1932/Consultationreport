import io
import os
from datetime import datetime
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import ConsultationForm
from io import BytesIO
import base64


def generate_pdf(template_src, context_dict, filename):
    print(context_dict)
    """Generate PDF from template and context."""
    template = get_template(template_src)
    html = template.render(context_dict)

    result = io.BytesIO()
    pdf = pisa.CreatePDF(html, dest=result)

    if not pdf.err:
        result.seek(0)
        return FileResponse(result, as_attachment=True, filename=filename)
    return HttpResponse("Error generating PDF", status=500)


def consultation_report(request):
    if request.method == "POST":
        form = ConsultationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            # Handle uploaded logo
            logo_file = request.FILES.get("clinic_logo")

            logo_bytes = None
            if logo_file:
                # Read the uploaded file into BytesIO
                logo_bytes_io = BytesIO()
                for chunk in logo_file.chunks():
                    logo_bytes_io.write(chunk)
    
                # Get raw bytes
                logo_bytes = logo_bytes_io.getvalue() 

            # Get IP + Timestamp
            ip = get_client_ip(request)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Filename format: CR_{Last}_{First}_{DOB}.pdf
            filename = f"CR_{cd['patient_last_name']}_{cd['patient_first_name']}_{cd['patient_dob']}.pdf"

            # Build context
            context = {
                **cd,
                "clinic_logo": logo_bytes,
                "timestamp": timestamp,
                "ip": ip,
            }

            return generate_pdf("report_template.html", context, filename)
    else:
        form = ConsultationForm()

    return render(request, "index.html", {"form": form})


def get_client_ip(request):
    """Get client IP from request headers."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")
