from django.urls import reverse
from utils.mixins.auth import TestCaseWithLogin


class ActionsHistoryDeleteTests(TestCaseWithLogin):
    url = reverse(
        'product:actions_history_delete',
        kwargs={
            'p_id': 1,
            'h_id': 1,
        })
