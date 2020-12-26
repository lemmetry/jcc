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

    def get_bag_name(self):
        try:
            bag_name = self.bag.name
            return bag_name
        except AttributeError:
            return "Not Yet Assigned To Any Bags"

    def __str__(self):
        return '{} _in_ {}'.format(self.name, self.get_bag_name())


class BagCompartmentToItemAssociation(models.Model):
    # Defines quantity of the item in the bag compartment.
    # Example: 'Bio-Hazard Bag, Large' x2 in 'Center Pocket'.
    bag_compartment = models.ForeignKey(BagCompartment,
                                        blank=True,
                                        null=True,
                                        on_delete=models.CASCADE)
    item = models.ForeignKey('Item',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    def __str__(self):
        item_details = self.item.name

        if self.item.size:
            item_details = '{}, {}'.format(item_details, self.item.size)
        item_details = '{} (x{})' .format(item_details, self.quantity)

        return '{} in {}'.format(item_details, self.bag_compartment.name)

    class Meta:
        verbose_name = "Bag Compartment to Item Association"


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


class KitToItemAssociation(models.Model):
    # Defines quantity of the item in the kit.
    # Example: 'Protective Lancet' x10 in 'Glucometer Kit'.
    kit = models.ForeignKey(Kit,
                            blank=True,
                            null=True,
                            on_delete=models.CASCADE)
    item = models.ForeignKey('Item',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    def __str__(self):
        item_details = self.item.name

        if self.item.size:
            item_details = '{}, {}'.format(item_details, self.item.size)
        item_details = '{} (x{})' .format(item_details, self.quantity)

        return '{} in {}'.format(item_details, self.kit.name)

    class Meta:
        verbose_name = "Kit to Item Association"


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

    def get_kit_name(self):
        try:
            return self.kit.name
        except AttributeError:
            return "Not Yet Assigned to Any Kits"

    def __str__(self):
        return '{} _in_ {}'.format(self.name, self.get_kit_name())


class KitCompartmentToItemAssociation(models.Model):
    # Defines quantity of the item in the kit compartment.
    # Example: 'Lubricant, Single Use' x4 in 'ETT Side'.
    kit_compartment = models.ForeignKey(KitCompartment,
                                        blank=True,
                                        null=True,
                                        on_delete=models.CASCADE)
    item = models.ForeignKey('Item',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    def __str__(self):
        item_details = self.item.name

        if self.item.size:
            item_details = '{}, {}'.format(item_details, self.item.size)
        item_details = '{} (x{})' .format(item_details, self.quantity)

        return '{} in {}'.format(item_details, self.kit_compartment.name)

    class Meta:
        verbose_name = "Kit Compartment to Item Association"


class Item(models.Model):
    # Single resource
    # For example "Band Aid", "Syringe", etc.
    name = models.CharField(max_length=40)
    size = models.CharField(max_length=40,
                            blank=True)
    brand = models.CharField(max_length=40,
                             blank=True,
                             null=True)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)
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
