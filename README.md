
<div align="center">
    <h1>WirePulseBOT</h1>
</div>

---

<br>

**WirePulseBOT is a Python-based scraping tool designed for automatically searching information from various news websites, performing Social Media Intelligence (SOCMINT), or conducting research that requires scraping search engines.**

> *It is highly customizable, making it ideal for researchers, journalists, OSINT experts, or anyone looking to gather data from the web.*

<br>

---

<br>

### KEY FEATURES

**Proxy Support:** *Users can enhance their anonymity by enabling proxy support. A random proxy is selected from a user-defined list, providing additional privacy and security during searches.*

**Automated Searches:** *Perform searches across multiple search engines and gather information.*
- *Google*
- *DuckDuckGo*
- *Brave*

**Categorized Information:** *Sources are grouped by categories for specific and precise searches.*

**Customizable Sources:** *Users have complete control over their sources and can add or remove sources and categories based on their preferences.*

<br>

---

<br>

### SOURCES  

> **WirePulseBOT by default includes a list of different sources.**

Sources (the news or specialized websites) are **organized by categories.** These categories correspond to the `type_slug` tag in the `sources.yaml` file:

**Default sources sample:**
```yaml
media:
  - type: "General News"
    type_slug: "general"
    sources:
      - name: "BBC News"
        url: "https://www.bbc.com"
        short_url: "www.bbc.com"
      - name: "Reuters"
        url: "https://www.reuters.com"
        short_url: "www.reuters.com"

  - type: "Geopolitics & Defense"
    type_slug: "geopolitics"
    sources:
      - name: "Janes"
        url: "https://www.janes.com"
        short_url: "www.janes.com"
      - name: "War on the Rocks"
        url: "https://warontherocks.com"
        short_url: "warontherocks.com"
```

These categories are then used in the command to **focus on a specific category** during the search using the argument `-mt, --media_type`.

**The user can check the available media types** by looking at the `type_slug` tags in the sources file, or simply by executing:

```python
python wirepulsebot.py
```

**You have full control over sources.** You can **add** or **remove** sources that you want to use by editing the YAML file `sources/sources.yaml`.

> **VERY IMPORTANT: If you want to add your sources, please make sure to add a "short_url", or the scraper may not work properly.**  

> **If you want to add your own categories, an advanced guide is available below.**

<br>

---

<br>

### INSTALLATION

**Requirements:**

- *Python3*
- *Pip3*

**Download:**

```bash
git clone https://github.com/NotLoBi/WirePulseBOT
```

<br>

---

<br>

### SETUP

> **It is recommended to use a Python virtual environment before using WirePulseBOT.**

**Create a virtual environment:**  
```bash
python3 -m venv .venv
```

**Install the libraries in the virtual environment:**

*On Linux:*
```bash
source .venv/bin/activate
```

*On Windows:*
```powershell
.\.venv\Scripts\Activate.ps1
```

Install the libraries:  
```bash
pip install -r requirements.txt
```

**Install Playwright:**

Inside your virtual environment:
```bash
playwright install-deps
```

<br>

---

<br>

### USAGE

**WirePulseBOT requires the user to provide a set of arguments to execute a search. Here's how to use it:**

**Basic Command:**  
```bash
python wirepulsebot.py -st <search-term> -ts <time-stamp> -mt <media-type> [-p] [-c]
```

**Arguments:**

- `-st, --search-term <{SEARCH_TERM}>` **(Required):** *The term you want to search.*

- `-ts, --time-stamp <{d,w,m,y}>` **(Required):** *Specifies the time range for the search. You can choose one of the following:*  
  - **d:** *Results less than a day old*
  - **w:** *Results less than a week old*
  - **m:** *Results less than a month old*
  - **y:** *Results less than a year old*
  - **a:** *All results*

- `-mt, --media-type <{SOURCE_TYPE_SLUG}>` **(Required):** *Specifies the type of news media to query. The `media-type` corresponds to the `type_slug` tag in your sources file `sources/sources.yaml`*

- `-p, --proxy` **(Optional):** *Enables the use of a random proxy from a list defined in the file `settings/proxies.yaml`. Simply include the flag to activate proxy support.*

- `-c, --captcha` **(Optional):** *Opens a visible Chromium browser for manual captcha solving when required by search engines. If not used, the browser runs in headless mode.*

> **Using `--captcha` is highly recommended: Google and Brave often require captcha solving.**

<br>

**Example:**  

To search for "inflation" from "economy" sources (default `sources.yaml`) for the past week using a proxy and captcha solving:  
```bash
python wirepulsebot.py -st "inflation" -ts "w" -mt "economy" -p -c
```

