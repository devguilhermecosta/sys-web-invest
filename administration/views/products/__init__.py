# flake8: noqa

from .product_register import (
    ActionRegister,
    FIIRegister,
    FIIAutoRegister,
    ActionAutoRegister,
    )
from .product_edit import ActionUpdate, FIIUpdate
from .product_delete import ActionDelete, FIIDelete
from .prices import ActionsUpdateLastCloseView, FIIsUpdateLastCloseView