import re
import json
import time
import random
import urllib.parse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

'''
Script settings
'''
from modules.parser import format_dorks
from settings.proxy_setup import select_proxy
from settings.scrapers_config import (      # Scapers config file : edit the setting if you know what you are doing
    BASE_URLS, 
    TIMEOUT,
    CAPTCHA_SOLVE_TIME,
    MAX_RESULTS,
    RATE_LIMIT_DELAY
    )
from settings.canvas import (
    sleeping_progress_bar,
    canvas_scraping_search_engine,
    canvas_ratelimit_search_engine,
    canvas_scraping_results,
    canvas_scraping_no_result,
    canvas_scraping_error,
    canvas_dumped_results,
    )

class Scrapers():
    '''
    Scraper settings
    '''
    def init_scraper(self, search_term: str, search_timestamp: str, media_type: str, captcha: bool, proxy):
        search_dorks = format_dorks(search_term, search_timestamp, media_type)

        # Load scrapers : Google - DuckDuckGo - Brave
        goo_results = list(set(self.scraper_goo(search_dorks, captcha, proxy))) # Erase doubles using sets
        ddg_results = list(set(self.scraper_ddg(search_dorks, captcha, proxy)))
        brv_results = list(set(self.scraper_brv(search_dorks, captcha, proxy)))

        scraping_results = {
            search_term: {
                "DuckDuckGo": ddg_results,
                "Google": goo_results,
                "Brave": brv_results
                }
            }
        
        # Save results to JSON
        try:
            with open("results/scraping_results.json", "w", encoding="utf-8") as results_file:
                json.dump(scraping_results, results_file, indent=4, ensure_ascii=False)

            canvas_dumped_results()
            
        except Exception as e:
            canvas_scraping_error(e)
            pass


    def scraper_goo(self, search_dorks: str, captcha: bool, proxy) -> list:
        '''
        Scraper for Google.

        Captcha verification is almost
        always required.
        '''
        scraping_results_list = []

        headless = not captcha  # Use headless mode if captcha is False
        
        # Let the user complete the captcha if captcha mode enabled
        if captcha:
            WAITING = random.uniform(*CAPTCHA_SOLVE_TIME)
            WAITING_MESSAGE = "Captcha solving time available"
        else:
            WAITING = random.uniform(*RATE_LIMIT_DELAY)
            WAITING_MESSAGE = "Sleeping to avoid rate-limit"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(proxy=proxy)
            page = context.new_page()

            for search_dorks_value, search_dorks_timestamp in search_dorks.items():
                # Format the dork query
                if search_dorks_timestamp == "a":
                    time_stamp = ""
                else:
                    time_stamp = f"&tbs=qdr:{search_dorks_timestamp}"

                scrape_url = f"{BASE_URLS['Google']}?q={search_dorks_value}&num={MAX_RESULTS}{time_stamp}"
                canvas_scraping_search_engine(se="Google", dorks=search_dorks_value)

                try:
                    page.goto(scrape_url)
                    sleeping_progress_bar(WAITING_MESSAGE, int(WAITING))

                    html_content = page.content()

                    if "This network is blocked due to unaddressed abuse complaints about malicious behavior" in html_content or "Our systems have detected unusual traffic from your computer network." in html_content:
                        canvas_ratelimit_search_engine(se="Google")
                        return scraping_results_list
                        
                    WAITING = random.uniform(*RATE_LIMIT_DELAY)
                    WAITING_MESSAGE = "Sleeping to avoid rate-limit"

                    links = page.locator('a[jsname="UWckNb"]')  # Google results tags
                    results = links.evaluate_all(
                        'elements => elements.map(e => e.href)'
                    )

                    soup = BeautifulSoup(html_content, "html.parser")
                    link_tags = soup.select('a[jsname="UWckNb"]')

                    # Extract results
                    for tag in link_tags:
                        href = tag.get('href')
                        if href:
                            parsed_url = urllib.parse.urlparse(href)
                            clean_url = urllib.parse.parse_qs(parsed_url.query).get('q', [None])[0]
                            if clean_url is None:
                                clean_url = href

                            scraping_results_list.append(clean_url.strip())

                    # Display results
                    if scraping_results_list:
                        for idx, link in enumerate(scraping_results_list, 1):
                            canvas_scraping_results(idx, link)
                    else:
                        canvas_scraping_no_result()

                except Exception as e:
                    canvas_scraping_error(e)
                    continue

            browser.close()

        return scraping_results_list

    
    def scraper_ddg(self, search_dorks: str, captcha: bool, proxy) -> list:
        '''
        Scraper for DuckDuckGo.

        Captcha verification is almost
        never required.
        '''
        scraping_results_list = []

        headless = not captcha
        
        if captcha:
            WAITING = random.uniform(*CAPTCHA_SOLVE_TIME)
            WAITING_MESSAGE = "Captcha solving time available"
        else:
            WAITING = random.uniform(10, 20)
            WAITING_MESSAGE = "Sleeping to avoid rate-limit"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(proxy=proxy)
            page = context.new_page()

            for search_dorks_value, search_dorks_timestamp in search_dorks.items():
                search_format = urllib.parse.quote(str(search_dorks_value).replace("%0A", ""))
                
                if search_dorks_timestamp == "a":
                    time_stamp = ""
                else:
                    time_stamp = f"&df={search_dorks_timestamp}"

                scrape_url = f"{BASE_URLS['DuckDuckGo']}?q={search_format}&kl=wt-wt&kp=-2&kf=-1{time_stamp}" # Do not use the TOR URL => SOCKS errors
                canvas_scraping_search_engine(se="DuckDuckGo", dorks=search_dorks_value)

                try:
                    page.goto(scrape_url)
                    sleeping_progress_bar(WAITING_MESSAGE, int(WAITING))

                    html_content = page.content()

                    if "Unfortunately, bots use DuckDuckGo too" in html_content:
                        canvas_ratelimit_search_engine(se="DuckDuckGo")
                        return scraping_results_list
                        
                    WAITING = random.uniform(*RATE_LIMIT_DELAY)
                    WAITING_MESSAGE = "Sleeping to avoid rate-limit"

                    url_regex = r'<a class="result__url" href="?//duckduckgo\.com?/l/\?uddg=[^"]+">([^<]+)<\/a>'    # Grepping results with regex
                    results = re.findall(url_regex, html_content)

                    for urls in results:
                        scraping_results_list.append(urls.strip())

                    if scraping_results_list:
                        for i, item in enumerate(scraping_results_list, start=1):  
                            canvas_scraping_results(i, item)
                    else:
                        canvas_scraping_no_result()

                except Exception as e:
                    canvas_scraping_error(e)
                    continue

            browser.close()

        return scraping_results_list

    
    def scraper_brv(self, search_dorks: str, captcha: bool, proxy) -> list:
        '''
        Scraper for Brave.

        Captcha verification is almost
        always required.
        '''
        scraping_results_list = []

        headless = not captcha 
        
        if captcha:
            WAITING = random.uniform(*CAPTCHA_SOLVE_TIME)
            WAITING_MESSAGE = "Captcha solving time available"
        else:
            WAITING = random.uniform(*RATE_LIMIT_DELAY)
            WAITING_MESSAGE = "Sleeping to avoid rate-limit"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(proxy=proxy)
            page = context.new_page()

            for search_dorks_value, search_dorks_timestamp in search_dorks.items():
                search_format = urllib.parse.quote(f"{str(search_dorks_value).replace('%0A','')}")  

                if search_dorks_timestamp == "a":
                    time_stamp = ""
                else:
                    time_stamp = f"&tf=p{search_dorks_timestamp}"

                scrape_url = f"{BASE_URLS['Brave']}?q={search_format}{time_stamp}"
                canvas_scraping_search_engine(se="Brave", dorks=search_dorks_value)

                try:
                    page.goto(scrape_url)
                    sleeping_progress_bar(WAITING_MESSAGE, int(WAITING))

                    html_content = page.content()
                    with open("test.html", "w") as file:
                        file.write(html_content)

                    if "Your request has been flagged as being suspicious" in html_content:
                        canvas_ratelimit_search_engine(se="Brave")
                        return scraping_results_list
                            
                    WAITING = random.uniform(*RATE_LIMIT_DELAY)
                    WAITING_MESSAGE = "Sleeping to avoid rate-limit"

                    soup = BeautifulSoup(html_content, 'html.parser')
                    divs = soup.find_all('div', class_="svelte-n9nog2")     # Brave results class

                    for div in divs:
                        link = div.find('a', href=True) 
                        if link and not link['href'].startswith("/search"):
                            scraping_results_list.append(link['href']) 

                    if scraping_results_list:
                        for i, item in enumerate(scraping_results_list, start=1):  
                            canvas_scraping_results(i, item)
                    else:
                        canvas_scraping_no_result()

                except Exception as e:
                    canvas_scraping_error(e)
                    continue

            browser.close()

        return scraping_results_list
