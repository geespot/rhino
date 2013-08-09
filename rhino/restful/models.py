from django.db import models

class CallingRecord(models.Model):
    time = models.DateTimeField(auto_now=True)
    session_id = models.CharField(max_length=32)
    user_id = models.IntegerField()
    client_ip = models.CharField(max_length=20)
    api_name = models.CharField(max_length=40)
    input_params = models.CharField(max_length=200)
    process_time = models.FloatField()
    status_code = models.IntegerField()
    response_length = models.IntegerField()
