import os
import django
django.setup()
from core.models import memberdetails
from django.db.models import Q
from datetime import datetime, timedelta

VERIFICATION_CODE_SESSION = int(os.environ['VERIFICATION_CODE_SESSION'])

two_hour_hours_date_time = datetime.now() - timedelta(hours = VERIFICATION_CODE_SESSION)
two_hour_date_time = two_hour_hours_date_time.strftime('%Y-%m-%d %H:%M:%S')

current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

get_updated_time = memberdetails.objects.filter(~Q(updated_at__range = (two_hour_date_time, current_date_time)))
for i in get_updated_time:
    i.verificationcode = ''
    i.save()