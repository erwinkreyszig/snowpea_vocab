from vocab.models import PartOfSpeech


pos = [
    PartOfSpeech(code="ADJ", desc="adjective"),
    PartOfSpeech(code="ADP", desc="adposition"),
    PartOfSpeech(code="ADV", desc="adverb"),
    PartOfSpeech(code="AUX", desc="auxiliary"),
    PartOfSpeech(code="CCONJ", desc="coordinating conjunction"),
    PartOfSpeech(code="DET", desc="determiner"),
    PartOfSpeech(code="INTJ", desc="interjection"),
    PartOfSpeech(code="NOUN", desc="noun"),
    PartOfSpeech(code="NUM", desc="numeral"),
    PartOfSpeech(code="PART", desc="particle"),
    PartOfSpeech(code="PRON", desc="pronoun"),
    PartOfSpeech(code="PROPN", desc="proper noun"),
    PartOfSpeech(code="PUNCT", desc="punctuation"),
    PartOfSpeech(code="SCONJ", desc="subordinating conjunction"),
    PartOfSpeech(code="SYM", desc="symbol"),
    PartOfSpeech(code="VERB", desc="verb"),
    PartOfSpeech(code="X", desc="other"),
]

PartOfSpeech.objects.bulk_create(pos)
