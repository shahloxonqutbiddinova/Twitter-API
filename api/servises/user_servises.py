from api.models import User
from api.models.user import VERIFIED


def verify_user(user, code):
    confirmation = user.confirmations.order_by("-created_at").first()

    if not confirmation:
        return False

    if confirmation.is_expired():
        return False

    if confirmation.code != code:
        return False

    user.status = VERIFIED
    user.save()

    user.confirmations.all().delete()
    return True