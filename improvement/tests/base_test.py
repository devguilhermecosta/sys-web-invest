from django.contrib.auth.models import User
from ..models import Improvement


def make_improvement(user: User,
                     title: str,
                     description: str,
                     ) -> Improvement:
    new_improvement = Improvement.objects.create(
        user=user,
        title=title,
        description=description,
        status='enviado',
    )
    new_improvement.save()
    return new_improvement
