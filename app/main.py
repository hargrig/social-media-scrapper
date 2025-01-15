import json
from datetime import datetime

from utils.utils import restruct_scrapped_data
from services.google_spreadsheet import GoogleSpreadsheetService
from services.social_media_scrapper import SocialMediaScrapperService


def scrape_social_media(internal_channels, credentials, data_dir):
    now = datetime.now()
    scrape_date = now.strftime('%Y-%m-%d')

    scrapper = SocialMediaScrapperService(internal_channels, credentials)
    scrapped_data = scrapper.get_scrapped_data()

    spreadsheet_data = restruct_scrapped_data(scrapped_data)

    google_spreadsheet = GoogleSpreadsheetService(spreadsheet_data)
    google_spreadsheet.fill_spreadsheet()

    with open(f'{data_dir}/scrapped-data-{scrape_date}.json', 'w') as scrapped_fp:
        json.dump(scrapped_data, scrapped_fp, indent=4)

    with open(f'{data_dir}/spreadsheet-data-{scrape_date}.json', 'w') as spreadsheet_fp:
        json.dump(spreadsheet_data, spreadsheet_fp, indent=4)


if __name__ == "__main__":
    with open('config/internal-channels.json', 'r') as internal_channels_fp:
        internal_channels = json.load(internal_channels_fp)

    if not internal_channels:
        print("Please configure Internal Channels' URLS")
        exit()

    with open('config/platform-creds.json', 'r') as creds_fp:
        credentials = json.load(creds_fp)

    scrape_social_media(internal_channels, credentials, 'data/internal')