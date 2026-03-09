import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import EmailVerificationCode


def generate_code():
    """6 орундуу рандом код"""
    return str(random.randint(100000, 999999))


def send_verification_email(user):
    """Колдонуучунун emailine код жөнөтүү"""

    # Эски коддорду өчүрүү
    EmailVerificationCode.objects.filter(user=user, is_used=False).delete()

    # Жаңы код жасоо
    code = generate_code()
    EmailVerificationCode.objects.create(user=user, code=code)

    # Email жөнөтүү
    send_mail(
        subject='TRIDE — Тастыктоо коду',
        message=f'Салам, {user.first_name}!\n\nСиздин код: {code}\n\nКод 10 мүнөт ичинде жарактуу.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def verify_code(email, code):
    """Кодду текшерүү — (True, user) же (False, None) кайтарат"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        user = User.objects.get(email=email)

        # Акыркы 10 мүнөттөгү код
        time_limit = timezone.now() - timedelta(minutes=10)

        verification = EmailVerificationCode.objects.filter(
            user=user,
            code=code,
            is_used=False,
            created_at__gte=time_limit
        ).last()

        if verification:
            verification.is_used = True
            verification.save()
            return True, user

        return False, None

    except Exception:
        return False, None