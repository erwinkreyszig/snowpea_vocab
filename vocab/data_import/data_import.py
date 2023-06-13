import csv
import os
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from vocab.models import RefWordOrPhrase, Language, WordOrPhraseHistory

EXCL = "!!"
QQ = "??"
Q = "?"
csv_path = os.path.join(os.getcwd(), "vocab", "data_import", "as_of_12_jun_2023.csv")
now = timezone.now()
prev_date = None


def clean_pronounciation(pronounciation, is_native):
    pronounciation = pronounciation.replace("*", "")  # remove asterisks
    pronounciation = pronounciation.replace(QQ, "")  # remove ??
    if EXCL in pronounciation:
        pronounciation = pronounciation.replace(EXCL, "")
    return (pronounciation.strip(), is_native != "")


data_dict = {}
with open(csv_path) as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    for i, row in enumerate(reader):
        if i == 0:  # skip first line
            continue
        date_added, ref, english, japanese, tagalog, not_sure, is_native = map(str.strip, row)
        # print(f"{date_added},{ref},{english},{japanese},{tagalog},{not_sure},{is_native}")
        # clean date
        if not date_added:
            date_added = prev_date
        date_obj = datetime.strptime(date_added, "%d %b %Y")
        date_added_obj = now.replace(year=date_obj.year, month=date_obj.month, day=date_obj.day)
        # print(f"{date_added}: {date_added_obj} | {ref}")
        prev_date = date_added
        # clean ref
        if ref == Q:
            continue  # skip ones we weren't sure of
        if not_sure:
            continue  # skip ones we weren't sure of
        # clean pronounciations:
        if english:
            key = (ref, "english")
            english, is_native_bool = clean_pronounciation(english, is_native)
            data_dict.setdefault(key, []).append(
                {"date_added": date_added_obj, "pronounciation": english, "is_native": is_native_bool}
            )
        if japanese:
            key = (ref, "japanese")
            japanese, is_native_bool = clean_pronounciation(japanese, is_native)
            data_dict.setdefault(key, []).append(
                {"date_added": date_added_obj, "pronounciation": japanese, "is_native": is_native_bool}
            )
        if tagalog:
            key = (ref, "tagalog")
            tagalog, is_native_bool = clean_pronounciation(tagalog, is_native)
            data_dict.setdefault(key, []).append(
                {"date_added": date_added_obj, "pronounciation": tagalog, "is_native": is_native_bool}
            )


# from pprint import PrettyPrinter as pp

# pp = pp(indent=2, width=200).pprint
# pp(data_dict)

user = User.objects.get(username="uskar")
lang_dict = {lang.desc.lower(): lang for lang in Language.objects.all()}

for ref_lang_pair, history_list in data_dict.items():
    ref, lang_str = ref_lang_pair
    print(f"processing {ref} ({lang_str})... ", end="")
    lang = lang_dict.get(lang_str)
    # check if ref exists
    new_entry = False
    ref_obj = RefWordOrPhrase.objects.filter(word_or_phrase=ref).first()
    if not ref_obj:
        ref_obj = RefWordOrPhrase.objects.create(word_or_phrase=ref, date_added=now, variation_count=0, added_by=user)
        new_entry = True
    print("record created" if new_entry else "record exists")
    hist_obj_list = []
    for i, item in enumerate(history_list):
        hist_obj = WordOrPhraseHistory(
            ref=ref_obj,
            date_added=item["date_added"],
            language=lang,
            pronounciation=item["pronounciation"],
            is_native=item["is_native"],
            added_by=user,
        )
        print(f"  saved '{item['pronounciation']}'")
        if i == 0 and new_entry:
            ref_obj.date_added = item["date_added"]
        ref_obj.variation_count += len(hist_obj_list)
        ref_obj.save()
        hist_obj_list.append(hist_obj)
    WordOrPhraseHistory.objects.bulk_create(hist_obj_list)
