import sys
import time

from colorama import Fore, Back, Style, init

init()

CNOTHING = Style.RESET_ALL
CRED = Fore.RED
CGREEN = Fore.GREEN
CYELLOW = Fore.YELLOW
CCYAN = Fore.CYAN
CVIOLET = Fore.MAGENTA

'''
Progress bar function
'''
def sleeping_progress_bar(reason, sleeping):
    print(f"\n{CCYAN}[i]---- : {reason} : {sleeping} seconds.{CNOTHING}\n")
    
    bar_length = 50
    step_duration = sleeping / bar_length
    
    for i in range(bar_length):
        progress = (i + 1) / bar_length * 100
        bar = f"{CGREEN}#{CNOTHING}" * (i + 1) + "-" * (bar_length - i-1)
        
        sys.stdout.write(f"\r[{bar}] {CGREEN}{progress:.2f}%{CNOTHING}")
        sys.stdout.flush()
        
        time.sleep(step_duration)   # Sleep for captcha resolution
    
    print("\n")

    
'''
Main messages
'''
def canvas_main_error(e):
    print(f"{CRED}[x]---- : Error WirePulseBOT : {e}{CNOTHING}\n")


'''
Scrapers messages
'''
def canvas_scraping_search_engine(se, dorks):
    print(f"{CCYAN}\n[i]---- : Scrapping {se}:{CNOTHING} {dorks}")

def canvas_ratelimit_search_engine(se):
    print(f"{CYELLOW}[!]---- : Reached rate limit for {se}.{CNOTHING}\n")

def canvas_scraping_results(i, item):
    print(f"{CGREEN}[{i}]---- :{CNOTHING} {item}")

def canvas_scraping_no_result():
    print(f"{CYELLOW}[!]---- : No results found.{CNOTHING}")

def canvas_scraping_error(e):
    print(f"{CRED}[x]---- : Error with scrapers : {e}{CNOTHING}\n")

def canvas_dumped_results():
    print(f"\n{CGREEN}[o]---- : Results dumped in results/scraping_results.json{CNOTHING}")


'''
Parser messages
'''
def canvas_invalid_method():
    print(f"{CRED}[x]---- : Invalid command or method.{CNOTHING}")

def canvas_parser_error(e):
    print(f"{CRED}[x]---- : Error with parser : {e}{CNOTHING}")

def canvas_parser_no_file():
    print(f"{CRED}[x]---- : Error with parser : sources.yaml file not found.{CNOTHING}")

def canvas_parser_yaml_error(e):
    print(f"{CRED}[x]---- : Error with parser : error parsing sources.yaml file : {e}{CNOTHING}")


'''
Proxy setup message
'''
def canvas_proxy_setup(random_proxy):
    print(f"{CCYAN}[i]---- : Using proxy:{CNOTHING} {random_proxy}\n")

def canvas_proxy_error():
    print(f"{CRED}[x]---- : Cannot use proxy, proxy set to None.{CNOTHING}\n")

def canvas_no_proxy():
    print(f"{CYELLOW}[!]---- : No proxy used. Consider using a proxy to avoid rate-limit.{CNOTHING}\n")


