from django.db import models

class EquipmentUpload(models.Model):
    filename = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
    total_equipment = models.IntegerField()
    average_flowrate = models.FloatField()
    average_pressure = models.FloatField()
    average_temperature = models.FloatField()

    def __str__(self):
        return f"{self.filename} ({self.upload_time})"