import csv

from aggregator.models import *

# Get an instance of a logger
logger = logging.getLogger(__name__)



def languages_from_csv(path):
    logger.info("Importing languages...")
    with open(path) as f:
        reader = csv.reader(f)
        next(reader) # skip headers
        for row in reader:
            _, created = Language.objects.get_or_create(
                name = row[0],
                code3d = row[1],
                code2d = row[2],
            )
    logger.info("Imported {} successfully".format(path))

def import_all():

    logger.info("Importing all csv file into Django db")
    language_csv_path = 'static/csv/languages.csv'
    languages_from_csv(language_csv_path)


if __name__ == "__main__":

    import_all()