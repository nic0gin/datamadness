import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


def save_data(div):
    data = None
    if div != None:
        data = div.find_all(['a', 'span'])
        data = [data[i].text for i in range(len(data))]
        data = ', '.join(data)

    return data


def save_data_blackboard(div):
    '''Find the div in the div and save the text'''
    data = None
    if div != None:
        div = div.find('div')
        data = div.text
    return data


def get_data(url):
    req = requests.get(url)
    page = BeautifulSoup(req.text, 'html.parser')

    div = page.find('div', attrs={'data-source': 'specialGuestVoices'})
    production_code = page.find('div', attrs={'data-source': 'productionCode'})
    production_code = production_code.find('div').text
    voice = None

    if div != None:
        content = div.find_all(['a', 'span'])

        voice = [content[i].text for i in range(len(content)) if i % 2 == 0]
        voice = ', '.join(voice)

    chalkboard_gag = save_data_blackboard(page.find('div', attrs={'data-source': 'blackboardText'}))
    couch_gag = save_data(page.find('div', attrs={'data-source': 'couchGag'}))
    show_runner = save_data(page.find('div', attrs={'data-source': 'Show Runner'}))
    written_by = save_data(page.find('div', attrs={'data-source': 'Written By'}))
    directed_by = save_data(page.find('div', attrs={'data-source': 'Directed By'}))

    return [production_code, voice, chalkboard_gag, couch_gag, show_runner, written_by, directed_by]


def scrape_box_data():
    links = pd.read_csv('./Datasets/scraped/simpsons_fandom_wiki_links.csv')

    box_data = pd.DataFrame(
        columns=['production_code', 'voice', 'chalkboard_gag', 'couch_gag', 'show_runner', 'written_by', 'directed_by'])
    for link in tqdm(links['url']):
        box_data.loc[len(box_data.index)] = get_data(link)

    box_data.to_csv('./Datasets/scraped/box_data.csv', index=False)


def clean_box_data():
    df = pd.read_csv('./Datasets/scraped/box_data.csv')
    # ignore nan values and strip 'Couch Gag,' from the string in the column 'couch_gag'

    df['couch_gag'] = df['couch_gag'].astype(str).map(lambda x: x.lstrip('Couch Gag,'))
    print(df.head(100))
    df.to_csv('./Datasets/scraped/box_data.csv', index=False)
    print('Done')
