from bs4 import BeautifulSoup
import requests
import pandas as pd

max_seasons = 28
season_page_url_base = 'https://simpsons.fandom.com/wiki/Season_'
season_page_urls = [season_page_url_base + str(i + 1) for i in range(max_seasons)]


def get_links_by_season(season_id: int, verbose=False):
    req = requests.get(season_page_urls[season_id])
    if verbose:
        print(f"Request terminated with status code {req.status_code}")
        print(f"Response encoded with {req.encoding}")
    season_page = BeautifulSoup(req.text, 'html.parser')

    episodes_links = {"title": [], "url": [], "episode": [], "season": []}

    tables = season_page('table')
    table_id = 0
    for i, table in enumerate(tables):
        if table.has_attr('class') and table['class'][0] == 'wikitable':
            table_id = i
            break
    rows = tables[table_id].find_all('tr')
    episode_num = (len(rows) - 1)
    episode_counter = 0
    for i in range(episode_num + 1):
        cols = rows[i].find_all('td')
        title_col_id = 4 if (16 < season_id < 21) else (3 if season_id == 21 else 2)
        if title_col_id < len(cols):
            link = cols[title_col_id].find_all('a', href=True)
            if len(link) > 0:
                episodes_links['title'].append(link[0].text)
                episodes_links['url'].append('https://simpsons.fandom.com' + link[0]['href'])
                episodes_links['season'].append(season_id + 1)
                episode_counter = episode_counter + 1
                episodes_links['episode'].append(episode_counter)
    return episodes_links


def save_links_to_csv():
    links_dict = [get_links_by_season(i) for i in range(max_seasons)]
    links_df = [pd.DataFrame(links_dict[i]) for i in range(max_seasons)]
    links_per_episode_df = pd.concat(links_df)
    links_per_episode_df[['episode', 'season']] = links_per_episode_df[['episode', 'season']].astype(int)
    links_per_episode_df.to_csv('simpsons_fandom_wiki_links.csv', index=False)
