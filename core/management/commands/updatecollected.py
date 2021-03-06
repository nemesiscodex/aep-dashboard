from django.core.management.base import BaseCommand, CommandError
from django.db.models.aggregates import Max
from core.models import CollectorActivation, Activation
from django.utils.timezone import make_aware
from datetime import timedelta
import re

class Command(BaseCommand):
    help = 'Update activations from collectors table'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from_id', 
            type=int, 
            help='Start from specific id. Otherwise will start from latest.'
        )

    def handle(self, *args, **options):
        if options['from_id'] is not None:
            from_id = options['from_id']
        else:    
            from_id = Activation.objects.aggregate(Max('collector_id')).get('collector_id__max')

        if from_id is None:
            from_id = 0
        
        print("Starting from {0}".format(from_id))

        values = CollectorActivation.objects.filter(id__gt=from_id).order_by('id')

        processed = 0
        total = values.count()

        print("Records to process: {0}".format(total))

        for value in values:
            last_24_hours = make_aware(value.created_at) - timedelta(days=1)
            similar_frames = CollectorActivation.objects.filter(id__lt=value.id, created_at__gt=last_24_hours, frame=value.frame).count()
            parsed_frame = value.match_frame()
            if similar_frames > 0:
                print("Similar frames found for {0} with id {1}. Skipping...".format(value.frame, value.id))
            elif parsed_frame == 0:
                days, hours, minutes, seconds, \
                    detector_id, s1, s2, s3, s4, count = parsed_frame.groups()
                activation = Activation.objects.filter(collector_id=value.id).first()
                if not activation:
                    activation = Activation()
                activation.collector_id = value.id
                activation.timestamp = make_aware(value.created_at)
                activation.detector_identifier = detector_id
                activation.uptime_days = days
                activation.uptime_hours = hours
                activation.uptime_minutes = minutes
                activation.uptime_seconds = seconds
                activation.sensor_1 = s1
                activation.sensor_2 = s2
                activation.sensor_3 = s3
                activation.sensor_4 = s4
                activation.count = count
                try:
                    activation.save()
                    processed += 1
                except e:
                    print("Error processing frame with id {0}. Error: {1}".format(value.id, e))
            else: 
                print("Unable to parse frame {0} with id {1}".format(value.frame, value.id))
        if processed != total:
            print("Processed {0} rows out of {1}".format(processed, total))
        elif total > 0: 
            print("Processed {0} rows".format(total))
        