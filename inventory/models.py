from django.db import models


class ContainerCommonInfo(models.Model):
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40,
                             blank=True,
                             null=True)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    class Meta:
        abstract = True
        ordering = ['name']


class Item(ContainerCommonInfo):
    # Single resource
    # For example "Band Aid", "Syringe", etc.

    size = models.CharField(max_length=40,
                            blank=True)
    notes = models.CharField(max_length=60,
                             blank=True)
    HOSPITAL = 'HOSPITAL'
    EMS_COMS = 'EMS_COMS'
    SUPPLIED_BY_CHOICES = [
        (HOSPITAL, 'Hospital'),
        (EMS_COMS, 'EMS Coms'),
    ]
    supplied_by = models.CharField(max_length=10,
                                   choices=SUPPLIED_BY_CHOICES,
                                   default=HOSPITAL)

    def __str__(self):
        item_details = self.name

        if self.brand:
            item_details = '{} by {}'.format(item_details, self.brand)
        if self.size:
            item_details = '{}, {}'.format(item_details, self.size)
        if self.notes:
            item_details = '{} ({})'.format(item_details, self.notes)

        return item_details

    class Meta:
        ordering = ['name', 'size']


class Compartment(ContainerCommonInfo):
    # Section of the bag or kit that holds items and other kits.
    # For example "Front Outside Pocket", "Pocket Under Blades", etc.

    pass


class Kit(ContainerCommonInfo):
    # Collection of items combined in a single case/box/carrier to tackle particular function
    # For example "Glucometer Kit", "Airway Kit", "Suction Unit", "IV Kit", "AirTraq", etc.

    pass


class Bag(ContainerCommonInfo):
    # Collection of compartments/pockets/pouches, see class Compartments for content.
    # May also hold loose items (optional) for single space bags (no compartmentalization).

    def __str__(self):
        return self.name

# TODO add Device class for Monitor X Series
