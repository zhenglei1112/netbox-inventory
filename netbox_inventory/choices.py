from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet

#
# Assets
#


class AssetStatusChoices(ChoiceSet):
    key = 'Asset.status'

    CHOICES = [
        ('stored', _('stored'), 'green'),
        ('used', _('used'), 'blue'),
        ('under_repair', _('under_repair'), 'yellow'),
        ('retired', _('retired'), 'gray'),
        ('scrapped', _('scrapped'), 'darkgray'),
    ]


class HardwareKindChoices(ChoiceSet):
    CHOICES = [
        ('device', 'Device'),
        ('module', 'Module'),
        ('inventoryitem', 'Inventory Item'),
        ('rack', 'Rack'),
    ]


#
# Deliveries
#


class PurchaseStatusChoices(ChoiceSet):
    key = 'Purchase.status'

    CHOICES = [
        ('open', _('Open'), 'cyan'),
        ('partial', _('Partial'), 'blue'),
        ('closed', _('Closed'), 'green'),
    ]
