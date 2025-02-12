import yaml

from settings.canvas import (
    canvas_invalid_method,
    canvas_parser_error,
    canvas_parser_no_file,
    canvas_parser_yaml_error
)

'''
Open YAML sources file and parse URLs 
for future scraping.
'''
def extract_urls(media_type: str) -> list:
    try:
        with open("sources/sources.yaml", 'r') as file:
            data = yaml.safe_load(file)

    except FileNotFoundError:
        canvas_parser_no_file()
        return []
    
    except yaml.YAMLError as e:
        canvas_parser_yaml_error(e)
        return []

    source_urls = []

    for section in data.get('media', []):
        # Filter by media type
        if section.get('type_slug', '').lower() == media_type.lower():
            if 'sources' in section:
                for source in section['sources']:
                    source_urls.append(source['short_url'])
            if 'regions' in section:
                for region in section['regions']:
                    for source in region['sources']:
                        source_urls.append(source['short_url'])
        
    return source_urls


'''
Prepare dorks for search engine scrapers:

The user defines the terms to search, the timestamp, and the media type.
'''
def format_dorks(search_term: str, search_timestamp: str, media_type: str) -> dict:
    source_urls = extract_urls(media_type)

    if not source_urls:
        canvas_invalid_method()
        return

    search_dorks = {}

    try:
        if search_term and search_timestamp:
            # Dorks format : "example" site:www.news.com
            for url in source_urls:
                search_dorks.update({f'"{search_term}" site:{url}': search_timestamp})

            return search_dorks

    except Exception as e:
        canvas_parser_error(e)
        return
    

'''
Open YAML sources file and check
for valid media types.
'''
def valid_media_types() -> list:
    media_types_list = []

    try:
        with open("sources/sources.yaml", 'r') as file:
            data = yaml.safe_load(file)

    except FileNotFoundError:
        canvas_parser_no_file()
        return []
    
    except yaml.YAMLError as e:
        canvas_parser_yaml_error(e)
        return []

    for section in data.get('media', []):
        # Filter by media type and get type_slug
        media_types_list.append(section.get('type_slug', '').lower())
    
    return media_types_list