'''
WirePulseBOT complete manual
'''
def canvas_usage_manual():
    print(f"""
{CCYAN}Basic Command:{CNOTHING}
```
python wirepulsebot.py -st <search-term> -ts <time-stamp> -mt <media-type> [-p]
```

{CCYAN}Arguments:{CNOTHING}

    {CYELLOW}-st, --search-term <SEARCH_TERM> (Required):{CNOTHING}
    The term you want to search.

    {CYELLOW}-ts, --time-stamp <d,w,m,y> (Required):{CNOTHING}
    Specifies the time range for the search. You can choose from the following:
        - d: Results less than a day old
        - w: Results less than a week old
        - m: Results less than a month old
        - y: Results less than a year old
        - a: All results

    {CYELLOW}-mt, --media-type <SOURCE_TYPE_SLUG> (Required):{CNOTHING}
    Specifies the type of news media to query. The `media-type` corresponds to the `type_slug` tag in your sources file `sources/sources.yaml`

    {CYELLOW}-p, --proxy (Optional):{CNOTHING}
    Enables the use of a random proxy from a list defined in the file settings/proxies.yaml.
    Simply include the flag to activate proxy support.

    {CYELLOW}-c, --captcha (Optional):{CNOTHING} 
    Opens a visible Chromium browser for manual captcha solving when required by search engines. If not used, the browser runs in headless mode.

    {CRED}Using `--captcha` is highly recommended: Google and Brave often require captcha solving.{CNOTHING}

{CCYAN}To search for "inflation" in "economy" news sources for the past week using a proxy and captcha solving:{CNOTHING}
```
python wirepulsebot.py -st "inflation" -ts "w" -mt "economy" -p -c
```

{CCYAN}Notes:{CNOTHING}

    - For help or to view the manual, use:
    ```
    python wirepulsebot.py -h
    ```

    ```
    python wirepulsebot.py --documentation
    ```

    - The script ensures that only valid time-stamps and media types are accepted.
    """)



'''
Banner setup
'''
def banner_1():
    print(CVIOLET)
    print(
    """
▄▄▌ ▐ ▄▌▪  ▄▄▄  ▄▄▄ . ▄▄▄·▄• ▄▌▄▄▌  .▄▄ · ▄▄▄ .▄▄▄▄·       ▄▄▄▄▄▄
██· █▌▐███ ▀▄ █·▀▄.▀·▐█ ▄██▪██▌██•  ▐█ ▀. ▀▄.▀·▐█ ▀█▪ ▄█▀▄ ▀•██ ▀
██▪▐█▐▐▌▐█·▐▀▀▄ ▐▀▀▪▄ ██▀·█▌▐█▌██ ▪ ▄▀▀▀█▄▐▀▀▪▄▐█▀▀█▄▐█▌.▐▌  ▐█.▪
▐█▌██▐█▌▐█▌▐█•█▌▐█▄▄▌▐█▪·•▐█▄█▌▐█▌ ▄▐█▄▪▐█▐█▄▄▌██▄▪▐█▐█▌.▐▌  ▐█▌·
 ▀▀▀▀ ▀▪▀▀▀.▀  ▀ ▀▀▀ .▀    ▀▀▀ .▀▀▀  ▀▀▀▀  ▀▀▀ ·▀▀▀▀  ▀█▄▀▪  ▀▀▀ 

            /////////NotLoBi
    """, CNOTHING)

def banner_2():
    print(CVIOLET)
    print("""
                       ▄▄                                         ▄▄                                                
▀████▀     █     ▀███▀ ██                 ▀███▀▀▀██▄            ▀███                ▀███▀▀▀██▄ ▄▄█▀▀██▄ ███▀▀██▀▀███
  ▀██     ▄██     ▄█                        ██   ▀██▄             ██                  ██    ████▀    ▀██▄▀   ██   ▀█
   ██▄   ▄███▄   ▄█  ▀███ ▀███▄███  ▄▄█▀██  ██   ▄██▀███  ▀███    ██  ▄██▀███ ▄▄█▀██  ██    ███▀      ▀██    ██     
    ██▄  █▀ ██▄  █▀    ██   ██▀ ▀▀ ▄█▀   ██ ███████   ██    ██    ██  ██   ▀▀▄█▀   ██ ██▀▀▀█▄▄█        ██    ██     
    ▀██ █▀  ▀██ █▀     ██   ██     ██▀▀▀▀▀▀ ██        ██    ██    ██  ▀█████▄██▀▀▀▀▀▀ ██    ▀██▄      ▄██    ██     
     ▄██▄    ▄██▄      ██   ██     ██▄    ▄ ██        ██    ██    ██  █▄   ████▄    ▄ ██    ▄███▄    ▄██▀    ██     
      ██      ██     ▄████▄████▄    ▀█████▀████▄      ▀████▀███▄▄████▄██████▀ ▀█████▀████████  ▀▀████▀▀    ▄████▄   

            /////////NotLoBi
    """, CNOTHING)

