from scraping_scripts.fandom_wiki_refs_scraper import save_ref_counts, clean_ref_counts
from scraping_scripts.fandom_wiki_links_scraper import save_links_to_csv
from scraping_scripts.imdb_scraper import save_imdb_data
from scraping_scripts.scraping_box_data import scrape_box_data, clean_box_data


if __name__ == '__main__':
    # save links for simpsons wiki fandom for each episode
    save_links_to_csv()

    # save counts of reference page from simpsons wiki fandom from each episode
    save_ref_counts()
    # clean the reference counts
    clean_ref_counts()

    # scrape island box data from simpsons wiki fandom for each episode
    scrape_box_data()
    # clean the box data
    clean_box_data()

    # scrape imdb demographics rating data for each episode
    save_imdb_data()
