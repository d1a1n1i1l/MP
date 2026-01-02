from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO

def render_to_pdf(template_path, context_dict, filename):
    """Генерирует PDF из шаблона с помощью xhtml2pdf"""
    html = render_to_string(template_path, context_dict)
    result = BytesIO()
    
    # Генерируем PDF
    pdf = pisa.CreatePDF(
        html,
        dest=result
    )
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse('Ошибка генерации PDF', status=500)