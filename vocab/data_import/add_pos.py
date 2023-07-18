from vocab.models import PartOfSpeech, Language


pos = [
    PartOfSpeech(code="VERB", desc="Verb", languages="en,ja,fl"),
    PartOfSpeech(code="NOUN", desc="Noun", languages="en,ja,fl"),
    PartOfSpeech(code="ADJ", desc="Adjective", languages="en,ja,fl"),
    PartOfSpeech(code="ADV", desc="Adverb", languages="ene,ja,fl"),
    PartOfSpeech(code="PRON", desc="Pronoun", languages="en,ja,fl"),
    PartOfSpeech(code="PREP", desc="Preposition", languages="en,fl"),
    PartOfSpeech(code="CONJ", desc="Conjunction", languages="en,ja,fl"),
    PartOfSpeech(code="INTR", desc="Interjection", languages="en,ja"),
    PartOfSpeech(code="ADVR", desc="Adjectival Verb", languages="ja"),
    PartOfSpeech(code="PART", desc="Particle", languages="ja"),
    PartOfSpeech(code="AUXV", desc="Auxiliary Verb", languages="ja"),
    PartOfSpeech(code="ATTR", desc="Attributive", languages="ja"),
    PartOfSpeech(code="MRKR", desc="Marker", languages="fl"),
]

PartOfSpeech.objects.bulk_create(pos)
