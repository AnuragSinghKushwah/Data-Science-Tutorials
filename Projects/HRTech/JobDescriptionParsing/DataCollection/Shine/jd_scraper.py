__author__="Anurag"
from selenium import webdriver
from bs4 import BeautifulSoup
import time,datetime,re,random
# from urllib.parse import urlencode
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox import firefox_profile
from DataCollection.config import Shine_config
config = Shine_config()
import logging
from DataCollection.config import logfile,logformat
class job_link_scraping():
    def __init__(self):
        self.logger = logging.getLogger("Shine job links scraping")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(filename=logfile)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def linksAutomation(self, database, keyword, location=None, browser="phantomjs"):

        if browser == "firefox":
            self.driver = webdriver.Firefox()
        elif browser == "chrome":
            self.driver = webdriver.Chrome(config["chromepath"])
        else:
            self.driver = webdriver.PhantomJS(config["phantomjspath"])

        self.driver.delete_all_cookies()

        self.baseurl = "https://www.shine.com/job-search/"

        if location:
            self.searchurl = self.baseurl + keyword.strip().lower().replace(" ","-") + "-jobs-in-" + location.lower()
        else:
            self.searchurl = self.baseurl + keyword.strip().lower().replace(" ","-") + "-jobs"

        self.logger.info("search url - %s",self.searchurl)
        self.driver.get(self.searchurl)
        pageCount = self.pagecount(self.driver.page_source)
        self.logger.info("total jobs found - %s",pageCount)

        for pagenumber in range(1, round(pageCount/ 20)):
            time.sleep(random.randint(5, 10))
            trickurl = self.searchurl+"-"+str(pagenumber)
            self.logger.info("search url - %s",trickurl)
            self.driver.get(trickurl)
            for job in self.linksScraper(self.driver.page_source):
                try:
                    self.logger.info("job link - %s",job)
                    self.logger.info("inserting job description - %s",database.insert(job))
                except Exception as e:
                    self.logger.fatal("exception in inserting data - %s", e)
                    pass

        self.driver.close()

    def pagecount(self, page):
        Soup = BeautifulSoup(page, "lxml")
        try:
            jobs = Soup.find(config["job_count"]["name"], config["job_count"]["attrs"]).text.split()[0]
            totaljobs=0
            if "," in jobs:
                jbs = jobs.split(",")
                totaljobs = int(jbs[0])*1000+int(jbs[1])
            else:
                totaljobs= int(jobs)
            return totaljobs
        except Exception as e:
            self.logger.fatal("exception in finding total jobs",e)
            return "Error"

    def linksScraper(self,page):
        Soup = BeautifulSoup(page,"lxml")
        descriptionArray = []
        postedday = [i.text for i in Soup.find_all(config["job_posted"]["name"], config["job_posted"]["attrs"])]

        for indx,jobs in enumerate(Soup.find_all(config["job_section"]["name"], config["job_section"]["attrs"])):
            descriptionurl = ""
            descriptionId = ""
            descriptionTitle = ""
            employerName = ""
            exprequired = ""
            location = ""
            skillsRequired = ""
            summary = ""
            salary = ""
            recruiter = ""
            postedDay = ""
            morejobs = ""

            ####################### Title ###############################
            try:
                descriptionTitle = jobs.find(config["job_title"]["name"], config["job_title"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in job title - %s",e)
                pass

            ####################### Description Url #####################
            try:
                descriptionurl = "https://www.shine.com"+jobs.find(config["job_url"]["name"], config["job_url"]["attrs"])["href"].strip()
            except Exception as e:
                self.logger.exception("exception in job url - %s",e)
                pass

            ####################### Description ID ######################
            try:
                descriptionId = jobs.find(config["job_url"]["name"], config["job_url"]["attrs"])["data-jid"].strip()
            except Exception as e:
                self.logger.exception("exception in job id - %s",e)
                pass

            ####################### Job Summary #########################
            try:
                summary = jobs.find(config["job_summary"]["name"], config["job_summary"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in job summary - %s",e)
                pass
            # ####################### Job Employer ########################
            try:
                employerName = jobs.find(config["job_employer"]["name"], config["job_employer"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in employer name - %s",e)
                pass

            ####################### Job Employer Url ####################
            # try:
            #     morejobs = jobs.find("span",{"class":"hidden-xs"}).find("a",{"class":"dice-btn-link"})["href"].strip()
            # except Exception as e:
            #     print("exception in employer url ",e)
            #     pass
            ######################## Job Location #######################
            try:
                location = jobs.find(config["job_location"]["name"], config["job_location"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in job location - %s",e)
                pass
            ####################### Job Posted Date #####################
            try:
                postedDay = postedday[indx]
            except Exception as e:
                self.logger.exception("exception in job Posted Date - %s",e)
                pass
            ####################### skills Required ######################
            try:
                skillsRequired = [i.text.rstrip(",") for i in jobs.find(config["job_skills"]["name"], config["job_skills"]["attrs"]).findAll("li")]
            except Exception as e:
                self.logger.exception("exception in job skills - %s",e)
                pass
            ####################### experience Required #################
            try:
                exprequired = jobs.find(config["job_experience"]["name"], config["job_experience"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in experience required - %s",e)
                pass


            # print("descriptiontitle ----------->",descriptionTitle)
            # print("descriptionId    ----------->",descriptionId)
            # print("descriptionurl   ----------->",descriptionurl)
            # print("descriptionlocation -------->",location)
            # print("descriptionemployer -------->",employerName)
            # print("descriptionemployerUrl ----->",morejobs)
            # print("descriptionPostedDate ------>",postedDay)
            # print("descriptionSummary --------->",summary)
            # print("descriptionSkills ---------->",skillsRequired)
            # print("descriptionExperience ------>",exprequired)

            descriptionDict = {}
            descriptionDict["_id"] = descriptionurl
            descriptionDict["jobDescriptionID"] = descriptionId
            descriptionDict["jobDescriptionURL"] = descriptionurl
            descriptionDict["jobTitle"] = descriptionTitle
            descriptionDict["jobLocation"] = location
            descriptionDict["jobSummary"] = summary
            descriptionDict["jobSalary"] = salary
            descriptionDict["jobPosted"] = postedDay
            descriptionDict["jobExperience"] = exprequired
            descriptionDict["jobSkills"] = skillsRequired
            descriptionDict["jobType"] = ""
            descriptionDict["employer"] = employerName
            descriptionDict["scrapTime"] = datetime.datetime.now()
            descriptionDict["postType"] = "general"
            descriptionDict["processFlag"] = "false"
            descriptionDict["source"] = "Shine"
            descriptionDict["moreJobsURL"] = ""
            descriptionDict["postedBy"] = recruiter
            descriptionArray.append(descriptionDict)

        return descriptionArray

class job_description_scraping():

    def __init__(self):
        self.logger = logging.getLogger("Shine job description scraping")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(filename=logfile)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def descriptionAutomation(self,database,browser = "phantomjs"):
        if browser=="firefox":
            self.driver = webdriver.Firefox()
        elif browser=="chrome":
            self.driver = webdriver.Chrome(config["chromepath"])
        else:
            self.driver = webdriver.PhantomJS(config["phantomjspath"])

        for joblink in database.find({"processFlag":"false"},
                                     {"_id":1}, no_cursor_timeout=True):

            self.jobDescUrl = "https://"+joblink["_id"]
            self.logger.info("job description url - %s",self.jobDescUrl)
            self.driver.get(self.jobDescUrl)
            time.sleep(random.randint(5,20))
            ########## calling function to extract the data #############
            FullDesc = self.descriptionExtraction(page=self.driver.page_source)
            if FullDesc:
                try:
                    self.logger.info("updating job description - %s",
                    database.update({"_id":joblink["_id"]},{"$set":{"full_desc":str(FullDesc),
                                                                    "descriptionPage":self.driver.page_source,
                                                                    "processFlag":"true",
                                                                    "descTime":datetime.datetime.now()}}))
                except Exception as e:
                    self.logger.fatal("exception in updating description - %s",e)
                    pass
        self.driver.close()

    def descriptionExtraction(self,page):
        Soup = BeautifulSoup(page,"lxml")
        try:
            Description = Soup.findAll(config["job_description"]["name"], config["job_description"]["attrs"])
            return "\n <br> \n".join([str(X) for X in Description])
        except Exception as e:
            self.logger.fatal("exception in finding job description - %s",e)
            pass

if __name__ == '__main__':
    from pymongo import MongoClient
    db = MongoClient("localhost",27017)["jd-scraper"]["shine.com"]
    classcall = job_link_scraping().linksAutomation(db,keyword="java developer",browser="firefox")

    # page = open("/home/anurag/Desktop/shine_page.html","r").read()
    # classcall = job_link_scraping().pagecount(page=page)

    # page = open("/home/anurag/Desktop/shine_description.html","r").read()

    # classcall2 = job_description_scraping().descriptionAutomation(db,browser="firefox")
    # print("classcall",classcall)