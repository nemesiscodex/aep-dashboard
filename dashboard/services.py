from datetime import datetime

from django.db.models.aggregates import Max
from core.models import Activation, Detector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware
from django.db.models import Sum
from django.db.models.functions import TruncDate

def today():
    return make_aware(datetime.now()).replace(hour=0, minute=0, second=0, microsecond=0)

class DashboardService:

    @staticmethod
    def get_detected_today():
        now = make_aware(datetime.now())
        start_of_day = today()
        result = Activation.objects \
            .filter(timestamp__gte=start_of_day, timestamp__lt=now) \
            .aggregate(Sum('count'))
        return result.get('count__sum', 0)

    @staticmethod
    def get_detected_this_week():
        now = make_aware(datetime.now())
        start_of_day = today()
        sunday = (start_of_day.weekday() + 1) % 7
        start_of_week = start_of_day - timedelta(days=sunday)
        result = Activation.objects \
            .filter(timestamp__gte=start_of_week, timestamp__lt=now) \
            .aggregate(Sum('count'))
        return result.get('count__sum', 0)    
            

    @staticmethod
    def get_detected_this_month():
        now = make_aware(datetime.now())
        start_of_day = today()
        start_of_month = start_of_day - timedelta(days=start_of_day.day - 1)
        result = Activation.objects \
            .filter(timestamp__gte=start_of_month, timestamp__lt=now) \
            .aggregate(Sum('count'))
        return result.get('count__sum', 0)

    @staticmethod
    def get_detected_per_day():
        start_of_day = today()
        a_year_ago = start_of_day - relativedelta(year=1)
        result = Activation.objects \
            .filter(timestamp__gt=a_year_ago) \
            .annotate(timestamp_date=TruncDate('timestamp')) \
            .values('timestamp_date') \
            .annotate(**{'total': Sum('count')}) \
            .order_by('timestamp_date')
        return list(
            map(
                lambda x: [x['timestamp_date'].strftime("%Y-%m-%d"), x['total']], 
                result
            )
        )

    @staticmethod
    def get_detected_last_30_days_grouped():
        now = make_aware(datetime.now())
        start_of_day = today()
        days_ago = start_of_day - timedelta(days=30)
        activations = Activation.objects \
            .filter(timestamp__gte=days_ago, timestamp__lt=now) \
            .values('detector_identifier') \
            .annotate(**{'total': Sum('count')})
        detectors = {detector.identifier: detector for detector in Detector.objects.all()}
        activations = list(filter(lambda x: x['detector_identifier'] in detectors, activations))
        return list(map(lambda x: [
            x['detector_identifier'], 
            x['total'], 
            detectors[x['detector_identifier']].longitude, 
            detectors[x['detector_identifier']].latitude
        ], activations))
