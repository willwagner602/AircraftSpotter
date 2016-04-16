from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

# session imports
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SqlitePlaneImage(Base):

    __tablename__ = 'images'

    image_page = Column(String, primary_key=True)
    image_url = Column(String)
    name = Column(String)
    image_license = Column(String)
    license_text = Column(String)
    location = Column(String)
    author = Column(String)
    aircraft = Column(String)
    aircraft_type = Column(String)
    redownload_flag = Column(Boolean)

    def __str__(self):
        return self.image_page


class MySqlPlaneImage(Base):

    __tablename__ = 'images2'

    image_page = Column(String, primary_key=True)
    image_url = Column(String)
    name = Column(String)
    image_license = Column(String)
    license_text = Column(String)
    location = Column(String)
    author = Column(String)
    aircraft = Column(String)
    aircraft_type = Column(String)
    redownload_flag = Column(Boolean)
    description = Column(String)

    def __str__(self):
        return self.image_page


def convert_image_object(image_object):
    new_image = MySqlPlaneImage(image_page=image_object.image_page,
                                image_url=image_object.image_url,
                                name=image_object.name,
                                image_license=image_object.image_license,
                                license_text=image.license_text,
                                location=image_object.location,
                                author=image_object.author,
                                aircraft=image_object.aircraft,
                                aircraft_type=image_object.aircraft_type,
                                redownload_flag=image_object.redownload_flag)
    return new_image

# setup engines
if __name__ == '__main__':
    mysql_engine = create_engine('mysql+pymysql://root:semperfi@localhost:3306/plane_viewer')
    sqlite_engine = create_engine('sqlite:///images.sqlite3')

    MysqlSessionMaker = sessionmaker(bind=mysql_engine)
    SqliteSessionMaker = sessionmaker(bind=sqlite_engine)

    mysql_session = MysqlSessionMaker()
    sqlite_session = SqliteSessionMaker()

    sqlite_images = sqlite_session.query(SqlitePlaneImage).all()

    for image in sqlite_images:
        mysql_image = convert_image_object(image)

        mysql_session.add(mysql_image)
        try:
            mysql_session.commit()
            print('Loaded', image)
        except exc.IntegrityError:
            mysql_session.rollback()
            print("Image {} already loaded".format(image))

    mysql_images = mysql_session.query(MySqlPlaneImage).all()
    print(len(mysql_images))