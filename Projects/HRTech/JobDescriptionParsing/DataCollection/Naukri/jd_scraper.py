__author="Anurag"

from DataCollection.config import Naukri_config
from bs4 import BeautifulSoup
from selenium import webdriver
import logging,datetime,time,random
config = Naukri_config()
from DataCollection.config import logfile,logformat
class job_link_scraping():

    def __init__(self):
        self.logger = logging.getLogger("Naukri job links scraping")
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
            self.driver = webdriver.Chrome(config['chromepath'])
        else:
            self.driver = webdriver.PhantomJS(config["phantomjspath"])
        try:
            if location:
                url = "https://www.naukri.com/" + str(keyword.lower() + "-jobs-in-" + location).replace(" ", "-").lower()
            else:
                url="https://www.naukri.com/" + str(keyword.lower() + "-jobs").replace(" ", "-").lower()
            self.logger.info("search url - %s",url)
            self.driver.get(url=url)
            time.sleep(5)
            pageCount = self.pageCount(pagesource=self.driver.page_source)
            self.logger.info("pages to search - %s",pageCount)
            for i in range(1, pageCount):
                if i == 1:
                    self.searchUrl = url
                else:
                    self.searchUrl = str(url + "-" + str(i))
                self.logger.info("search url - %s",self.searchUrl)
                self.driver.get(self.searchUrl)
                time.sleep(random.randint(5, 10))
                linksData = self.linksExtraction(pagesource=self.driver.page_source)
                if linksData:
                    for data in linksData:
                        data["searchKey"] = keyword
                        data["searchLocation"] = location
                        try:
                            self.logger.info("job links - %s",data)
                            self.logger.info("inserting job links into database - %s",database.insert(data))
                        except Exception as e:
                            self.logger.fatal("exception in inserting job Links - %s", e)
                            pass
        except Exception as e:
            self.logger.fatal("excecption in job Links Searching - %s", e)
            pass
        self.driver.close()
        self.driver.quit()

    def pageCount(self, pagesource):
        Page = BeautifulSoup(pagesource, "lxml")
        try:
            result = str(Page.find(config["job_count"]["name"], config["job_count"]["attrs"]).text).split(" of ")[-1]
            pageCount = round(int(result) / 50)
            self.logger.info("total jobs found - %s",result)
            return pageCount
        except Exception as e:
            self.logger.fatal("exception in finding total Job Links - %s", e)

    def linksExtraction(self, pagesource):

        descriptionArray = []
        Page = BeautifulSoup(pagesource, "lxml")

        ########### Finding Job Links ############
        try:
            for section in Page.find_all(config["job_section"]["name"], config["job_section"]["attrs"]):
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

                ############ Finding description Id ########
                try:
                    descriptionId = section["id"].strip()
                except Exception as e:
                    self.logger.exception("exception in Job Id - %s", e)
                    pass

                ############## Finding Jobs Url ############
                try:
                    descriptionurl1 = section.find(config["job_url"]["name"], config["job_url"]["attrs"])["href"].strip().split(descriptionId)[0]
                    descriptionurl = descriptionurl1 + descriptionId
                except Exception as e:
                    self.logger.exception("exception in Jobs Url - %s", e)
                    pass

                ############## finding Job title ###########
                try:
                    descriptionTitle = section.find(config["job_title"]["name"], config["job_title"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in Job Title - %s", e)
                    pass

                ########## Finding Hiring Organisation #########
                try:
                    employerName = section.find(config["job_employer"]["name"], config["job_employer"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in Job hiringOrganization - %s", e)
                    pass

                ########## finding Exp Required ##############
                try:
                    exprequired = section.find(config["job_experience"]["name"], config["job_experience"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in Job Exp Required - %s", e)
                    pass

                ########## Finding Job Location ##############
                try:
                    location = section.find(config["job_location"]["name"], config["job_location"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job Location - %s", e)
                    pass

                ######### Finding Job Skills #################
                try:
                    skillsRequired = section.find(config["job_skills"]["name"], config["job_skills"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job skills - %s", e)
                    pass

                ######### Finding Job Description ############
                try:
                    summary = section.find(config["job_summary"]["name"], config["job_summary"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job summary - %s", e)
                    pass

                ######## Finding Jobs Salary #################
                try:
                    salary = section.find(config["job_salary"]["name"], config["job_salary"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job salary - %s", e)
                    pass

                ######## Finding Posted By ###################
                try:
                    recruiter = section.find(config["job_recruiter"]["name"], config["job_recruiter"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in  job Recruiter - %s", e)
                    pass

                ######## Finding Job Posted Date #############
                try:
                    postedDay = section.find(config["job_posted"]["name"], config["job_posted"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job Posted Date - %s", e)
                    pass
                # print("********************************************")
                # print("joburl -------------------->", descriptionurl)
                # print("descriptionId ------------->", descriptionId)
                # print("jobtitle ------------------>", descriptionTitle)
                # print("hiringOrganization--------->", employerName)
                # print("joblocation---------------->", location)
                # print("skillsRequired------------->", skillsRequired)
                # print("jobDescription  ----------->", summary)
                # print("salary--------------------->", salary)
                # print("recruiter------------------>", recruiter)
                # print("jobPosted------------------>", postedDay)
                # print("********************************************")
                descriptionDict = {}
                descriptionDict["_id"] = descriptionurl
                descriptionDict["jobDescriptionID"] = descriptionId
                descriptionDict["jobDescriptionURL"] = descriptionurl
                descriptionDict["jobTitle"] = descriptionTitle
                descriptionDict["employer"] = employerName
                descriptionDict["jobLocation"] = location
                descriptionDict["jobSummary"] = summary
                descriptionDict["jobSalary"] = salary
                descriptionDict["jobPosted"] = postedDay
                descriptionDict["jobExperience"] = exprequired
                descriptionDict["scrapTime"] = datetime.datetime.now()
                descriptionDict["postType"] = "general"
                descriptionDict["processFlag"] = "false"
                descriptionDict["source"] = "Naukri"
                descriptionDict["jobType"] = ""
                descriptionDict["moreJobsURL"] = ""
                descriptionDict["postedBy"] = recruiter
                descriptionArray.append(descriptionDict)

        except Exception as e:
            self.logger.fatal("exception in Job Links Extraction - %s", e)

        return descriptionArray

class job_description_scraping():

    def __init__(self):
        self.logger = logging.getLogger("Naukri job description scraping")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(filename=logfile)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def descriptionAutomation(self,database,browser="phantomjs"):
        if browser=="firefox":
            self.driver = webdriver.Firefox()
        elif browser=="chrome":
            self.driver = webdriver.Chrome(config["chromepath"])
        else:
            self.driver = webdriver.PhantomJS(config["phantomjspath"])


        for joblink in database.jobDescriptions.find({"processFlag": "false"}, {"_id": 1},
                                                     no_cursor_timeout=True).limit(1000):
            self.jobDescUrl = joblink["_id"]
            self.logger.info("job description url - %s",self.jobDescUrl)
            self.driver.get(self.jobDescUrl)
            time.sleep(random.randint(5, 20))
            self.currenturl = self.driver.current_url
            self.logger.info("current url - %s",self.currenturl)

            if "www.naukri.com" in self.currenturl:
                self.pagesource = self.driver.page_source
                ########## calling function to extract the data #############
                FullDesc = self.descriptionExtraction(page=self.pagesource)
                if FullDesc:
                    try:
                        self.logger.info("updating job description - %s",
                        database.update({"_id": joblink["_id"]}, {"$set": {"full_desc": FullDesc,
                                                                                           "processFlag": "true"}}))
                    except Exception as e:
                        self.logger.fatal("exception in updating job description - %s",e)
                        pass
            else:
                self.logger.fatal("the page has been re-directed")
                self.logger.info("updating job description - %s",
                database.update({"_id": joblink["_id"]}, {"$set": {"processFlag": "reDirected"}}))

    def descriptionExtraction(self, page):
        Page = BeautifulSoup(page, "lxml")
        try:
            description = Page.find(config["job_description"]["name"], config["job_description"]["attrs"])
            return description.text
        except Exception as e:
            self.logger.fatal("exception in job description - %s",e)
            return "error"

if __name__ == '__main__':
    from pymongo import MongoClient
    db = MongoClient("localhost",27017)["jd-scraper"]["naukri.com"]
    classcall = job_link_scraping().linksAutomation(db,keyword="java developer",location="",browser="firefox")

    # page = open("/home/anurag/Desktop/wisdomjobs_links.html","r").read()
    # classcall = job_link_scraping().linksScraper(page=page)

    # page = open("/home/anurag/Desktop/shine_description.html","r").read()

    # classcall2 = job_description_scraping().descriptionAutomation(db,browser="firefox")
    # print("classcall",classcall)