from django.db import models
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='documents/')
    content = models.TextField(editable=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pdf:
            self.extract_text_from_pdf()
        super(Document, self).save(*args, **kwargs)

    def extract_text_from_pdf(self):
        text = ''
        try:
            # Extraction du texte avec PyPDF2
            pdf_reader = PyPDF2.PdfReader(self.pdf)
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text

            # Si aucun texte n'est extrait, utiliser l'OCR
            if not text:
                images = convert_from_path(self.pdf.path)
                for image in images:
                    text += pytesseract.image_to_string(image)

        except Exception as e:
            print(f"Erreur lors de l'extraction du texte du PDF: {e}")

        self.content = text

    def __str__(self):
        return self.title


class UserDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='user_documents/')
    content = models.TextField(editable=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pdf:
            self.extract_text_from_pdf()
        super(UserDocument, self).save(*args, **kwargs)

    def extract_text_from_pdf(self):
        text = ''
        try:
            # Extraction du texte avec PyPDF2
            pdf_reader = PyPDF2.PdfReader(self.pdf)
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text

            # Si aucun texte n'est extrait, utiliser l'OCR
            if not text:
                images = convert_from_path(self.pdf.path)
                for image in images:
                    text += pytesseract.image_to_string(image)

        except Exception as e:
            print(f"Erreur lors de l'extraction du texte du PDF: {e}")

        self.content = text

    def __str__(self):
        return self.title


class PlagiarismCheckHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_document = models.ForeignKey(UserDocument, on_delete=models.CASCADE)
    similarity_score = models.FloatField()
    matched_document = models.ForeignKey(Document, on_delete=models.CASCADE)
    checked_at = models.DateTimeField(auto_now_add=True)
