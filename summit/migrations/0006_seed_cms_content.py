"""Seed CMS data so the site looks the same after the upgrade.

* Creates TicketType rows for the old hardcoded ticket choices and links any
  existing registrations to them.
* Gives every existing registration a reference number.
* Creates the 'Key Topics' and 'Why Attend' cards that used to be hardcoded
  in templates/summit/home.html.
"""
import secrets

from django.db import migrations

OLD_TICKETS = [
    ('regular', 'Regular Ticket', 1),
    ('vip', 'VIP Ticket', 2),
    ('exhibitor', 'Exhibitor Pass', 3),
]

TOPICS = [
    ('fa-shipping-fast', 'Last-Mile Delivery Innovation',
     'Exploring cutting-edge solutions for efficient last-mile delivery in Nigerian cities.'),
    ('fa-leaf', 'Sustainable Transport',
     'Green logistics solutions and environmentally sustainable transport practices.'),
    ('fa-chart-line', 'Supply Chain Optimization',
     'Advanced strategies for optimizing supply chain operations across West Africa.'),
    ('fa-robot', 'Digital Transformation',
     'AI, IoT, and automation in modern transport and logistics operations.'),
    ('fa-handshake', 'Public-Private Partnerships',
     'Collaborative approaches to infrastructure development and transport solutions.'),
    ('fa-globe-africa', 'Regional Integration',
     'Cross-border transport solutions and African Continental Free Trade Area opportunities.'),
]

WHY_ATTEND = [
    ('fa-network-wired', 'Networking',
     'Connect with industry leaders, decision-makers, and potential business partners '
     'from across Nigeria and West Africa.'),
    ('fa-lightbulb', 'Innovation',
     'Explore cutting-edge technologies, innovative solutions, and emerging trends '
     'in transport and logistics.'),
    ('fa-award', 'Awards',
     "Celebrate excellence in the industry and recognition of outstanding "
     "contributions to Nigeria's transport sector."),
]


def forwards(apps, schema_editor):
    TicketType = apps.get_model('summit', 'TicketType')
    Registration = apps.get_model('summit', 'ConferenceRegistration')
    Highlight = apps.get_model('summit', 'Highlight')

    tickets = {}
    for code, name, order in OLD_TICKETS:
        tickets[code], _ = TicketType.objects.get_or_create(
            code=code, defaults={'name': name, 'order': order, 'price': 0})

    alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    used = set(Registration.objects.exclude(reference=None).values_list('reference', flat=True))
    for reg in Registration.objects.all():
        reg.ticket = tickets.get(reg.ticket_type, tickets['regular'])
        if not reg.reference:
            while True:
                code = 'TLNG-{}-{}'.format(reg.registration_date.year,
                                           ''.join(secrets.choice(alphabet) for _ in range(6)))
                if code not in used:
                    used.add(code)
                    break
            reg.reference = code
        reg.save(update_fields=['ticket', 'reference'])

    if not Highlight.objects.exists():
        for section, rows in (('topics', TOPICS), ('why_attend', WHY_ATTEND)):
            for i, (icon, title, desc) in enumerate(rows, start=1):
                Highlight.objects.create(section=section, icon=icon, title=title,
                                         description=desc, order=i)


def backwards(apps, schema_editor):
    Registration = apps.get_model('summit', 'ConferenceRegistration')
    for reg in Registration.objects.select_related('ticket'):
        if reg.ticket_id:
            reg.ticket_type = reg.ticket.code if reg.ticket.code in dict(
                (c, n) for c, n, _ in OLD_TICKETS) else 'regular'
            reg.save(update_fields=['ticket_type'])


class Migration(migrations.Migration):

    dependencies = [
        ('summit', '0005_cms_gallery_tickets'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
