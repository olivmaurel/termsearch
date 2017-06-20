import csv
import os
import logging
import sys
import django

LOCAL_DIR =  os.path.dirname(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.dirname('../')))
sys.path.append(os.path.abspath(os.path.dirname('.')))
django.setup()

from aggregator.models import Language


# Get an instance of a logger
logger = logging.getLogger(__name__)



def import_languages_from_csv(path):
    logger.info("Importing languages...")

    with open(path) as f:
        reader = csv.reader(f)
        next(reader) # skip headers
        for row in reader:
            _, created = Language.objects.get_or_create(
                name = row[0],
                code2d = row[1],
                code3d = row[2],)

            logger.info("{} found. Created {}".format(row[0], created))
    logger.info("Imported {} successfully".format(path))


def export_csv_to_json(csvpath, jsonpath):

    logger.info("Converting {} to JSON...".format(csvpath))
    with open(csvpath, 'r') as f:
        csvfile = csv.reader(f)
        jsonfile = open(jsonpath, 'w')
        # fieldnames = csvfile # todo finish this

    pass

def order_csv_alphabetically(file):

    pass


if __name__ == "__main__":

    language_csv_path =  os.path.join(LOCAL_DIR, 'static/aggregator/csv/language.csv')
    language_json_path = os.path.join(LOCAL_DIR, 'aggregator/fixtures/language.json')
    import_languages_from_csv(language_csv_path)
    export_csv_to_json(language_csv_path, language_json_path)
