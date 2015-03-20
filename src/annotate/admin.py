from django.contrib import admin
from annotate.models import TextSnippit, Token, Sentence

class TextSnippitAdmin(admin.ModelAdmin):
    pass
class TokenAdmin(admin.ModelAdmin):
    pass
class SentenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(TextSnippit, TextSnippitAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Sentence, SentenceAdmin)