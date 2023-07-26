from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PartOfSpeech(models.Model):
    """Lists parts of speech for the languages involved"""

    code = models.CharField(max_length=10, unique=True)
    desc = models.CharField(max_length=255)
    languages = models.CharField(max_length=255, default=None, null=True)

    class Meta:
        ordering = ["code"]
        verbose_name_plural = "parts of speech"

    def __str__(self):
        return f"{self.code} - {self.desc} ({self.languages})"


class RefWordOrPhrase(models.Model):
    """Model that will hold the reference word or phrase"""

    word_or_phrase = models.CharField(max_length=255, help_text="What Snowpea likely meant")
    date_added = models.DateTimeField(auto_now_add=True)
    variation_count = models.IntegerField(default=0)
    part_of_speech = models.ForeignKey(PartOfSpeech, on_delete=models.SET_NULL, null=True, default=None)
    base = models.ForeignKey("RefWordOrPhrase", on_delete=models.SET_NULL, null=True, default=None, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["word_or_phrase"]
        unique_together = ("word_or_phrase", "part_of_speech")

    def __str__(self):
        return f"{self.word_or_phrase} - {self.date_added} ({self.variation_count})"


class Language(models.Model):
    """Stores a language"""

    code = models.CharField(max_length=2, unique=True)
    desc = models.CharField(max_length=100)

    class Meta:
        ordering = ["desc"]

    def __str__(self):
        return self.desc


class WordOrPhraseHistory(models.Model):
    """Records pronounciation variation for words in all languages"""

    ref = models.ForeignKey(RefWordOrPhrase, on_delete=models.RESTRICT)
    date_added = models.DateTimeField()
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    pronounciation = models.TextField(null=True, blank=True)
    is_native = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["ref__word_or_phrase", "language", "date_added"]

    def __str__(self):
        return f"{self.ref.word_or_phrase} - {self.language.desc} - {self.date_added} - {self.pronounciation}"
