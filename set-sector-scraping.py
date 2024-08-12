from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import datetime
import time

CHROMEDRIVER_PATH = r"C:\<path>\chromedriver.exe"

sector = {
    "AGRO":["AGRI","FOOD"],
    "CONSUMP":["FASHION","HOME","PERSON"],
    "FINCIAL":["BANK",'FIN','INSUR'],
    "INDUS":["AUTO","IMM","PAPER","PETRO","PKG","STEEL"],
    "PROPCON":["CONMAT","PROP","PF&REIT","CONS"],
    "RESOURC":["ENERG","MINE"],
    "SERVICE":["COMM","HELTH","MEDIA","PROF","TOURISM","TRANS"],
    "TECH":["ETRON","ICT"]
    }

def parseInfo(sector_name, target_url):
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(target_url)
    time.sleep(3)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content,'html.parser')

    tmp_info = {}
    tmp_info["sector_name"] = str(sector_name).upper()
    try:
        tmp_info["timestamp_info"] = soup.find("div",{"class":"d-block quote-market-lastInfo me-2 me-xl-3"}).find("span").text
    except:
        tmp_info["timestamp_info"] = None
    try:
        tmp_info["market_status"] = soup.find("div",{"class":"d-block quote-market-status me-2 me-xl-4"}).find("span",{"class":"market-close"}).text
    except:
        tmp_info["market_status"] = None
    try:
        tmp_info["open_price"] = soup.find("div",{"class":"d-block quote-market-open pe-1 pe-xl-3"}).find("span",{"class":"ms-2 ms-xl-4"}).text
    except:
        tmp_info["open_price"] = None
    try:
        tmp_info["close_price"] = soup.find("div",{"class":"value text-white mb-0 me-2 lh-1 stock-info"}).text.replace("\n ","")
    except:
        tmp_info["close_price"] = None
    try:
        tmp_info["price_change"] = soup.find("h3",{"class":"d-flex mb-0 pb-2 theme-success"}).text
    except:
        try:
            tmp_info["price_change"] = soup.find("h3",{"class":"d-flex mb-0 pb-2 theme-danger"}).text
        except:
            tmp_info["price_change"] = None
    try:
        tmp_info["high_price"] = soup.find("div",{"class":"d-block quote-market-high px-1 px-xl-3"}).find("span",{"class":"ms-2 ms-xl-4"}).text
    except:
        tmp_info["high_price"] = None
    try:
        tmp_info["low_price"] = soup.find("div",{"class":"d-block quote-market-low px-1 px-xl-3"}).find("span",{"class":"ms-2 ms-xl-4"}).text
    except:
        tmp_info["low_price"] = None
    try:
        tmp_info["market_volume"] = soup.find("div",{"class":"d-block quote-market-volume px-1 px-xl-3"}).find("span",{"class":"ms-2 ms-xl-4"}).text
    except:
        tmp_info["market_volume"] = None
    try:
        tmp_info["market_cost"] = soup.find("div",{"class":"d-block quote-market-cost ps-2 ps-xl-3"}).find("span",{"class":"ms-2 ms-xl-4"}).text
    except:
        tmp_info["market_cost"] = None
    driver.close()
    driver.quit()
    return tmp_info   

if __name__ == "main":
    
    major_sector_list = []
    minor_sector_list = []
    for key,value in sector.items():
        print(key,value)
        major_sector_url = "https://www.set.or.th/th/market/index/set/" + key.lower()
        # print(major_sector_url)
        major_sector_list.append(parseInfo(key.lower(), major_sector_url))
        for v in value:
            minor_sector_url = major_sector_url+"/"+v.lower()
            # print("  .."+minor_sector_url)
            minor_sector_list.append(parseInfo(v.lower(),minor_sector_url))
            
    # convert to DataFrame
    major_sector_df = pd.DataFrame(major_sector_list)
    minor_sector_df = pd.DataFrame(minor_sector_list)

    # export to csv
    major_sector_fn = "major_sector_"+str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))+".csv"
    minor_sector_fn = "minor_sector_"+str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))+".csv"

    major_sector_df.to_csv(major_sector_fn,index=False,encoding="TIS-620")
    minor_sector_df.to_csv(minor_sector_fn,index=False,encoding="TIS-620")