import csv
from django.db.models import F, Value
from django.utils import timezone
from vocab.models import WordOrPhraseHistory


field_names = [
    "ref_",
    "ref_date_added",
    "ref_added_by",
    "lang_code",
    "date_added",
    "pronounciation",
    "is_native",
    "added_by_user",
]
rows = (
    WordOrPhraseHistory.objects.annotate(
        ref_=F("ref__word_or_phrase"),
        ref_date_added=F("ref__date_added"),
        ref_added_by=F("ref__added_by__username"),
        lang_code=F("language__code"),
        added_by_user=F("added_by__username"),
        pos=Value(""),
        lemma=Value(""),
        base=Value(""),
    )
    .values(*field_names)
    .order_by("ref_", "lang_code", "ref_date_added", "date_added")
)

now = timezone.now()
with open(f"{now.strftime('%Y-%m-%d_%H%M%S')}_export.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=field_names + ["pos", "lemma", "base"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
