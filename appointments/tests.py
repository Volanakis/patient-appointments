from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Appointment, Doctor, Patient


class AppointmentModelTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(first_name='Jane', last_name='Doe', date_of_birth='1990-01-01')
        self.doctor = Doctor.objects.create(first_name='Greg', last_name='House', specialty='Diagnostics')

    def test_double_booking_rejected(self):
        when = timezone.now() + timedelta(days=1)
        Appointment.objects.create(patient=self.patient, doctor=self.doctor, scheduled_at=when)
        other_patient = Patient.objects.create(first_name='John', last_name='Smith', date_of_birth='1985-05-05')
        clashing = Appointment(patient=other_patient, doctor=self.doctor, scheduled_at=when)
        with self.assertRaises(ValidationError):
            clashing.full_clean()


class AppointmentViewTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(first_name='Jane', last_name='Doe', date_of_birth='1990-01-01')
        self.doctor = Doctor.objects.create(first_name='Greg', last_name='House', specialty='Diagnostics')

    def test_create_and_list_appointment(self):
        when = timezone.now() + timedelta(days=1)
        response = self.client.post(reverse('appointments:appointment_create'), {
            'patient': self.patient.pk,
            'doctor': self.doctor.pk,
            'scheduled_at': when.strftime('%Y-%m-%dT%H:%M'),
            'reason': 'Checkup',
            'status': Appointment.Status.SCHEDULED,
            'notes': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 1)

        response = self.client.get(reverse('appointments:appointment_list'))
        self.assertContains(response, 'Jane Doe')
        self.assertContains(response, 'Checkup')

    def test_cancel_appointment(self):
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            scheduled_at=timezone.now() + timedelta(days=1),
        )
        response = self.client.post(reverse('appointments:appointment_cancel', args=[appointment.pk]))
        self.assertEqual(response.status_code, 302)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, Appointment.Status.CANCELLED)
