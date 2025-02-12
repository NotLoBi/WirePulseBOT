import sys
import random
import argparse

from modules.scraper import Scrapers
from modules.parser import valid_media_types
from settings.proxy_setup import select_proxy
from settings.canvas import (
    banner_1, 
    banner_2, 
    banner_3, 
    banner_4,
    canvas_main_error,
    canvas_no_proxy,
    canvas_usage_manual
    )

def show_banner():
    banners = [banner_1, banner_2, banner_3, banner_4]
    random.choice(banners)()
    

VALID_MEDIA_TYPES = valid_media_types()
VALID_TIMESTAMPS = ["d", "w", "m", "y", "a"]


def main():
    '''
    Execute WirePulseBOT :

    Set a search terms (eg: "inflation"), 
    a time-stamp (eg: "w" that stands for "week")
    and a media type (eg: "economy").

    - Search term : whatever the you want to search.

    - Time-stamp : multiple time-stamp available :
        - Results less than a day old : "d"
        - Results less than a week old : "w" 
        - Results less than a month old : "m" 
        - Results less than a year old : "y"
        - All results : "a"
  
    - Media type : "type_slug" from "sources/sources.yaml".
    
    You can choose to use a proxy, which will be randomly
    selected from the proxy list 'settings/proxies.yaml'.
    '''
    show_banner()

    if "--documentation" in sys.argv:
        canvas_usage_manual()
        return

    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument("-st", "--search-term", action="store", type=str, required=True, help="The term you want to search. (eg: 'inflation', 'russia', ...)")
    parser.add_argument("-ts", "--time-stamp", action="store", type=str, required=True, choices=VALID_TIMESTAMPS, help=f"Selected time-stamp for the search. Choose from: {', '.join(VALID_TIMESTAMPS)}.")
    parser.add_argument("-mt", "--media-type", action="store", type=str, required=True, choices=VALID_MEDIA_TYPES, help=f"The type of media you want to use. Choose from: {', '.join(VALID_MEDIA_TYPES)}.")
    parser.add_argument("-p", "--proxy", action="store_true", required=False, help="Use a random proxy from 'settings/proxies.yaml'")
    parser.add_argument("-c", "--captcha", action="store_true", required=False, help="Enable visible Chromium to solve captchas manually.")
    parser.add_argument("--documentation", action="store_true", required=False, help="Show complete documentation.")

    args = parser.parse_args()

    try:
        if args.proxy:
            proxy = select_proxy()
        else:
            proxy = None
            canvas_no_proxy()
        
        captcha = bool(args.captcha)

        # Initiate scrapping
        scrape = Scrapers()
        scrape.init_scraper(
            search_term=args.search_term, 
            search_timestamp=args.time_stamp, 
            media_type=args.media_type, 
            captcha=args.captcha, 
            proxy=proxy
        )

    except Exception as e:
        canvas_main_error(e)
        exit(1)

if __name__ == "__main__":
    main()