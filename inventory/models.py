from django.db import models


class Bag(models.Model):
    # Collection of compartments/pockets/pouches, see class Compartments for content.
    # May also hold loose items (optional) for single space bags (no compartmentalization).
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40,
                             blank=True,
                             null=True)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    def __str__(self):
        return self.name


class BagCompartment(models.Model):
    # Section of the bag that holds items and other kits.
    # For example "Main Top Compartment", "Top Outside Pouch", etc.
    name = models.CharField(max_length=40)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)
    bag = models.ForeignKey(Bag,
                            blank=True,
                            null=True,
                            on_delete=models.CASCADE)
    items = models.ManyToManyField('Item',
                                   blank=True,
                                   null=True)

    def get_bag_name(self):
        try:
            bag_name = self.bag.name
            return bag_name
        except AttributeError:
            return "Not Yet Assigned To Any Bags"

    def __str__(self):
        return '{} _in_ {}'.format(self.name, self.get_bag_name())


class Kit(models.Model):
    # Collection of items combined in a single case/box/carrier to tackle particular function
    # For example "Glucometer Kit", "Airway Kit", "Suction Unit", "IV Kit", "AirTraq", etc.
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40,
                             blank=True,
                             null=True)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)
    bag_compartment = models.ForeignKey(BagCompartment,
                                        blank=True,
                                        null=True,
                                        on_delete=models.CASCADE)
    items = models.ManyToManyField('Item',
                                   blank=True,
                                   null=True)

    def get_bag_compartment_name(self):
        try:
            bag_compartment_name = self.bag_compartment.name
            return bag_compartment_name
        except AttributeError:
            return "Not Yet Assigned to Any Bag Compartments"

    def get_bag_name(self):
        try:
            bag_compartment = self.bag_compartment
            bag_name = bag_compartment.get_bag_name()
            return bag_name
        except AttributeError:
            # Exception also being caught in BagCompartment.get_bag_name()
            return "Not Yet Assigned To Any Bags"

    def __str__(self):
        return '{} _in_ {} >> {}'.format(self.name, self.get_bag_name(), self.get_bag_compartment_name())


class KitCompartment(models.Model):
    # Section of the kit that holds items.
    # For example "Pocket Under Blades", "Pocket Under Syringes", etc.
    name = models.CharField(max_length=40)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)
    kit = models.ForeignKey(Kit,
                            blank=True,
                            null=True,
                            on_delete=models.CASCADE)
    items = models.ManyToManyField('Item',
                                   blank=True,
                                   null=True)

    def get_kit_name(self):
        try:
            return self.kit.name
        except AttributeError:
            return "Not Yet Assigned to Any Kits"


class Item(models.Model): #TODO does not need to be a Container
    # Single resource
    # For example "Band Aid", "Syringe", etc.
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40,
                             blank=True,
                             null=True)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)
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

# TODO add Device class for Monitor X Series
