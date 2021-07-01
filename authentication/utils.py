from django.core.mail import EmailMessage

TITLE = [
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Ms', 'Ms'),
    ('Dr', 'Dr'),
]

EXPERTISE = [
    ('UI/UX Design', 'UI/UX Design'),
    ('Product Design', 'Product Design'),
    ('AI Design', 'AI Design'),
]

MENTORSHIP_AREAS = [
    ('Career Advice', 'Career Advice'),
    ('Portfolio Review', 'Portfolio Review'),
    ('Interview Techniques', 'Interview Techniques'),
]

USER_TYPE = [('mentor', 'mentor'), ('member', 'member')]

MENTOR_STATUS = [('n/a', 'not applicable'), ('pending', 'pending'),
                 ('approved', 'approved'), ('denied', 'denied')]


class Util:

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=(data['to_email'],))
        email.send()
