import pprint
import importlib

from collections import OrderedDict
from app.utils.utils import get_driver


class SocialMediaScrapperService:
    def __init__(self, social_media_urls, credentials):
        self.credentials = credentials
        self.social_media_urls = social_media_urls

    def get_scrapped_data(self):
        scrapped_data = OrderedDict()

        for platform, channel_urls_data in self.social_media_urls.items():

            print("=========================================================")
            print(f"Starting to scrap: {platform.upper()}")
            print("=========================================================")

            platform = platform.split("-")[0].lower()

            login_required = channel_urls_data.get("meta", {}).get("login_required", False)
            channel_urls = channel_urls_data.get("urls", {})

            if login_required:
                creds = self.credentials.get(platform, {})

            try:
                module = importlib.import_module(f'app.social_medias.{platform}')
                get_data = getattr(module, 'get_data')
            except Exception as ex:
                print(ex)
                continue

            try:
                platform_data = get_data(channel_urls, creds)
            except Exception as ex:
                print(ex)
                continue

            scrapped_data[platform] = OrderedDict({
                **scrapped_data.get(platform, {}),
                **platform_data
            })

            print(f"Finished to scrap: {platform.upper()}")
            print("=========================================================")
            print("\n")

        return scrapped_data
