import datetime

from payment.models import Reserve


def delete_expiring_reservations():
    five_days_later = datetime.date.today() + datetime.timedelta(days=5)
    reservations_to_delete = Reserve.objects.filter(session__date__lt=five_days_later)

    for reservation in reservations_to_delete:
        session = reservation.session
        session.is_reserved = False
        session.save()
        reservation.delete()

    print(f"Deleted {reservations_to_delete.count()} reservations expiring within 5 days.")
