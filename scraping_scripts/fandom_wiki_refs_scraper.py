from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

links_df_original = pd.read_csv('./Datasets/scraped/simpsons_fandom_wiki_links.csv')
links_df = links_df_original.sort_values(['season', 'episode'], ascending=[True, True])
links_df.index = np.arange(1, len(links_df) + 1)

ref_types = ['Trivia', 'Cultural references', 'Continuity', 'Goofs', 'Cultural References',
             'Appearances in other media', 'Trivia/Goofs', 'Goofs/Trivia', 'Previous Episode References',
             'Production Notes', 'Connections to future episodes', "Krusty's Birthday Buddies", 'Movie Moment',
             'Trivia/Cultural References', 'Censorship', 'Cultural Reference', 'U.S. Syndication Cuts',
             'Beatles references', 'Notes and references', 'Notes', 'Legacy', 'Running Gags:', 'Seven Deadly Sins',
             'Previous and Future Episode References', 'Goofs and Continuity Errors', 'Pants Goof', 'Deleted scenes',
             'DVD Release', 'Censorship and Bans', 'Reception and Legacy', 'Reception', 'Airings', 'Pranks',
             'Alternate Versions', 'Call-Backs', 'External Links', 'Premiere', 'Previous episode references',
             'Broadcast', 'Aerospace References', 'Awards', 'China References', 'Production', 'Goofs/errors',
             'Broadcasting Information', 'Errors', 'World War II references', 'Goof', 'Notes on Known Profiles',
             'Reference links', 'Songs', 'Differences from Lady and the Tramp', 'Confusion',
             'References to other episodes', 'Music', 'Factual Errors', 'International premieres', 'Cuts',
             'References to Toy Story in Condiments', "Goofs'", 'Continuity Errors', 'In-show references',
             'Culture References', 'Characters seen in the Advent Calendar', 'Continually',
             'Previous Episodes References', 'Call-Backs to Episodes (In order of appearance in the episode)']


# for all headers in the list find <ul> lists that may be separated with figures or smaller header
# count <li> elements in each list
def get_ref_counts(episode_id):
    ref_page_link = links_df['url'].iloc[episode_id - 1] + '/References'
    req = requests.get(ref_page_link)
    ref_page = BeautifulSoup(req.text, 'html.parser')
    headers = ref_page.find_all('h2')
    counter_dict = {}
    h_pointer = headers[0]
    for header in headers:
        if header.text in ref_types:
            h_pointer = header
            break

    counter_dict[h_pointer.text] = 0
    for sibling in h_pointer.next_siblings:
        if sibling.name in ['h2', 'ul']:
            # switch pointer to new header if it was encountered
            if sibling.name == 'h2':
                if sibling.text in ref_types:
                    h_pointer = sibling
                    counter_dict[h_pointer.text] = 0
                elif sibling.text == 'Call-Backs to previous episodes':
                    # hard-coded cuz it was easier to count then to write specialized parser for 1 page
                    counter_dict[sibling.text] = 31
            else:
                # count number of li elements in ul tag
                counter = 0
                for li in sibling.contents:
                    if li.name == 'li':
                        counter = counter + 1
                # increment total number of il elements of a pointed h2
                counter_dict[h_pointer.text] = counter_dict[h_pointer.text] + counter
    return counter_dict


def save_ref_counts():
    counter_dicts = []
    for i in range(len(links_df)):
        cd = get_ref_counts(i + 1)
        counter_dicts.append(cd)

    list_df = []
    for i, cd in enumerate(counter_dicts):
        list_df.append(pd.DataFrame(cd, index=[i]))
    joined_df = pd.concat(list_df)

    new_joined_df = joined_df.fillna(0)
    new_joined_df = new_joined_df.astype(int)
    new_joined_df.to_csv('./Datasets/scraped/references.csv', index=False)


def select_columns(data, columns):
    return data.reindex(columns=columns)


def add_column_from_existing(data, new_column_name, columns_names):
    data[new_column_name] = pd.Series(dtype=float)
    for cnt, name in enumerate(columns_names):
        if cnt == 0:
            data[new_column_name] = data.loc[:, name].fillna(value=0)
        else:
            data[new_column_name] += data.loc[:, name].fillna(value=0)
    return data


def clean_ref_counts():
    references_df = pd.read_csv('./Datasets/scraped/references.csv')
    references_df.index += 1

    cult_refs_count_cols = ['Cultural references', 'Cultural References', 'Trivia/Cultural References',
                            'Cultural Reference', 'Notes and references', 'Beatles references',
                            'References to Toy Story in Condiments', 'Culture References']
    self_refs_count_cols = ['Previous Episode References', 'Previous and Future Episode References',
                            'Previous episode references', 'References to other episodes', 'In-show references',
                            'Previous Episodes References', 'Call-Backs', 'Call-Backs to previous episodes',
                            'Call-Backs to Episodes (In order of appearance in the episode)']
    goofs_count_cols = ['Goofs', 'Trivia/Goofs', 'Goofs/Trivia', 'Goofs and Continuity Errors', 'Pants Goof',
                        'Goofs/errors', 'Goof', "Goofs'"]
    errors_count_cols = ['Errors', 'Continuity Errors', 'Factual Errors', 'Goofs and Continuity Errors', 'Goofs/errors']

    new_cols_names = ['cult_refs_count', 'self_refs_count', 'goofs_count', 'errors_count']
    feature_counts = (
        references_df
        .pipe(add_column_from_existing, new_cols_names[0], cult_refs_count_cols)
        .pipe(add_column_from_existing, new_cols_names[1], self_refs_count_cols)
        .pipe(add_column_from_existing, new_cols_names[2], goofs_count_cols)
        .pipe(add_column_from_existing, new_cols_names[3], errors_count_cols)
        .pipe(select_columns, new_cols_names)
    )

    feature_counts.index.names = ['episode_id']
    feature_counts.to_csv('./Datasets/scraped/ref_counts_clean.csv', index=True)
