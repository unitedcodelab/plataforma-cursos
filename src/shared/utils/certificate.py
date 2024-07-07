from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime

from django.core.files import File

from apps.courses.models import Certificate


def generate_certificate(**kwargs):
    certificate, _ = Certificate.objects.get_or_create(
        student_object_id=kwargs.get('student').id,
        student_content_type=kwargs.get('student').get_content_type(),
        instructor=kwargs.get('instructor'),
        course=kwargs.get('course'),
        hours=kwargs.get('hours')
    )

    html_content = create_html(certificate=certificate)
    pdf = generate_pdf(html_content)
    certificate.file.save(f'certificate_{certificate.id}.pdf', File(pdf))
    certificate.save()


def generate_pdf(html_content):
    pdf_file = BytesIO()

    try:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

        if not pisa_status.err:
            pdf_file.seek(0)
            return pdf_file

        else:
            print(f"PDF generation failed: {pisa_status.err}")
            return None

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None


def create_html(certificate):
    style = """
        <style>
            body { font-family: 'Arial', sans-serif; background-color: #f0f0f0; }
            .certificate-wrapper { max-width: 800px; margin: 50px auto; padding: 20px; border: 6px solid #4CAF50; border-radius: 30px; background-color: #fff; display: flex; flex-direction: row; justify-content: space-between; align-items: center; box-shadow: 0 0 20px rgba(0, 0, 0, 0.2); }
            .certificate-content { flex: 1; padding: 40px; }
            .certificate-title { font-size: 48px; font-weight: bold; text-align: center; margin-bottom: 30px; color: #4CAF50; text-transform: uppercase; }
            .certificate-info { font-size: 28px; line-height: 1.6; }
            .info-label { font-weight: bold; color: #4CAF50; }
            .certificate-seal { flex: 1; text-align: center; }
            .seal-image { max-width: 300px; height: auto; }
            .footer { margin-top: 10px; text-align: center; font-size: 20px; color: #555; }
            .intro-text { font-size: 24px; text-align: justify; margin-bottom: 20px; }
        </style>
    """

    intro_text = f"Certificamos que o aluno {certificate.student.name} em { datetime.now().strftime('%d/%m/%Y') } concluiu com sucesso o curso de {certificate.course.title}, ministrado por {certificate.instructor.author.name}, totalizando {certificate.hours} horas de estudo."

    html_content = f"""
        <html>
        <head>
            {style}
        </head>
        <body>
            <div class="certificate-wrapper">
                <div class="certificate-content">
                    <div class="certificate-title">Certificado de Conclusão</div>
                    <div class="intro-text">{intro_text}</div>
                    <div class="certificate-info">
                        <div><span class="info-label">Nome do Aluno:</span> { certificate.student.name }</div>
                        <div><span class="info-label">Curso:</span> { certificate.course.title }</div>
                        <div><span class="info-label">Horas Totais:</span> { certificate.hours }</div>
                    </div>
                    <div class="footer">
                        Este certificado é uma distinção concedida em reconhecimento ao esforço e realização acadêmica.
                        <br>Código de Verificação: { certificate.student.name.split(' ')[0] }-{ certificate.id }
                    </div>
                </div>
            </div>
        </body>
        </html>
    """

    return html_content
