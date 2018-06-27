__author__="Anurag"
from selenium import webdriver
from bs4 import BeautifulSoup
import time,datetime,re,random
from urllib.parse import urlencode
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox import firefox_profile
from DataCollection.config import FreshersWorld_config
config = FreshersWorld_config()
import logging
from DataCollection.config import logfile,logformat
class job_link_scraping():
    def __init__(self):
        self.logger = logging.getLogger("FreshersWorld job links scraping")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(filename=logfile)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def linksAutomation(self, database, keyword, location=None, browser="phantomjs"):

        if browser == "firefox":
            profile = webdriver.FirefoxProfile()
            profile.set_preference("geo.prompt.testing", True)
            profile.set_preference("geo.prompt.testing.allow", True)
            self.driver = webdriver.Firefox(firefox_profile=profile)

        elif browser == "chrome":
            self.driver = webdriver.Chrome(config["chromepath"])
        else:
            self.driver = webdriver.PhantomJS(config["phantomjspath"])

        self.baseurl = "https://www.freshersworld.com/jobs"
        self.driver.get(self.baseurl)
        self.driver.find_element_by_id("keyword").clear()
        self.driver.find_element_by_id("keyword").click()
        #
        time.sleep(5)
        self.driver.find_element_by_id("keyword").send_keys(keyword)
        time.sleep(5)
        if location:
            self.driver.find_element_by_id(id_="job_location").send_keys(location)
            time.sleep(5)

        self.driver.find_element_by_id("search_job_button").click()
        time.sleep(5)

        pageCount = self.pagecount(self.driver.page_source)
        self.logger.info("total jobs found - %s",pageCount)

        for pagenumber in range(0, round(pageCount/50)+1):
            if pagenumber ==0:
                trickurl = self.driver.current_url
            else:
                trickurl = self.driver.current_url+"?&limit=50&offset="+str(pagenumber*50)
            self.logger.info("search url - %s",trickurl)
            self.driver.get(trickurl)
            time.sleep(random.randint(5, 10))
            for job in self.linksScraper(self.driver.page_source):
                try:
                    self.logger.info("job link - %s",job)
                    self.logger.info("inserting job link in database - %s",database.insert(job))
                except Exception as e:
                    self.logger.exception("exception in inserting job links - %s ", e)
                    pass

        self.driver.close()

    def pagecount(self, page):
        Soup = BeautifulSoup(page, "lxml")
        print("Soup ",Soup)
        try:
            print("here sumthing",Soup.find(config["job_count"]["name"],config["job_count"]["attrs"]).text)
            jobs = int(Soup.find(config["job_count"]["name"],config["job_count"]["attrs"]).text.split("of")[-1].split()[0])
            print("jobs ",jobs)
            return jobs
        except Exception as e:
            self.logger.fatal("exception in finding jobs count - %s",e)
            return "Error"

    def linksScraper(self,page):
        Soup = BeautifulSoup(page,"lxml")
        descriptionArray = []

        for indx,jobs in enumerate(Soup.find_all(config["job_section"]["name"],config["job_section"]["attrs"])):
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
            qualifications=""
            applydate=""

            ####################### Title ###############################
            try:
                descriptionTitle = jobs.find(config["job_title"]["name"],config["job_title"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in job title - %s",e)
                pass

            ####################### Description Url #####################
            try:
                descriptionurl = jobs.find(config["job_url"]["name"],config["job_url"]["attrs"])["href"].strip()
            except Exception as e:
                self.logger.exception("exception in job url - %s",e)
                pass

            # ####################### Description ID ######################
            try:
                descriptionId = descriptionurl.split("-")[-1]
            except Exception as e:
                self.logger.exception("exception in job id - %s",e)
                pass

            # ####################### Job Summary #########################
            # try:
            #     summary = jobs.find("span",{"itemprop":"description"}).text.strip()
            # except Exception as e:
            #     self.logger.exception("exception in job summary - %s",e)
            #     pass

            ######################## Job Employer ########################
            try:
                employerName = jobs.find(config["job_employer"]["name"],config["job_employer"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in employer name - %s",e)
                pass

            ####################### Job Employer Url ####################
            # try:
            #     morejobs = jobs.find("span",{"class":"hidden-xs"}).find("a",{"class":"dice-btn-link"})["href"].strip()
            # except Exception as e:
            #     self.logger.exception("exception in employer url - %s",e)
            #     pass
            ######################## Job Location #######################
            try:
                location = jobs.find(config["job_location"]["name"],config["job_location"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in job location - %s",e)
                pass

            ####################### skills Required ######################
            try:
                skillsRequired = jobs.find(config["job_skills"]["name"],config["job_skills"]["attrs"])["title"]
            except Exception as e:
                self.logger.exception("exception in job skills - %s",e)
                pass

            ####################### experience Required #################
            # try:
            #     exprequired = jobs.find("span",{"itemprop":"experienceRequirements"}).text.strip()
            # except Exception as e:
            #     self.logger.exception("Exception in experience required - %s",e)
            #     pass

            ####################### Job Posted Date #####################
            try:
                postedDay = jobs.find(config["job_posted"]["name"],config["job_posted"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in job Posted Date - %s", e)
                pass

            ####################### qualifications ######################
            try:
                summary = jobs.find(config["job_summary"]["name"],config["job_summary"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in qualifications - %s",e)
                pass

            ###################### apply date ##########################
            try:
                applydate = jobs.find(config["job_applied"]["name"],config["job_applied"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in apply date - %s",e)
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
            # print("descriptionQualification --->",qualifications)
            # print("descriptionapplydate-     -->",applydate)
            # print("***************************************************************************************")

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
            descriptionDict["jobQualifications"] = qualifications
            descriptionDict["jobType"] = ""
            descriptionDict["employer"] = employerName
            descriptionDict["scrapTime"] = datetime.datetime.now()
            descriptionDict["postType"] = "general"
            descriptionDict["processFlag"] = "false"
            descriptionDict["source"] = "FreshersWorld"
            descriptionDict["moreJobsURL"] = ""
            descriptionDict["postedBy"] = recruiter
            descriptionDict["applyDate"] = applydate
            descriptionArray.append(descriptionDict)

        return descriptionArray

class job_description_scraping():

    def __init__(self):
        self.logger = logging.getLogger("FreshersWorld job description scraping")
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

            self.jobDescUrl = joblink["_id"]
            self.logger.info("job description url - %s",self.jobDescUrl)
            self.driver.get(self.jobDescUrl)
            time.sleep(random.randint(5,20))
            ########## calling function to extract the data #############
            FullDesc = self.descriptionExtraction(page=self.driver.page_source)
            if FullDesc:
                try:
                    self.logger.info("updating job description - %s",database.update({"_id":joblink["_id"]},{"$set":{"full_desc":str(FullDesc),
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
            Description = Soup.find(config["job_description"]["name"],config["job_description"]["attrs"])
            Description = str(Description)+"\n <br> \n"+" <br> ".join([str(i) for i in Soup.findAll(config["job_description_1"]["name"],config["job_description_1"]["attrs"])])
            Description = str(Description)+"\n <br> \n"+str(Soup.find(config["job_description_2"]["name"],config["job_description_2"]["attrs"]))
            return Description
        except Exception as e:
            self.logger.fatal("exception in job description finding - %s",e)
            pass


if __name__ == '__main__':
    from pymongo import MongoClient
    db = MongoClient("localhost",27017)["jd-scraper"]["freshersworld.com"]
    classcall = job_link_scraping().linksAutomation(db, keyword="java developer",browser="chrome") #,browser="firefox"

    # page = open("/home/anurag/Desktop/fw_home.html","r").read()
    # classcall = job_link_scraping().pagecount(page)

    # page = open("/home/anurag/Desktop/monster_description.html","r").read()

    # classcall2 = job_description_scraping().descriptionAutomation(database=db)
    # print("classcall",classcall)