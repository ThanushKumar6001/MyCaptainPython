import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser=argparse.ArgumentParser()
parser.add_argument("--page_num_max", help="Enter the number of pages to parse", type=int)
parser.add_argument("--dbname", help="Enter the name of db",type=str)
args=parser.parse_args()

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_num_Max=args.page_num_max
scraped_info_list=[]
for page_num in range(1,page_num_Max):
    url=oyo_url + str(page_num)
    print("GET Request for: " + url)
    req=requests.get(url)
    content=req.content
    soup=BeautifulSoup(content, "html.parser")

    all_hotels=soup.find_all("div", {"class": "hotelCardListing"})
    for hotel in all_hotels:
        hotel.dict={}
        hotel_dict["name"]=hotel_name=hotel.find("h3", {"class": "listingHotelDescription__hotelName"}).text
        hotel_dict["address"]=hotel_address=hotel.find("span",{"itemprop": "streetAddress"}).text
        hotel_dict["price"]=hotel_price=hotel.find("span", {"class": "listingPrice__FinalPrice"}).text
        try:
            hotel_dict["rating"]=hotel_rating=hotel.find("span", {"class": "hotelRating__ratingSummary"}).text
        except AttributError:
            hotel_dict["rating"] = None
        parent_amenities_element=hotel.find("div", {"class":  "amenityWrapper"})
        amenities_list=[]
        for amenity in parent_amenities_element.find_all("div", {"class":  "amenityWrapper__amenity"}):
            amenities_list.append(amenity.find("span", {"class": "d-body-sm"}).text)
        hotel_dict["amenities"]='.'.join(amenities_list[:-1])
   
        scrapped_info_list.append(hotel_dict)
        connect.insert_into_table(args.dbname, tuple(hotel_dict.values()))

dataFrame=pandas.DataFrame(scrapped_info_list)
print("Creating csv file...")
dataFrame.to_csv("Oyo.csv")
connect.get_hotel_info(args.dbname)
