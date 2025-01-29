import json

from datetime import datetime
from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready

from app.utils.utils import restruct_scrapped_data
from app.services.google_spreadsheet import GoogleSpreadsheetService
from app.services.social_media_scrapper import SocialMediaScrapperService


celery_app = Celery('tasks', broker='redis://redis:6379/0')
EXPORT_DIR="app/data/internal"

@celery_app.task
def scrape_social_media():

    with open('app/config/internal-channels.json', 'r') as social_media_file:
        social_media_urls = json.load(social_media_file)

    if not social_media_urls:
        print("Please configure Social Media URLS")
        return

    with open('app/config/platform-creds.json', 'r') as cred_file:
        credentials = json.load(cred_file)

    now = datetime.now()
    scrape_date = now.strftime('%Y-%m-%d')

    scrapper = SocialMediaScrapperService(social_media_urls, credentials)
    scrapped_data = scrapper.get_scrapped_data()

    spreadsheet_data = restruct_scrapped_data(scrapped_data)

    # google_spreadsheet = GoogleSpreadsheetService(spreadsheet_data)
    # google_spreadsheet.fill_spreadsheet()

    with open(f'{EXPORT_DIR}/scrapped-data-{scrape_date}.json', 'w') as scrapped_file:
        json.dump(scrapped_data, scrapped_file, indent=4)

    with open(f'{EXPORT_DIR}/spreadsheet-data-{scrape_date}.json', 'w') as spreadsheet_file:
        json.dump(spreadsheet_data, spreadsheet_file, indent=4)


celery_app.conf.beat_schedule = {
    'run-every-day-at7': {
        'task': 'app.tasks.scrape_social_media', 
        'schedule': crontab(
            hour=3, 
            minute=0
        )
    },
}

# Open comment below only for testing (debugging) purposes, 
# it runs the scrapper once the container runs.

# @worker_ready.connect
# def at_start(sender, **kwargs):
#     with sender.app.connection() as conn:
#         sender.app.send_task('app.tasks.scrape_social_media')

