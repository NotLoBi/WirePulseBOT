import yaml
import random

from settings.canvas import canvas_proxy_setup, canvas_proxy_error

'''
Open YAML proxies file and parse the proxies 
that can be used for future scraping.
'''
def select_proxy() -> str:
    with open("settings/proxies.yaml", "r") as f:
        data = yaml.safe_load(f)
        proxies = [proxy["url"] for proxy in data["proxies"]]

    random_proxy = random.choice(proxies)
    
    if random_proxy:
        canvas_proxy_setup(random_proxy)
    else:
        canvas_proxy_error()
        return None

    return {"http":random_proxy, "https":random_proxy}
