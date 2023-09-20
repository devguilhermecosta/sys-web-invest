from django.contrib.auth.models import User
from improvement.models import Improvement
from typing import List
from faker import Faker

fake = Faker()


def make_improvement(user: User,
                     title: str,
                     description: str,
                     status: str,
                     ) -> Improvement:
    '''
        the status attribute must be:
        enviado, em análise, em desenvolvimento, recusado, concluído
    '''
    new_improvement = Improvement.objects.create(
        user=user,
        title=title,
        description=description,
        status=status,
    )
    new_improvement.save()
    return new_improvement


def make_improvements_in_batch(quantity: int) -> List[Improvement]:
    user = User.objects.create(
        username='jhondoe',
        password='123456',
        email='email@email.com',
    )

    improvements = []

    for _ in range(quantity):
        new_improvement = Improvement.objects.create(
            user=user,
            title=fake.text()[:10],
            description=fake.text()[:10],
            status='enviado',
        )
        new_improvement.save()
        improvements.append(new_improvement)

    return improvements
