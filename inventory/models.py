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


class Kit(ContainerCommonInfo):
    # Glucometer Kit, Airway Kit, Suction Unit, IV Kit, AirTraq
    items = models.ManyToManyField(Item,
                                   through='KitItemAssociation')

    def __str__(self):
        return self.name


class Compartment(ContainerCommonInfo):
    items = models.ManyToManyField(Item,
                                   through='CompartmentItemAssociation')
    kits = models.ManyToManyField(Kit,
                                  through='CompartmentKitAssociation',
                                  blank=True)
    notes = models.CharField(max_length=60,
                             blank=True)

    def __str__(self):
        return '({}) {}'.format(self.notes, self.name)


class Bag(ContainerCommonInfo):
    compartments = models.ManyToManyField(Compartment,
                                          through='BagCompartmentAssociation')

    def get_bag_items(self):
        models_to_visit = [self]
        bag_items = []
        while len(models_to_visit) > 0:
            model_to_visit = models_to_visit.pop()

            if isinstance(model_to_visit, Bag):
                # Bag may have Compartments
                bag_compartments = model_to_visit.bagcompartmentassociation_set.all()
                for bag_compartment in bag_compartments:
                    models_to_visit.append(bag_compartment.compartment)
            elif isinstance(model_to_visit, Compartment):
                # Compartment may have Items and/or ...
                compartment_items = model_to_visit.compartmentitemassociation_set.all()
                for compartment_item in compartment_items:
                    bag_items.append(compartment_item.item)

                # ... Compartment may have Kits
                compartment_kits = model_to_visit.compartmentkitassociation_set.all()
                for compartment_kit in compartment_kits:
                    models_to_visit.append(compartment_kit.kit)
            elif isinstance(model_to_visit, Kit):
                # Kit may have Items and/or ...
                kit_items = model_to_visit.kititemassociation_set.all()
                for kit_item in kit_items:
                    bag_items.append(kit_item.item)

                # ... Kit may have Compartments
                kit_compartments = model_to_visit.kitcompartmentassociation_set.all()
                for kit_compartment in kit_compartments:
                    models_to_visit.append(kit_compartment.compartment)
            elif isinstance(model_to_visit, Item):
                bag_items.append(model_to_visit)
            else:
                raise Exception('You... shall... not... pass!')

        return bag_items

    def __str__(self):
        return self.name


class KitCompartmentAssociation(models.Model):
    kit = models.ForeignKey(Kit,
                            on_delete=models.CASCADE)
    compartment = models.ForeignKey(Compartment,
                                    on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    def __str__(self):
        return '{}: {}'.format(self.kit.name, self.compartment.name)

    class Meta:
        verbose_name = "Kit-Compartment Association"
        verbose_name_plural = "Kit-Compartment Association"
        ordering = ['ordering']


class KitItemAssociation(models.Model):
    kit = models.ForeignKey(Kit,
                            on_delete=models.CASCADE)
    item = models.ForeignKey(Item,
                             on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    def __str__(self):
        return '{}: {}'.format(self.kit.name, self.item.name)

    class Meta:
        verbose_name = "Kit-Item Association"
        verbose_name_plural = "Kit-Item Association"
        ordering = ['ordering']


class CompartmentItemAssociation(models.Model):
    compartment = models.ForeignKey(Compartment,
                                    on_delete=models.CASCADE)
    item = models.ForeignKey(Item,
                             on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    def __str__(self):
        item_details = self.item.name

        if self.item.size:
            item_details = '{}, {}'.format(item_details, self.item.size)

        item_details = '{} (x{})' .format(item_details, self.quantity)

        return '{}: {}'.format(self.compartment.name, item_details)

    class Meta:
        verbose_name = "Compartment-Item Association"
        verbose_name_plural = "Compartment-Items Association"
        ordering = ['ordering']


class CompartmentKitAssociation(models.Model):
    compartment = models.ForeignKey(Compartment,
                                    on_delete=models.CASCADE)
    kit = models.ForeignKey(Kit,
                            on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    def __str__(self):
        item_details = self.kit.name

        return '{}: {}'.format(self.compartment.name, item_details)

    class Meta:
        verbose_name = "Compartment-Kit Association"
        verbose_name_plural = "Compartment-Kits Association"
        ordering = ['ordering']


class BagCompartmentAssociation(models.Model):
    bag = models.ForeignKey(Bag,
                            on_delete=models.CASCADE)
    compartment = models.ForeignKey(Compartment,
                                    on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(blank=True,
                                                null=True)

    def __str__(self):
        return '{}: {}'.format(self.bag.name, self.compartment.name)

    class Meta:
        verbose_name = "Bag-Compartment Association"
        verbose_name_plural = "Bag-Compartment Associations"
        ordering = ['ordering']


# TODO add Device class for Monitor X Series, Monitor E Series
