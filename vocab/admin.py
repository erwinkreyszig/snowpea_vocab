from django.contrib import admin
from .models import RefWordOrPhrase, Language, WordOrPhraseHistory

# Register your models here.


class WordOrPhraseHistoryInline(admin.TabularInline):
    model = WordOrPhraseHistory
    extra = 1


@admin.register(RefWordOrPhrase)
class RefWordOrPhraseAdmin(admin.ModelAdmin):
    list_display = ("word_or_phrase", "date_added", "variation_count")
    inlines = [WordOrPhraseHistoryInline]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "desc")
    # list_editable = ("code", "desc")


admin.site.register(WordOrPhraseHistory)
