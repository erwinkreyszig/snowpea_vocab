from django.contrib import admin
from .models import RefWordOrPhrase, Language, WordOrPhraseHistory, PartOfSpeech

# Register your models here.


class WordOrPhraseHistoryInline(admin.TabularInline):
    model = WordOrPhraseHistory
    extra = 1


@admin.register(RefWordOrPhrase)
class RefWordOrPhraseAdmin(admin.ModelAdmin):
    list_display = ("word_or_phrase", "pos_desc", "date_added", "variation_count")
    inlines = [WordOrPhraseHistoryInline]

    @admin.display(empty_value="---")
    def pos_desc(self, obj):
        return obj.part_of_speech.desc if obj.part_of_speech else "---"


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "desc")


admin.site.register(WordOrPhraseHistory)
admin.site.register(PartOfSpeech)