<br>

**Notes:**

For help or to view the manual, use:  
```bash
python wirepulsebot.py -h
```

```bash
python wirepulsebot.py --documentation
```

**The script ensures that only valid time-stamps and media types are accepted.**

<br>

**Tips:**

- Use **simple and short** search terms to get more results.
- Use **multiple proxies** to improve the chances of scraping success.

<br>

---

<br>

### RESULTS

> **Scraping results are saved in JSON format.**

WirePulseBOT stores the scraping results in the JSON file ```results/scraping_results.json```

**Example:**

- Command:
    ```Python
    python wirepulsebot.py -st "trump" -ts "d" -mt "economy" -c
    ```

- Results file:
    ```json
    {
        "trump": {
            "DuckDuckGo": [
                "www.reuters.com/markets/....",
                "www.reuters.com/markets/us/...",
            ],
            "Google": [
                "www.bloomberg.com/news/articles/...",
                "www.ft.com/content/...",
                "www.ft.com/content/...",
            ],
            "Brave": [
                "www.morningstar.com/news/dow-jones/...",
                "www.reuters.com/markets/us/...",
                "www.ft.com/content/...",
            ]
        }
    }
    ```

> **Please note: Since multiple search engines may index the same articles, some links might appear in more than one engine’s results.**

> **IMPORTANT: The content of this file is erased each time the script is executed.** 

*Ensure you save a copy of the results file before re-running the script.*

<br>

---

<br>

### SETTINGS

**PROXY:**  

> **Using proxies is recommended to avoid rate-limiting and enhance privacy during scraping.**

You can configure the proxies you want to use by editing the YAML file `settings/proxies.yaml`.

```yaml
proxies:
  - url: "https://10.10.1.11:8118"
    type: "https"
  - url: "https://127.0.0.1:8080"
    type: "https"
```

To **add** or **remove** a proxy, simply edit the "url" and "type" line.  

**To use proxies**, simply include the flag `-p` in your command. **A random proxy** will be then selected when scraping.  

**If you do not want to use proxies**, do not include the flag `-p` in your command.  

> **IMPORTANT: Using SOCKS proxies is not recommended and often leads to errors.**

<br>

---

<br>

### ADVANCED SOURCES SETTINGS

> **If you really want to have more sources and more categories, here's the advanced guide.**

<br>

**STEPS:**
- *Add the new category to the sources file*

<br>

**NEW CATEGORIES AND SOURCES:**

You can **add** sources and **categories** by editing or creating the YAML file `sources/sources.yaml`.

To create a new category "Ecology & Climate":
- **Create a new "type":** *"Ecology & Climate"*
- **Create a new simple "type_slug":** *"ecology"*
- **Add all of your sources:**
    - *name*
    - *URL*
    - *shortened URL*

> **Be sure to respect YAML indentation and formatting.**

```yaml
- type: "Ecology & Climate"
  type_slug: "ecology"
  sources:
    - name: "National Geographic"
      url: "https://www.nationalgeographic.com"
      short_url: "www.nationalgeographic.com"
    - name: "Mongabay"
      url: "https://www.mongabay.com"
      short_url: "www.mongabay.com"
    - name: "Environmental News Network (ENN)"
      url: "https://www.enn.com"
      short_url: "www.enn.com"
```

**The `type_slug` "ecology" becomes the `media-type` to use in your command.**

**Once your changes are saved**, you can run the following command to target this new category:

```
python wirepulsebot.py -st "petrol extraction" -ts "w" -mt "ecology" -p -c
```

<br>

**MANAGEMENT OF CUSTOM SOURCES FILES:**

**You can create specific directories** under `/sources` containing their own `sources.yaml` files.

*To use a specific file, simply replace `/sources/sources.yaml` content with the content of your custom file `/sources/mysources/sources.yaml`.*

> **WirePulseBOT will only parse the content of /sources/sources.yaml and will ignore files located in subdirectories.**

<br>

---

<br>

### REMINDER
  
*Search engines typically do not favor web scraping activities, as they may violate their terms of service. Excessive scraping can trigger rate-limiting mechanisms, leading to temporary or permanent blocking of your IP address, which may disrupt your ability to retrieve data effectively.*  

**To minimize these risks:**  
- *Use proxies.*  
- *Avoid sending too many requests in a short period.*  

<br>

---

<br>

> **If you have ideas for improvements, want to fix bugs, or suggest new features, feel free to contribute!**

> *[OSINT CHEAT SHEET by NotLoBi](https://github.com/NotLoBi/NotLoBi)*
