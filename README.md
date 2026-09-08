# Patient Appointments

A small Django app for managing patients, doctors, and their appointments.

## Features

- Manage patients (create, list) and doctors (via the Django admin).
- Schedule, edit, and cancel appointments.
- Prevents double-booking the same doctor at the same time.
- Sample data seeding via a management command.

## Getting started

```bash
python -m venv env
source env/bin/activate
pip install django

python manage.py migrate
python manage.py seed_appointments   # optional: populate sample data
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — it redirects to the appointments list at
`/appointments/`. Admin (for managing doctors) is at `/admin/` (run
`python manage.py createsuperuser` first).

## Screens

| Appointments list | New appointment |
| --- | --- |
| ![Appointments list](docs/screenshots/01-appointment-list.png) | ![New appointment form](docs/screenshots/02-new-appointment-form.png) |

| Appointment created | Patients list |
| --- | --- |
| ![Appointment created](docs/screenshots/03-appointment-created.png) | ![Patients list](docs/screenshots/04-patient-list.png) |

| New patient | Patient created |
| --- | --- |
| ![New patient form](docs/screenshots/05-new-patient-form.png) | ![Patient created](docs/screenshots/06-patient-created.png) |

| Cancel confirmation | Appointment cancelled |
| --- | --- |
| ![Cancel confirmation](docs/screenshots/07-cancel-confirm.png) | ![Appointment cancelled](docs/screenshots/08-appointment-cancelled.png) |

## Demo video

A screen recording of the app in use is at [`docs/demo.webm`](docs/demo.webm).
It walks through: scheduling an appointment, editing it (adding notes and
marking it completed), cancelling another appointment, adding a new patient,
and logging into the Django admin to add a doctor. Download or open it
locally to play — GitHub's README renderer doesn't play embedded videos,
only images.

## Project layout

- `appointments/models.py` — `Patient`, `Doctor`, `Appointment` models.
- `appointments/views.py` — list/create/update/cancel views.
- `appointments/management/commands/seed_appointments.py` — sample data seeder.
- `appointments/tests.py` — model and view tests (`python manage.py test appointments`).
