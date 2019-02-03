from . import models
from django.core.exceptions import ObjectDoesNotExist

def validate_users(pks):
    """
    Given a list of user PKs, verify that they exist.
    If they do, return True, list of user objects.
    Else, return False, [failed_pk]
    :param pks: 
    :return: Status, Users (In fail case, Users is 1 pk that failed)
    """
    verified = []
    for pk in pks:
        try:
            user = models.CustomUser.objects.get(pk=pk)
            verified.append(user)
        except ObjectDoesNotExist:
            return False, [pk]
    return True, verified
