from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from weasyprint import HTML, CSS
import os
import base64


def get_image_as_base64(image_path):
    """Convert image to base64 for embedding in PDF"""
    try:
        # Try to find the static file
        found_path = finders.find(image_path)
        if found_path:
            with open(found_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                # Detect image type
                if image_path.lower().endswith('.png'):
                    return f"data:image/png;base64,{img_data}"
                elif image_path.lower().endswith(('.jpg', '.jpeg')):
                    return f"data:image/jpeg;base64,{img_data}"
                else:
                    return f"data:image/png;base64,{img_data}"  # default to png
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
    return None


def render_to_pdf(template_src, context_dict={}):
    # Add base64 images to context
    context_dict['get_image_base64'] = get_image_as_base64("file:///C:/Users/DELL/Documents/Myprojects/Healthy%20Home%20Evaluation/static/img/audit.png")
    
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
    subject = "Healthy Home Evaluation Report!"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [customer.user.email]

    text_content = f"Hi {customer.user.name}, please find your PDF attached."
    html_content = f"<p>Hi {customer.user.name},</p><p>Your PDF is attached.</p>"

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")

    context = {"customer": customer, "data": data}    
    pdf = render_to_pdf("email/healthy_home_report.html", context)
    if pdf:

        # Save locally in BASE_DIR
        file_path = os.path.join(settings.BASE_DIR, "Healthy_Home_Report.pdf")
        with open(file_path, "wb") as f:
            f.write(pdf)

        msg.attach("Healthy_Home_Report.pdf", pdf, "application/pdf")
        msg.send()