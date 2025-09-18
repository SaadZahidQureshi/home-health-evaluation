import os
import base64
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from weasyprint import HTML, CSS



def encode_image_to_base64(path):
    if path.startswith("/media/"):
        path = os.path.join(settings.MEDIA_ROOT, path.replace("/media/", ""))
    
    if not os.path.exists(path):
        return None
    
    with open(path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode("utf-8")

        ext = os.path.splitext(path)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            mime = "image/jpeg"
        elif ext == ".png":
            mime = "image/png"
        elif ext == ".gif":
            mime = "image/gif"
        else:
            mime = "image/png"

        return f"data:{mime};base64,{img_data}"


def replace_images_with_base64(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key == "image" and isinstance(value, str):
                new_data[key] = encode_image_to_base64(value)
            else:
                new_data[key] = replace_images_with_base64(value)
        return new_data

    elif isinstance(data, list):
        return [replace_images_with_base64(item) for item in data]

    return data


def render_to_pdf(template_src, context_dict={}):
    context_dict = replace_images_with_base64(context_dict)
    house_image = context_dict["data"]["customer"]["house_image"] or '/media/default-home-image.png'
    context_dict["data"]["customer"]["house_image"] = encode_image_to_base64(house_image)
    html_string = render_to_string(template_src, context_dict)

    # Multiple approaches for base_url
    base_url = None
    
    # Method 1: Try STATIC_ROOT first (production)
    if getattr(settings, "STATIC_ROOT", None) and os.path.exists(settings.STATIC_ROOT):
        base_url = f"file://{os.path.abspath(settings.STATIC_ROOT)}/"
    
    # Method 2: Try STATICFILES_DIRS (development)
    elif getattr(settings, "STATICFILES_DIRS", None):
        for static_dir in settings.STATICFILES_DIRS:
            if os.path.exists(static_dir):
                base_url = f"file://{os.path.abspath(static_dir)}/"
                break
    
    # Method 3: Fallback to BASE_DIR
    if not base_url:
        base_url = f"file://{os.path.abspath(settings.BASE_DIR)}/"

    print(f"Using base_url: {base_url}")  # Debug print
    html = HTML(string=html_string, base_url=base_url)

    # Enhanced CSS with page break controls
    css = CSS(string='''
        @page { 
            size: A4; 
            margin: 1cm;
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10px;
                color: #666;
            }
        }
        
        body { 
            font-family: Arial, sans-serif; 
            font-size: 12px;
            line-height: 1.4;
        }
        
        /* Page break controls */
        .page-break-before {
            page-break-before: always;
        }
        
        .page-break-after {
            page-break-after: always;
        }
        
        .page-break-inside-avoid {
            page-break-inside: avoid;
        }
        
        /* Prevent breaking these elements */
        .section {
            page-break-inside: avoid;
            margin-bottom: 20px;
        }
        
        .section-header {
            page-break-after: avoid;
            margin-bottom: 10px;
        }
        
        .task-grid {
            page-break-inside: avoid;
        }
        
        /* Force break before major sections if needed */
        .major-section {
            page-break-before: always;
        }
        
        /* Keep images with their captions */
        .task-item {
            page-break-inside: avoid;
            display: inline-block;
            margin: 5px;
        }
        
        /* Image sizing for PDF */
        .task-item img {
            max-width: 100%;
            height: auto;
            display: block;
        }
        
        /* Prevent orphaned headers */
        h1, h2, h3, h4, h5, h6 {
            page-break-after: avoid;
        }
        
        /* Keep paragraphs with strong tags together */
        p strong {
            page-break-after: avoid;
        }
    ''')

    return html.write_pdf(stylesheets=[css])


def send_home_evaluation_report_email(customer, data=None):
    subject = "Your Healthy Home Evaluation Report"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [customer.user.email]

    text_content = subject
    text_template = get_template("email/report-email-template.html")
    context_obj = {"customer": customer, "type": "healthy"}
    template_content = text_template.render(context_obj)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(template_content, "text/html")

    context = {"customer": customer, "data": data}    
    pdf = render_to_pdf("email/healthy_home_report.html", context)
    if pdf:
        # file_path = os.path.join(settings.BASE_DIR, "Healthy_Home_Report.pdf")
        # with open(file_path, "wb") as f:
        #     f.write(pdf)

        msg.attach("Healthy_Home_Report.pdf", pdf, "application/pdf")
        msg.send()


def send_home_energy_report_email(customer, data=None):
    subject = "Your Residencial Home Evaluation Report"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [customer.user.email]

    text_content = subject
    text_template = get_template("email/report-email-template.html")
    context_obj = {"customer": customer, "type": "residential"}
    template_content = text_template.render(context_obj)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(template_content, "text/html")

    context = {"customer": customer, "data": data}
    pdf = render_to_pdf("email/residential-home-report.html", context)
    if pdf:
        # file_path = os.path.join(settings.BASE_DIR, "Residential_Home_Report.pdf")
        # with open(file_path, "wb") as f:
        #     f.write(pdf)

        msg.attach("Residential_Home_Report.pdf", pdf, "application/pdf")
        msg.send()

def format_service_type(service_type):
    return service_type.replace("_", " ").title()


def send_contact_us_email(first_name, last_name, email, phone_number, service_type, message):
    subject = "New Contact Us Submission"
    text_content = subject
    template = get_template("email/contact_us_email.html")
    context = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "service_type": format_service_type(service_type),
        "message": message,
    }
    html_content = template.render(context)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        settings.CONTACT_EMAIL,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_appointment_email(data):
    subject = "New Appointment Scheduled – PG Home Dynamics"
    text_content = subject
    template = get_template("email/appointment_email.html")
    context = {"data": data}
    # context = {
    #     "appointment_date": appointment_date,
    #     "appointment_time": appointment_time,
    #     "first_name": first_name,
    #     "last_name": last_name,
    #     "email": email,
    #     "phone_number": phone_number,
    #     "address": address,
    #     "zip_code": zip_code,
    #     "city": city,
    #     "state": state,
    #     "notes": notes,
    #     "message": message,
    # }
    html_content = template.render(context)
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        settings.CONTACT_EMAIL,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()