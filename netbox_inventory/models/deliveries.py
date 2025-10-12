from django.db import models

from netbox.models.features import ContactsMixin

from ..choices import PurchaseStatusChoices
from .mixins import NamedModel

from django.utils.translation import gettext_lazy as _


class Supplier(NamedModel, ContactsMixin):
    """
    Supplier is a legal entity that sold some assets that we keep track of.
    This can be the same entity as Manufacturer or a separate one. However
    netbox_inventory keeps track of Suppliers separate from Manufacturers.
    """

    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    clone_fields = ['description', 'comments']

    class Meta:
        ordering = ['name']

        verbose_name_plural = _('Suppliers')
        verbose_name = _('Supplier')

class Purchase(NamedModel):
    """
    Represents a purchase of a set of Assets from a Supplier.
    """

    name = models.CharField(max_length=100, verbose_name=_('Name'))
    supplier = models.ForeignKey(
        help_text=_('Legal entity this purchase was made at'),
        to='netbox_inventory.Supplier',
        on_delete=models.PROTECT,
        related_name='purchases',
        blank=False,
        null=False,
        verbose_name=_('Supplier'),
    )
    status = models.CharField(
        max_length=30,
        choices=PurchaseStatusChoices,
        help_text=_('Status of purchase'),
        verbose_name=_('Status'),
    )
    date = models.DateField(
        help_text=_('Date when this purchase was made'),
        blank=True,
        null=True,
        verbose_name=_('Date'),
    )

    clone_fields = ['supplier', 'date', 'status', 'description', 'comments']

    class Meta:
        ordering = ['supplier', 'name']

        verbose_name_plural = _('Purchases')
        verbose_name = _('Purchase')

        unique_together = (('supplier', 'name'),)

    def get_status_color(self):
        return PurchaseStatusChoices.colors.get(self.status)

    def __str__(self):
        return f'{self.supplier} {self.name}'


class Delivery(NamedModel):
    """
    Delivery is a stage in Purchase. Purchase can have multiple deliveries.
    In each Delivery one or more Assets were delivered.
    """

    name = models.CharField(max_length=100, verbose_name=_('Name'))
    purchase = models.ForeignKey(
        help_text=_('Purchase that this delivery is part of'),
        to='netbox_inventory.Purchase',
        on_delete=models.PROTECT,
        related_name='orders',
        blank=False,
        null=False,
        verbose_name=_('Purchase'),
    )
    date = models.DateField(
        help_text=_('Date when this delivery was made'),
        blank=True,
        null=True,
        verbose_name=_('Date'),
    )
    receiving_contact = models.ForeignKey(
        help_text=_('Contact that accepted this delivery'),
        to='tenancy.Contact',
        on_delete=models.PROTECT,
        related_name='deliveries',
        blank=True,
        null=True,
        verbose_name=_('Receiving Contact'),
    )

    clone_fields = ['purchase', 'date', 'receiving_contact', 'description', 'comments']

    class Meta:
        ordering = ['purchase', 'name']
        unique_together = (('purchase', 'name'),)
        
        verbose_name = _('delivery')
        verbose_name_plural = _('deliveries')

    def __str__(self):
        return f'{self.purchase} {self.name}'
