import pytz
from snowpea_vocab.settings import TIME_ZONE
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MainForm
from django.utils import timezone
from django.http import JsonResponse
from .models import RefWordOrPhrase, Language, WordOrPhraseHistory

# Create your views here.

DATE_FORMAT = "%Y-%m-%d"


@login_required
def main(request):
    if request.method == "GET":
        return render(
            request,
            "main.html",
            context={
                "form": MainForm(initial={"date_added": timezone.now().strftime(DATE_FORMAT), "is_native": False}),
                "username": request.user.username,
            },
        )
    # process sent data
    date_added = request.POST["date_added"]
    word_or_phrase = request.POST["word_or_phrase"].strip()
    language = request.POST["language"]
    pronounciation = request.POST["pronounciation"].strip()
    is_native = request.POST["is_native"]
    now = timezone.now()
    created = added = False
    # setup Language objects
    lang_dict = {lang.code: lang for lang in Language.objects.all()}
    # break down date_added
    year, month, day = [int(num) for num in date_added.split("-", 2)]
    date_added = now.replace(year=year, month=month, day=day)
    # check if word_or_phrase is already in the db
    kwargs_for_history = {
        "date_added": date_added,
        "language": lang_dict.get(language),
        "pronounciation": pronounciation,
        "is_native": is_native,
        "added_by": request.user,
    }
    if ref := RefWordOrPhrase.objects.filter(word_or_phrase__iexact=word_or_phrase).first():
        history_found = ref.wordorphrasehistory_set.filter(
            pronounciation__icontains=pronounciation, language=lang_dict.get(language)
        )
        if not history_found:  # create a history entry
            kwargs_for_history["ref"] = ref
            WordOrPhraseHistory.objects.create(**kwargs_for_history)
            added = True
            ref.variation_count += 1
            ref.save()
    else:
        ref = RefWordOrPhrase.objects.create(
            word_or_phrase=word_or_phrase, date_added=date_added, variation_count=1, added_by=request.user
        )
        created = True
        # create a history entry
        kwargs_for_history["ref"] = ref
        WordOrPhraseHistory.objects.create(**kwargs_for_history)
    # prepare response
    # pull history for ref
    history = (
        WordOrPhraseHistory.objects.filter(ref=ref)
        .order_by("language", "date_added")
        .values("date_added", "language__desc", "pronounciation", "is_native")
    )
    # localize date_added
    for item in history:
        item["date_added"] = item["date_added"].astimezone(pytz.timezone(TIME_ZONE)).strftime("%d %b, %Y %H:%M:%S")
    resp = {
        "created": created,
        "added": added,
        "found": False,
        "history": list(history),
        "ref_data": {
            "date_added": ref.date_added,
            "count": ref.variation_count,
            "word_or_phrase": ref.word_or_phrase,
            "pronounciation": pronounciation,
        },
    }
    return JsonResponse(resp)


@login_required
def find_word(request):
    if request.method == "GET":
        query_str = request.GET["query"]
        if ref := RefWordOrPhrase.objects.filter(word_or_phrase__iexact=query_str).first():
            history = (
                WordOrPhraseHistory.objects.filter(ref=ref)
                .order_by("language", "date_added")
                .values("date_added", "language__desc", "pronounciation", "is_native")
            )
            resp = {
                "created": False,
                "added": False,
                "found": True,
                "history": list(history),
                "ref_data": {
                    "date_added": ref.date_added,
                    "count": ref.variation_count,
                    "word_or_phrase": ref.word_or_phrase,
                    "pronounciation": "",
                },
            }
            return JsonResponse(resp)
        return JsonResponse(
            {"created": False, "added": False, "found": False, "ref_data": {"word_or_phrase": query_str}}
        )


@login_required
def get_word_counts(request):
    if request.method == "GET":
        # for now
        counts = {}
        for lang_code in ("en", "ja", "fl"):
            counts[lang_code] = (
                WordOrPhraseHistory.objects.filter(language__code=lang_code)
                .values("ref__word_or_phrase")
                .order_by("ref__word_or_phrase")
                .distinct()
                .count()
            )
        return JsonResponse(counts)
