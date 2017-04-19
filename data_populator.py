from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///itemcategorywithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Dai Kikuchi", email="kikuchi.dai@gmail.com",
             picture="https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png")  # noqa
session.add(User1)
session.commit()

User2 = User(name="Hana Kikuchi", email="kikuchi.hana@gmail.com",
             picture="https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png")  # noqa
session.add(User2)
session.commit()

# category1 Fashion
category1 = Category(user_id=1, name="Fashion",
                     picture="https://image.ibb.co/cqG7qk/SD_clothingshoesjewelry_2x_CB274380260.png")  # noqa

session.add(category1)
session.commit()

# category1 items
category1item1 = Item(user_id=1, name="Blue T shirt",
                      description="Simple blue color T shirt! "
                                  "Reasonable price!!",
                      price="$10", category=category1,
                      picture="https://thumb.ibb.co/kRL1Fk/blue_tshirt.jpg")
session.add(category1item1)
session.commit()

# category2 Electronics
category2 = Category(user_id=1, name="Electronics",
                     picture="https://image.ibb.co/cta0Ak/SD_electronics_2x_CB270241075.png")  # noqa

session.add(category2)
session.commit()
# category2 items


category2item1 = Item(user_id=1, name="IPhone 7 Red 64GB",
                      description="Special edition of I phone "
                                  "7 beautiful and slick",
                      price="$800", category=category2,
                      picture="https://preview.ibb.co/j0QF85/170321093219_iphone_7_red_780x439.jpg")  # noqa
session.add(category2item1)
session.commit()

category2item2 = Item(user_id=1, name="IPhone SE 16GB",
                      description="Smaller screen size, Budget range Iphone!",
                      price="$400", category=category2,
                      picture="https://preview.ibb.co/gVG0ak/iphone_se_dt_debate.jpg")  # noqa

session.add(category2item2)
session.commit()

category2item3 = Item(user_id=1, name="I Phone case",
                      description="Fasionable, slick design I Phone case",
                      price="$20", category=category2,
                      picture='https://preview.ibb.co/hNHqak/the_birches_clear_iphone_case.jpg')  # noqa

session.add(category2item3)
session.commit()

# category3 Food

category3 = Category(user_id=1, name="Food",
                     picture="https://preview.ibb.co/huCDVk/SD_food_01_0006045739_F13_740x555.jpg")  # noqa

session.add(category3)
session.commit()

# category3 Item

category3item1 = Item(user_id=2, name="Japanese rice 10KG",
                      description="Japanese rice made in Japan. "
                                  "Very good taste!",
                      price="$50", category=category3,
                      picture="https://thumb.ibb.co/daUxMQ/Japanese_white_rice_kyoto_brand.jpg")  # noqa
session.add(category3item1)
session.commit()

category3item2 = Item(user_id=2, name="Japanese Wagyu beef 5KG",
                      description="Uttimate Japanese Wagyu beef.best beef!",
                      price="$1000", category=category3,
                      picture="https://thumb.ibb.co/jJQtvk/140930103747_wagyu_oita_bungo_beef_horizontal_large_gallery_1.jpg")  # noqa

session.add(category3item2)
session.commit()

category3item3 = Item(user_id=2, name="Japanese Udon",
                      description="Popualr Japanese noodle! "
                                  "easy to make! Health!",
                      price="$10", category=category3,
                      picture="https://thumb.ibb.co/ca4Q85/download.jpg")

session.add(category3item3)
session.commit()

# category4 Cosmetic

category4 = Category(user_id=1, name="Cosmetic",
                     picture="https://preview.ibb.co/fXi935/SD_beauty_category_tiles_makeup_tile_670x520.png")  # noqa

session.add(category4)
session.commit()

# category4 Item
category4item1 = Item(user_id=1, name="Organic Shampo",
                      description="Organic shampoo provides particularly "
                                  "gentle cleansing for stressed hair",
                      price="$30", category=category4,
                      picture="https://preview.ibb.co/cWWSMQ/aa_Bain_Vital_2_28.png")  # noqa

session.add(category4item1)
session.commit()

# category5 book

category5 = Category(user_id=1, name="Book",
                     picture="https://image.ibb.co/cg0YVk/SD_books_2x_CB274420682.png")  # noqa

session.add(category5)
session.commit()

# category5 Item
category5item1 = Item(user_id=1, name="Steve Jobs",
                      description="Biography on more than forty interviews "
                                  "with Steve Jobs conducted over two years",
                      price="$10", category=category5,
                      picture="https://thumb.ibb.co/c1h2O5/Isaacson_2011_Steve_Jobs.jpg")  # noqa

session.add(category5item1)
session.commit()

# category6 Outdoor

category6 = Category(user_id=1, name="Outdoor",
                     picture="https://image.ibb.co/e1fBGQ/SD_sportsoutdoors_2x_CB274422802.png")  # noqa

session.add(category6)
session.commit()

# category6 Item
category6item1 = Item(user_id=1, name="Hiking Mini portable Camping Stoves",
                      description="The mini stainless stove is designed for "
                                  "solid biomass fuel, such as tree root,bark",
                      price="$70", category=category6,
                      picture="https://thumb.ibb.co/iSCK35/r_BVa_HFZKz_SAJbal_AADo_ZVOm2bo524.jpg")  # noqa
session.add(category6item1)
session.commit()

print "added menu items!"
