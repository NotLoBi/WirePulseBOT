'''
Scrapers Configuration File:

Edit this file if you know what 
you are doing.

- BASE_URLS: URLs of the search engines used 
             for scraping and retrieving results.

             > Modifications are not recommended.

- TIMEOUT: Maximum time available for HTML response parsing (in ms).

- CAPTCHA_SOLVE_TIME: Time range given to the user to solve
                      captchas (in seconds).

- RATE_LIMIT_DELAY: Time to spend on the search page before 
                    moving on to the next one.

- MAX_RESULTS: Maximum number of results to show when scraping.
               Heavy impact on rate-limiting. Default is 15.


'''

BASE_URLS = {
    "DuckDuckGo": "https://duckduckgo.com/html/",
    "Google": "https://www.google.com/search",
    "Brave": "https://search.brave.com/search"
}

TIMEOUT = 6000

CAPTCHA_SOLVE_TIME = (50, 90)

RATE_LIMIT_DELAY = (8, 15)

MAX_RESULTS = 15