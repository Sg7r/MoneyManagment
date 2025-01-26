from celery import shared_task
from .models import Wallet


@shared_task
def delete_anonymous_records(records_to_delete):
    anonymous_records = Wallet.objects.filter(id__in=records_to_delete)
    deleted_count, _ = anonymous_records.delete()  # Возвращает количество удаленных записей

    return f"{deleted_count} anonymous records deleted"