def banner_3():
    print(CVIOLET)
    print(
    """
                    ▄▄                                         ▄▄                                                
▀████▀     █     ▀███▀ ██                 ▀███▀▀▀██▄            ▀███                ▀███▀▀▀██▄ ▄▄█▀▀██▄ ███▀▀██▀▀███
  ▀██     ▄██     ▄█                        ██   ▀██▄             ██                  ██    ████▀    ▀██▄▀   ██   ▀█
   ██▄   ▄███▄   ▄█  ▀███ ▀███▄███  ▄▄█▀██  ██   ▄██▀███  ▀███    ██  ▄██▀███ ▄▄█▀██  ██    ███▀      ▀██    ██     
    ██▄  █▀ ██▄  █▀    ██   ██▀ ▀▀ ▄█▀   ██ ███████   ██    ██    ██  ██   ▀▀▄█▀   ██ ██▀▀▀█▄▄█        ██    ██     
    ▀██ █▀  ▀██ █▀     ██   ██     ██▀▀▀▀▀▀ ██        ██    ██    ██  ▀█████▄██▀▀▀▀▀▀ ██    ▀██▄      ▄██    ██     
     ▄██▄    ▄██▄      ██   ██     ██▄    ▄ ██        ██    ██    ██  █▄   ████▄    ▄ ██    ▄███▄    ▄██▀    ██     
      ██      ██     ▄████▄████▄    ▀█████▀████▄      ▀████▀███▄▄████▄██████▀ ▀█████▀████████  ▀▀████▀▀    ▄████▄   

            /////////NotLoBi
    """, CNOTHING)

def banner_4():
    print(CVIOLET)
    print(
    """
 █     █░  ██▓ ██▀███   ▓█████ ██▓███   █    ██   ██▓     ██████  ▓█████  ▄▄▄▄    ▒█████  ▄▄▄█████▓
▓█░ █ ░█░▒▓██▒▓██ ▒ ██▒ ▓█   ▀▓██░  ██  ██  ▓██▒ ▓██▒   ▒██    ▒  ▓█   ▀ ▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
▒█░ █ ░█ ▒▒██▒▓██ ░▄█ ▒ ▒███  ▓██░ ██▓▒▓██  ▒██░ ▒██░   ░ ▓██▄    ▒███   ▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
░█░ █ ░█ ░░██░▒██▀▀█▄   ▒▓█  ▄▒██▄█▓▒ ▒▓▓█  ░██░ ▒██░     ▒   ██▒ ▒▓█  ▄ ▒██░█▀  ▒██   ██░░ ▓██▓ ░ 
░░██▒██▓ ░░██░░██▓ ▒██▒▒░▒████▒██▒ ░  ░▒▒█████▓ ▒░██████▒██████▒▒▒░▒████▒░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ 
░ ▓░▒ ▒   ░▓  ░ ▒▓ ░▒▓░░░░ ▒░ ▒▓▒░ ░  ░░▒▓▒ ▒ ▒ ░░ ▒░▓  ▒ ▒▓▒ ▒ ░░░░ ▒░ ░░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   
  ▒ ░ ░  ░ ▒ ░  ░▒ ░ ▒ ░ ░ ░  ░▒ ░     ░░▒░ ░ ░ ░░ ░ ▒  ░ ░▒  ░ ░░ ░ ░  ░▒░▒   ░   ░ ▒ ▒░     ░    
  ░   ░  ░ ▒ ░  ░░   ░     ░  ░░        ░░░ ░ ░    ░ ░  ░  ░  ░      ░    ░    ░ ░ ░ ░ ▒    ░ ░    
    ░      ░     ░     ░   ░              ░     ░    ░        ░  ░   ░  ░ ░          ░ ░           

            /////////NotLoBi
    """, CNOTHING)

