from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
import sqlalchemy
import os


def confirm_image_download(image, folders):
    """
    Confirm the existence of the physical image file in its correct location on disk
    :param image: image object
    :param folders: list of all image folders
    :return: bool of success
    """

    # necessary information to lookup image in dictionary
    name = image[2]
    location = image[5]

    try:
        if name in folders[location]:
            return True
        else:
            return False
    except KeyError:
        return False


def mark_image_for_download(image, db_connection):
    """
    Update image's flag in SQL to redownload the physical file
    :param image:
    :param db_connection:
    :return:
    """
    url = image[0]
    update_statement = """UPDATE images SET redownload_flag = 1 WHERE image_page = '{}'""".format(url)
    db_connection.execute(update_statement)
    db_connection.commit()


def get_image_lists(base_directory):
    """
    Setup lists of all the images found in each directory, to save time over repeatedly scanning directories
    :param base_directory:
    :return:
    """
    images_by_folder = {}
    os.chdir(base_directory)
    print(base_directory)
    for folder in os.listdir():
        print(folder)
        os.chdir(folder)
        images_by_folder[folder] = os.listdir()
        os.chdir(base_directory)
    return images_by_folder

# setup base class for database models
BASE = declarative_base()


class Image(BASE):
    __tablename__ = 'images'
    image_page = Column(String(200), primary_key=True)
    image_url = Column(String(200))
    name = Column(String(100))
    image_license = Column(String(100))
    license_text = Column(String(1000))
    location = Column(String(200))
    author = Column(String(100))
    aircraft = Column(String(100))
    aircraft_type = Column(String(50))

    def __init__(self, image_page, image_url, name, image_license, license_text, location, author,
                 aircraft, aircraft_type):
        self.image_page = image_page
        self.image_url = image_url
        self.name = name
        self.image_license = image_license
        self.license_text = license_text
        self.location = location
        self.author = author
        self.aircraft = aircraft
        self.aircraft_type = aircraft_type

    def __repr__(self):
        return "<Image(url='{}', name='{}', license='{}', location='{}', author='{}'".format(
                      self.image_page, self.name, self.image_license, self.location, self.author)


def create_table():
    engine = sqlalchemy.create_engine('sqlite:///' + os.getcwd() + '\\images.db')
    BASE.metadata.create_all(engine)

if __name__ == "__main__":

    # setup DB connection
    engine = sqlalchemy.create_engine('sqlite:///A:\Dropbox\Projects\PlaneViewer\\images.sqlite3')
    connection = engine.connect()
    
    # get each image from the DB that has an Aircraft assigned to it
    identified_aircraft = connection.execute('''SELECT * FROM images WHERE redownload_flag = 0 AND use_flag = 1''')
    
    missing_image_count = 0
    images_by_folder = get_image_lists(r'A:\Projects\PycharmProjects\PlaneScraper\images')
    
    for folder in images_by_folder:
        print(folder)
    
    print(' Distinct Locations ')
    
    locations = connection.execute('''SELECT DISTINCT location FROM images''')
    
    for loc in locations:
        print(loc)

    # iterate over images where the aircraft is identified and download them
    for i, row in enumerate(identified_aircraft):
        if i % 100 == 0:
            print("Missing images: {} out of {}".format(missing_image_count, i))
        if not confirm_image_download(row, images_by_folder):
            mark_image_for_download(row, connection)
            missing_image_count += 1

    print("Missing {} images.".format(missing_image_count))

    connection.close()