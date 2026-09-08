from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from appointments.models import Appointment, Doctor, Patient


class Command(BaseCommand):
    help = 'Populate the database with sample patients, doctors, and appointments.'

    def handle(self, *args, **options):
        doctors = [
            Doctor.objects.get_or_create(first_name='Greg', last_name='House', specialty='Diagnostics')[0],
            Doctor.objects.get_or_create(first_name='Lisa', last_name='Cuddy', specialty='Endocrinology')[0],
            Doctor.objects.get_or_create(first_name='James', last_name='Wilson', specialty='Oncology')[0],
        ]

        patients = [
            Patient.objects.get_or_create(
                first_name='Jane', last_name='Doe', date_of_birth='1990-01-15',
                defaults={'email': 'jane.doe@example.com', 'phone_number': '555-0101'},
            )[0],
            Patient.objects.get_or_create(
                first_name='John', last_name='Smith', date_of_birth='1985-06-30',
                defaults={'email': 'john.smith@example.com', 'phone_number': '555-0102'},
            )[0],
            Patient.objects.get_or_create(
                first_name='Alice', last_name='Johnson', date_of_birth='2000-11-02',
                defaults={'email': 'alice.johnson@example.com', 'phone_number': '555-0103'},
            )[0],
        ]

        now = timezone.now().replace(minute=0, second=0, microsecond=0)
        sample_appointments = [
            (patients[0], doctors[0], now + timedelta(days=1, hours=9), 'Annual checkup', Appointment.Status.SCHEDULED),
            (patients[1], doctors[1], now + timedelta(days=2, hours=11), 'Follow-up', Appointment.Status.SCHEDULED),
            (patients[2], doctors[2], now - timedelta(days=3, hours=-14), 'Consultation', Appointment.Status.COMPLETED),
            (patients[0], doctors[2], now + timedelta(days=5, hours=15), 'Second opinion', Appointment.Status.CANCELLED),
        ]

        created = 0
        for patient, doctor, scheduled_at, reason, status in sample_appointments:
            _, was_created = Appointment.objects.get_or_create(
                patient=patient, doctor=doctor, scheduled_at=scheduled_at,
                defaults={'reason': reason, 'status': status},
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(doctors)} doctors, {len(patients)} patients, {created} new appointments.'
        ))
