__author__="Anurag"
from DataCollection.CareerBuilder import jd_scraper as CB_parser
from DataCollection.Dice import jd_scraper as Dice_parser
from DataCollection.FreshersWorld import jd_scraper as FresherWorld_parser
from DataCollection.Indeed import jd_scraper as Indeed_parser
from DataCollection.Monster import jd_scraper as Monster_parser
from DataCollection.Naukri import jd_scraper as Naukri_parser
from DataCollection.Shine import jd_scraper as Shine_parser
from DataCollection.WisdomJobs import jd_scraper as WisdomJobs_parser
import datetime


def CareerBuilder_links_scraper(database,keyword,location,browser="phantomjs"):
    CB_parser.jobs_links_scraping().linksAutomation(database=database,keyword=keyword,location=location,browser=browser)

def Dice_links_scraper(database,keyword,location,browser="phantomjs"):
    Dice_parser.job_links_scraping().linksAutomation(database=database,keyword=keyword,location=location,browser=browser)

def FresherWorld_links_scraper(database,keyword,location,browser="phantomjs"):
    FresherWorld_parser.job_link_scraping().linksAutomation(database=database,keyword=keyword,location=location,browser=browser)

def Indeed_links_scraper(database,keyword,location,browser="phantomjs"):
    Indeed_parser.job_links_scraping().linksAutomation(database=database,keyword=keyword,location=location,browser=browser)

def Monster_links_scraper(database,keyword,location,browser="phantomjs"):
    Monster_parser.job_link_scraping().linksAutomation(database=database,keyword=keyword,location=location,browser=browser)

def Naukri_links_scraper(database,keyword,location,browser="phantomjs"):
    Naukri_parser.job_link_scraping().linksAutomation(database=database,keyword=keyword,location=location,browser=browser)

def Shine_links_scraper(database,keyword,location,browser="phantomjs"):
    Shine_parser.job_link_scraping().linksAutomation(database=database,keyword=keyword,location=location,browser=browser)

def WisdomJobs_links_scraper(database,keyword,location,browser="phantomjs"):
    WisdomJobs_parser.job_link_scraping().linksAutomation(database=database,keyword=keyword,location=location,browser=browser)

def CareerBuilder_description_scraper(database,browser="phantomjs"):
    CB_parser.job_description_scraping().descriptionAutomation(database=database,browser=browser)

def Dice_description_scraper(database,browser="phantomjs"):
    Dice_parser.job_description_scraping().descriptionAutomation(database=database,browser=browser)

def Indeed_description_scraper(database,browser="phantomjs"):
    Indeed_parser.job_description_scraping().descriptionAutomation(database=database,browser=browser)

def FresherWorld_description_scraper(database,browser="phantomjs"):
    FresherWorld_parser.job_description_scraping().descriptionAutomation(database=database,browser=browser)

def Monster_description_scraper(database,browser="phantomjs"):
    Monster_parser.job_description_scraping().descriptionAutomation(database=database,browser=browser)

def Naukri_description_scraper(database,browser="phantomjs"):
    Naukri_parser.job_description_scraping().descriptionAutomation(database=database,browser=browser)

def Shine_description_scraper(database,browser="phantomjs"):
    Shine_parser.job_description_scraping().descriptionAutomation(database=database,browser=browser)

def WisdomJobs_description_scraper(database,browser="phantomjs"):
    WisdomJobs_parser.job_description_scraping().descriptionAutomation(database=database,browser=browser)

def links_scraper(database,keyword,location,browser,CB=False,Dice=False,FresherWorld =False,Indeed=False,Monster=False,Naukri=False,Shine=False,WisdomJobs=False):
    executors_list = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        if CB:
            executors_list.append(executor.submit(CareerBuilder_links_scraper, database, keyword, location, browser))
        if Dice:
            executors_list.append(executor.submit(Dice_links_scraper, database, keyword, location, browser))
        if FresherWorld:
            executors_list.append(executor.submit(FresherWorld_links_scraper, database, keyword, location, browser))
        if Indeed:
            executors_list.append(executor.submit(Indeed_links_scraper, database, keyword, location, browser))
        if Monster:
            executors_list.append(executor.submit(Monster_links_scraper, database, keyword, location, browser))
        if Naukri:
            executors_list.append(executor.submit(Naukri_links_scraper, database, keyword, location, browser))
        if Shine:
            executors_list.append(executor.submit(Shine_links_scraper, database, keyword, location, browser))
        if WisdomJobs:
            executors_list.append(executor.submit(WisdomJobs_links_scraper, database, keyword, location, browser))

    for x in executors_list:
        print(x.result())

def description_scraper(database,browser,CB=False,Dice=False,FresherWorld =False,Indeed=False,Monster=False,Naukri=False,Shine=False,WisdomJobs=False):
    executors_list = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        if CB:
            executors_list.append(executor.submit(CareerBuilder_description_scraper, database, browser))
        if Dice:
            executors_list.append(executor.submit(Dice_description_scraper, database, browser))
        if FresherWorld:
            executors_list.append(executor.submit(FresherWorld_description_scraper, database, browser))
        if Indeed:
            executors_list.append(executor.submit(Indeed_description_scraper, database, browser))
        if Monster:
            executors_list.append(executor.submit(Monster_description_scraper, database, browser))
        if Naukri:
            executors_list.append(executor.submit(Naukri_description_scraper, database, browser))
        if Shine:
            executors_list.append(executor.submit(Shine_description_scraper, database, browser))
        if WisdomJobs:
            executors_list.append(executor.submit(WisdomJobs_description_scraper, database, browser))

    for x in executors_list:
        print(x.result())

if __name__ == '__main__':
    from pymongo import MongoClient
    from concurrent.futures import ThreadPoolExecutor

    database = MongoClient("localhost",27017)["jd-scraping-testing"]["job_description"]

    keyword = "sales manager"
    location = ""
    browser = "phantomjs"
    ############## to start scraping job description links ##################
    links_scraper(database=database,keyword=keyword,location=location,browser=browser,CB=True)
    ############# to start scraping job description full description #######
    # description_scraper(database=database,browser=browser,CB=True,Dice=True,Shine=True)
