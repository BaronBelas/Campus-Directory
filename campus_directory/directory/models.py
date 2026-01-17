from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    landmark = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='building_photos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors')
    floor_number = models.IntegerField()
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='floor_photos/', blank=True, null=True)  # FLOOR PLAN

    class Meta:
        unique_together = ('building', 'floor_number')

    def __str__(self):
        return f"{self.building.name} - Floor {self.floor_number}"


class Room(models.Model):
    ROOM_TYPES = [
        ('Office', 'Office'),
        ('Laboratory', 'Laboratory'),
        ('Department', 'Department'),
        ('Faculty', 'Faculty'),
        ('Specialized Room', 'Specialized Room'),
    ]

    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=50)
    name = models.CharField(max_length=200, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    description = models.TextField(blank=True)  # DIRECTIONS GO HERE
    photo = models.ImageField(upload_to='room_photos/', blank=True, null=True)

    class Meta:
        unique_together = ('floor', 'room_number')

    def __str__(self):
        return f"{self.room_number} - {self.name}"


class Personnel(models.Model):
    assigned_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='personnel')
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='personnel_photos/', blank=True, null=True)

    def __str__(self):
        return self.name


class SearchLog(models.Model):
    entity_type = models.CharField(max_length=50)
    entity_id = models.PositiveIntegerField()
    search_time = models.DateTimeField(auto_now_add=True)

