from django.contrib import admin
from .models import RefWordOrPhrase, Language, WordOrPhraseHistory, PartOfSpeech

# Register your models here.


class WordOrPhraseHistoryInline(admin.TabularInline):
    model = WordOrPhraseHistory
    extra = 1


@admin.register(RefWordOrPhrase)
class RefWordOrPhraseAdmin(admin.ModelAdmin):
    list_display = ("word_or_phrase", "pos_desc", "base_ref", "date_added", "variation_count")
    inlines = [WordOrPhraseHistoryInline]

    @admin.display(empty_value="---")
    def pos_desc(self, obj):
        return obj.part_of_speech.desc if obj.part_of_speech else "---"

    @admin.display(empty_value="---")
    def base_ref(self, obj):
        return obj.base.word_or_phrase if obj.base else "---"


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "desc")


admin.site.register(WordOrPhraseHistory)
admin.site.register(PartOfSpeech)
