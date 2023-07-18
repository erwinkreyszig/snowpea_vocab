import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from vocab.models import PartOfSpeech, RefWordOrPhrase, Language, WordOrPhraseHistory
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Imports data"

    def add_arguments(self, parser):
        parser.add_argument("file")

    def handle(self, *args, **kwargs):
        self.stdout.write(f"filename: {kwargs.get('file')}")

        data = []
        with open(kwargs.get("file"), "r") as f:
            reader = csv.DictReader(f)
            data.extend(row for row in reader if row["pos"] and row["lemma"])

        now = timezone.now()
        DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

        # data for foreign keys
        users_dict = {user.username: user for user in User.objects.all()}
        lang_dict = {lang.code: lang for lang in Language.objects.all()}
        pos_dict = {pos.desc.lower(): pos for pos in PartOfSpeech.objects.all()}

        for row in data:
            username = row["added_by_user"].strip().lower()
            date_added = row["date_added"].strip()
            date_added_naive = datetime.strptime(date_added.split("+", 1)[0], DT_FORMAT)
            date_added_aware = now.replace(
                **{
                    x: getattr(date_added_naive, x)
                    for x in ("year", "month", "day", "hour", "minute", "second", "microsecond")
                }
            )
            is_native = row["is_native"].strip()
            lang_code = row["lang_code"].strip()
            lemma = row["lemma"].strip().lower()
            pos = row["pos"].strip().lower()
            pronounciation = row["pronounciation"].strip().lower()
            ref = row["ref_"].strip().lower()
            ref_username = row["ref_added_by"].strip().lower()
            ref_date_added = row["ref_date_added"].strip()
            ref_date_added_naive = datetime.strptime(ref_date_added.split("+", 1)[0], DT_FORMAT)
            ref_date_added_aware = now.replace(
                **{
                    x: getattr(ref_date_added_naive, x)
                    for x in ("year", "month", "day", "hour", "minute", "second", "microsecond")
                }
            )
            # check if ref exists
            ref_obj = RefWordOrPhrase.objects.filter(word_or_phrase__iexact=ref).first()
            if not ref_obj:  # create if it doesn't
                ref_obj = RefWordOrPhrase.objects.create(
                    word_or_phrase=ref,
                    date_added=ref_date_added_aware,
                    part_of_speech=pos_dict.get(pos),
                    added_by=users_dict.get(ref_username),
                    variation_count=1,
                )
            else:
                ref_obj.variation_count += 1
                ref_obj.save()
            if ref_obj.word_or_phrase != lemma:  # RefWordOrPhrase.base is null if word is the same as lemma
                base = RefWordOrPhrase.objects.filter(word_or_phrase__iexact=lemma).first()
                if not base:
                    base = RefWordOrPhrase.objects.create(
                        word_or_phrase=lemma,
                        date_added=ref_date_added_aware,
                        part_of_speech=pos_dict.get(pos),  # same as the word?
                        added_by=users_dict.get(ref_username),
                        variation_count=0,
                    )
                ref_obj.base = base
                ref_obj.save()
            WordOrPhraseHistory.objects.create(
                ref=ref_obj,
                date_added=date_added_aware,
                language=lang_dict.get(lang_code),
                pronounciation=pronounciation,
                is_native=is_native == "TRUE",
                added_by=users_dict.get(username),
            )
