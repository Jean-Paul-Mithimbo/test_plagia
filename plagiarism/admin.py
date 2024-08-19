from django.contrib import admin
from .models import Document, UserDocument, PlagiarismCheckHistory

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    readonly_fields = ('content',)

class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    readonly_fields = ('content',)

class PlagiarismCheckHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_document', 'similarity_score', 'matched_document', 'checked_at')

admin.site.register(Document, DocumentAdmin)
admin.site.register(UserDocument, UserDocumentAdmin)
admin.site.register(PlagiarismCheckHistory, PlagiarismCheckHistoryAdmin)
