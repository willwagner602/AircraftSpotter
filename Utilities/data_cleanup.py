from datetime import datetime, timedelta
import requests
import time
import sqlite3

from bs4 import BeautifulSoup


def get_page(page):
    """
    A simple wrapper around the BeautifulSoup.get function.
    :param page:
    :return HTML document:
    """
    try:
        return BeautifulSoup(requests.get(page).text.encode('ascii', 'replace'), 'html.parser')
    except requests.exceptions.ConnectionError:
        time.sleep(5)
        return get_page(page)


def retrieve_author(image_page, session, page_type):
    page = get_page(image_page)

    if page_type == 'photographer':
        container = 'span'
    elif page_type == 'author':
        container = 'td'

    # get picture info
    try:
        author = page.find('td', id='fileinfotpl_aut').find_next(container).text
    except AttributeError:
        author = "Author not found"
    insert_author(image_page, author, session)


def retrieve_description(image_page, cursor):
    page = get_page(image_page)

    try:
        description = page.find('td', id='fileinfotpl_desc').find_next('td').text
    except AttributeError:
        try:
            description = page.find('p', id='mw-imagepage-content').find_next('li').text
        except AttributeError:
            description = 'No description on page'
            print(image_page)

    update_description(image_page, clean_text_for_sql(description), cursor)


def clean_entries_missing_data(cursor):
    descriptions_cleaned = 0

    entries_missing_data = cursor.execute("""SELECT image_page FROM images WHERE author IN ('Photographer', 'Author')
                                        OR description IS NULL OR description = 'No description on page'""").fetchall()

    last_image_time = datetime(2016, 1, 1)

    for entry in entries_missing_data:
        if descriptions_cleaned % 1000 == 0:
            print("Cleaned {} descriptions.".format(descriptions_cleaned))
        while datetime.now() < last_image_time + timedelta(seconds=1):
            pass
        last_image_time = datetime.now()
        retrieve_description(entry[0], cursor)
        retrieve_author(entry[0], cursor, 'photographer')
        descriptions_cleaned += 1



def clean_text_for_sql(author):
    return author.replace("'", "''")


def clean_authors(cursor):
    # query all files where the author is Photographer
    photographers = cursor.execute("""SELECT image_page FROM images WHERE author IN ('Photographer', 'Author') OR description IS NULL OR description = 'No description on page'""").fetchall()

    last_image_time = datetime(2016, 1, 1)

    for photographer in photographers:
        while datetime.now() < last_image_time + timedelta(seconds = 1):
            # do nothing to limit the rate of requests to wikimedia
            pass
        retrieve_author(photographer[0], cursor, 'photographer')
        last_image_time = datetime.now()
        connection.commit()

    authors = cursor.execute("""SELECT image_page FROM images WHERE author = 'Author'""").fetchall()

    for author in authors:
        while datetime.now() < last_image_time + timedelta(seconds = 1):
            # do nothing to limit the rate of requests to wikimedia
            pass
        retrieve_author(author[0], cursor, 'author')
        last_image_time = datetime.now()
        connection.commit()

    connection.close()


def insert_author(image, author, cursor):
    update = """UPDATE images SET author = '{}' WHERE image_page = '{}'""".format(clean_text_for_sql(author), image)
    try:
        cursor.execute(update)
    except sqlite3.OperationalError as e:
        print(e)
        print(update)
        exit()


def update_description(image, description, cursor):
    update = """UPDATE images SET description = '{}' WHERE image_page = '{}'""".format(description, image)
    try:
        cursor.execute(update)
        connection.commit()
    except sqlite3.OperationalError as e:
        print(e)
        print(update)
        exit()

if __name__ == "__main__":

    connection = sqlite3.connect('images.sqlite3')
    current_cursor = connection.cursor()

    clean_entries_missing_data(current_cursor)
