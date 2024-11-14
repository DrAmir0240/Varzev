import datetime

from complex.models import Session


def delete_past_sessions():
    today = datetime.date.today()
    past_sessions = Session.objects.filter(date__lt=today, is_reserved=False, is_available=True)

    deleted_count, _ = past_sessions.delete()

    print(f"Deleted {deleted_count} past sessions that were not reserved.")


