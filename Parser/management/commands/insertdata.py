import csv
import os
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from Parser.models import NEM13
from datetime import datetime

class Command(BaseCommand):

    help = "parse csv"

    def add_arguments(self, parser):
        parser.add_argument( 'filenames' ,
                              nargs='+',
                              type=str ,
                              help="Inserts data from CSV file" )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = NEM13

    def insert_data_to_db(self ,data) :
        try :
            self.model_name.objects.create (
                nmi=data [ "nmi" ] ,
                reading_time=data [ "reading_time" ] ,
                serial_number=data [ "serial_number" ],
                reading_value = data ["reading_value"],
                filename = data [ "filename" ]
            )
        except Exception as e :
            raise CommandError ( "Error in inserting " )

    def get_current_app_path(self):
        return apps.get_app_config('Parser').path

    def get_csv_file(self, filename):
        app_path = self.get_current_app_path()
        file_path = os.path.join(app_path, "management",
                                 "commands", filename)
        return file_path

    def handle(self, *args, **options):

        for filename in options['filenames']:
            self.stdout.write(self.style.SUCCESS('Reading:{}'.format(filename)))
            file_path = self.get_csv_file(filename)
            try:
                self.stdout.write ( file_path )
                with open(file_path) as csv_file:
                    csv_reader = csv.reader(csv_file)
                    data = list ( csv_reader )
                    count = 0
                    row_count = len ( data )
                    print(csv_reader)
                    for row in data:
                        print ( row )
                        if row != "" and count != 0 and count != row_count-1:

                            words = [word.strip() for word in row]
                            nmi = words[1]
                            reading_time = words[14]
                            serial_number = words[6]
                            reading_value = words[13]
                            dt = datetime.strptime ( reading_time , '%Y%m%d%H%M%S')
                            reading_time= dt.strftime ( '%Y-%m-%d %H:%M:%S' )
                            data = {}
                            data["nmi"] = nmi
                            data["reading_time"] = reading_time
                            data["serial_number"] = serial_number
                            data [ "reading_value" ] = reading_value
                            data [ "filename" ] = filename
                            print(filename)
                            self.insert_data_to_db(data)
                            self.stdout.write(
                                self.style.SUCCESS('{}_{}'.format(
                                        nmi, reading_time
                                        )
                                )
                            )
                        count = count + 1

            except FileNotFoundError:
                raise CommandError("File {} does not exist".format(
                    file_path))

