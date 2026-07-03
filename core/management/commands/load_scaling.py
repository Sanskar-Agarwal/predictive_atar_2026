"""
Reload the VIC and WA scaling tables from their source CSVs.

Why this exists: NSW scaling is read from CSV at runtime, but VIC (Vic_scaling)
and WA (Wa_scaling) scaling are read from DB tables. The CSVs in
core/source/scaling_csv/ are the source of truth; this command (re)loads them
into the DB so the data is reproducible — instead of depending on the committed
db.sqlite3 binary staying in sync by hand.

Idempotent: clears each table and recreates it from the CSV. Run on a fresh
setup (it's wired into the Docker startup) or any time the CSVs change:

    python manage.py load_scaling
"""

import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from core.models import Region, Subject, Tas_scaling_alt, Vic_scaling, Wa_scaling

# project_root/core/management/commands/load_scaling.py -> parents[3] = project root
SOURCE_DIR = Path(__file__).resolve().parents[3] / "core" / "source"
SCALING_DIR = SOURCE_DIR / "scaling_csv"
NEW_SUBJECTS_CSV = SOURCE_DIR / "new_subjects.csv"


def _none_if_blank(value):
    value = (value or "").strip()
    return value or None


class Command(BaseCommand):
    help = "Reload VIC and WA scaling tables from their source CSVs."

    def handle(self, *args, **options):
        self._load_vic()
        self._load_wa()
        self._load_tas()
        self._ensure_subjects()

    def _load_tas(self):
        path = SCALING_DIR / "tas_scaling_alt.csv"
        if not path.exists():
            return
        cols = ["sa_min", "sa_max", "ca_min", "ca_max", "ha_min", "ha_max", "ea_min", "ea_max"]
        rows = list(csv.reader(open(path, encoding="utf-8-sig")))[1:]  # header: course, sa_min, ...
        Tas_scaling_alt.objects.all().delete()
        objs = [
            Tas_scaling_alt(id=i, course=_none_if_blank(r[0]), **{c: _none_if_blank(r[j + 1]) for j, c in enumerate(cols)})
            for i, r in enumerate(rows)
        ]
        Tas_scaling_alt.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(objs)} Tas_scaling_alt rows from {path.name}"))

    def _ensure_subjects(self):
        """Add subjects that exist in the refreshed scaling tables but were missing
        from the Subject list, and fix a name with an embedded newline. Idempotent."""
        # Fix the NSW name with a stray newline so it matches the scaling table.
        n = Subject.objects.filter(subject="Information & Digital Technology\nExam").update(
            subject="Information & Digital Technology Exam"
        )
        if n:
            self.stdout.write(self.style.SUCCESS(f"Fixed {n} NSW subject name (stray newline)"))

        if not NEW_SUBJECTS_CSV.exists():
            return
        last = Subject.objects.order_by("-id").first()
        next_id = (last.id if last else 0) + 1
        added = 0
        for row in csv.DictReader(open(NEW_SUBJECTS_CSV, encoding="utf-8-sig")):
            region = Region.objects.get(abbreviation=row["region"].strip())
            name = row["subject"].strip()
            if Subject.objects.filter(subject=name, regionid=region).exists():
                continue
            Subject.objects.create(
                id=next_id,
                subject=name,
                units=row["units"].strip(),
                category=row["category"].strip(),
                regionid=region,
                is_language=(row["is_language"].strip() == "True") or None,
            )
            next_id += 1
            added += 1
        self.stdout.write(self.style.SUCCESS(f"Ensured new subjects (added {added})"))

    def _load_vic(self):
        path = SCALING_DIR / "vic_scaling.csv"
        rows = list(csv.reader(open(path, encoding="utf-8-sig")))[1:]  # skip header
        Vic_scaling.objects.all().delete()
        objs = [
            Vic_scaling(
                id=i,
                study_code=_none_if_blank(r[0]),
                study_name=_none_if_blank(r[1]),
                mean=_none_if_blank(r[2]),
                sd=_none_if_blank(r[3]),
                scaled_score_20=_none_if_blank(r[4]),
                scaled_score_25=_none_if_blank(r[5]),
                scaled_score_30=_none_if_blank(r[6]),
                scaled_score_35=_none_if_blank(r[7]),
                scaled_score_40=_none_if_blank(r[8]),
                scaled_score_45=_none_if_blank(r[9]),
                scaled_score_50=_none_if_blank(r[10]),
                category=_none_if_blank(r[11]),
                group=_none_if_blank(r[12]),
            )
            for i, r in enumerate(rows)
        ]
        Vic_scaling.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(objs)} Vic_scaling rows from {path.name}"))

    def _load_wa(self):
        path = SCALING_DIR / "wa_scaling.csv"
        rows = list(csv.reader(open(path, encoding="utf-8-sig")))[1:]  # skip header: course,mean,min_mark,max_mark
        Wa_scaling.objects.all().delete()
        objs = [
            Wa_scaling(
                id=i,
                course=_none_if_blank(r[0]),
                mean=_none_if_blank(r[1]),
                min_mark=_none_if_blank(r[2]),
                max_mark=_none_if_blank(r[3]),
            )
            for i, r in enumerate(rows)
        ]
        Wa_scaling.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(objs)} Wa_scaling rows from {path.name}"))
