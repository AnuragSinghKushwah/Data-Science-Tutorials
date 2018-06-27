from selenium import webdriver
from bs4 import BeautifulSoup
import time,datetime,re,random
from urllib.parse import urlencode
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox import firefox_profile
from DataCollection.config import Dice_config
config = Dice_config()
import logging
from DataCollection.config import logfile,logformat
class job_links_scraping():

    def __init__(self):
        self.logger = logging.getLogger("Dice job links scraping")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(filename=logfile)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def linksAutomation(self,database,keyword,location=None,browser="phantomjs"):
        profile = webdriver.FirefoxProfile()
        # profile.set_preference("geo.prompt.testing", True)
        # profile.set_preference("geo.prompt.testing.allow", True)
        # self.driver = webdriver.Firefox()
        # self.driver.delete_all_cookies()

        if browser == "firefox":
            self.driver = webdriver.Firefox(firefox_profile=profile)
        elif browser == "chrome":
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.PhantomJS(config["phantomjspath"])


        # chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--incognito")

        self.baseurl = "https://www.dice.com/jobs?"

        if location:
            self.urldict = {"q": keyword, "l": location}
        else:
            self.urldict = {"q": keyword}

        self.searchurl = self.baseurl+urlencode(self.urldict)
        self.logger.info("searchurl - %s",self.searchurl)
        self.driver.get(self.searchurl)
        pagecount = self.pagecount(self.driver.page_source)
        self.logger.info("total jobs found - %s",pagecount)

        for pagenumber in range(1,round(pagecount/120)+1):
            if pagenumber==1:
                trickurl = self.searchurl
            else:
                trickurl = self.baseurl.replace("?","/")+str(urlencode({"q": keyword, "l": location})).replace(" ","_").replace("=","-").replace("&","-").replace("+","_")+"-radius-30-startPage-"+str(pagenumber)+"-jobs-limit-120-jobs"
            time.sleep(random.randint(5, 10))
            self.driver.find_element_by_id("location").clear()
            self.driver.find_element_by_id("location").send_keys(Keys.ENTER)
            self.logger.info("search url - %s",trickurl)
            self.driver.get(trickurl)
            for job in self.linksScraper(self.driver.page_source):
                try:
                    self.logger.info("job link - %s",job)
                    self.logger.info("inserting job link in database - %s",database.insert(job))
                except Exception as e:
                    self.logger.exception("exception in inserting job links in database - %s",e)
                    pass
        self.driver.close()

    def linksScraper(self,page):
        Soup = BeautifulSoup(page,"lxml")
        descriptionArray = []
        for jobs in Soup.find_all(config["job_section"]["name"],config["job_section"]["attrs"]):
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
                descriptionTitle = jobs.find(config["job_title"]["name"],config["job_title"]["attrs"])["title"].strip()
            except Exception as e:
                self.logger.exception("exception in job title - %s",e)
                pass
            ####################### Description Url #####################
            try:
                descriptionurl = jobs.find(config["job_url"]["name"],config["job_url"]["attrs"])["href"].strip()
            except Exception as e:
                self.logger.exception("exception in job url - %s",e)
                pass
            ####################### Description ID ######################
            try:
                descriptionId = jobs.find(config["job_url"]["name"],config["job_url"]["attrs"])["value"].strip()
            except Exception as e:
                self.logger.exception("exception in job id - %s",e)
                pass
            ####################### Job Summary #########################
            try:
                summary = jobs.find(config["job_summary"]["name"],config["job_summary"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in job summary  - %s",e)
                pass
            ####################### Job Employer ########################
            try:
                employerName = jobs.find(config["job_employer"]["name"],config["job_employer"]["attrs"]).find(config["job_employer_text"]["name"],config["job_employer_text"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in employer name - %s",e)
                pass
            ######################## Job Location #######################
            try:
                location = jobs.find(config["job_location"]["name"],config["job_location"]["attrs"])["title"].strip()
            except Exception as e:
                self.logger.exception("exception in job location - %s",e)
                pass

            ####################### Job Employer Url ####################
            try:
                morejobs = jobs.find(config["job_employer"]["name"],config["job_employer"]["attrs"]).find(config["job_employer_text"]["name"],config["job_employer_text"]["attrs"])["href"].strip()
            except Exception as e:
                self.logger.exception("exception in employer url - %s", e)
                pass

            ####################### Job Posted Date #####################
            try:
                postedDay = jobs.find(config["job_posted"]["name"],config["job_posted"]["attrs"]).text.strip()
            except Exception as e:
                self.logger.exception("exception in job Posted Date - %s",e)
                pass

            # print("descriptiontitle ----------->",descriptionTitle)
            # print("descriptionId    ----------->",descriptionId)
            # print("descriptionurl   ----------->",descriptionurl)
            # print("descriptionlocation -------->",location)
            # print("descriptionemployer -------->",employerName)
            # print("descriptionemployerUrl ----->",morejobs)
            # print("descriptionPostedDate ------>",postedDay)
            # print("descriptionSummary --------->",summary)

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
            descriptionDict["source"] = "Dice"
            descriptionDict["jobType"] = ""
            descriptionDict["moreJobsURL"] = ""
            descriptionDict["postedBy"] = recruiter
            descriptionArray.append(descriptionDict)

        return descriptionArray

    def pagecount(self,page):
        Soup = BeautifulSoup(page,"lxml")
        try:
            totaljobs =int(re.findall(r'\d+',Soup.find(config["job_count"]["name"],config["job_count"]["attrs"]).text.split("of")[1])[0])
            return totaljobs
        except Exception as e:
            self.logger.fatal("exception in jobs count - %s",e)
            return "Error"

class job_description_scraping():

    def __init__(self):
        self.logger = logging.getLogger("Dice job description scraping")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(filename=logfile)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def descriptionAutomation(self,database,browser="phantomjs"):
        if browser == "firefox":
            self.driver = webdriver.Firefox()
        elif browser == "chrome":
            self.driver = webdriver.Chrome(config["chromepath"])
        else:
            self.driver = webdriver.PhantomJS(config["phantomjspath"])

        for joblink in database.find({"processFlag":"false"},
                                     {"_id":1}, no_cursor_timeout=True):

            self.jobDescUrl = joblink["_id"]
            self.logger.info("description url - %s",self.jobDescUrl)
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
                    self.logger.fatal('exception in updating job description - %s',e)
                    pass
        self.driver.close()

    def descriptionExtraction(self,page):
        Soup = BeautifulSoup(page,"lxml")
        try:
            Description = Soup.find(config["job_description"]["name"],config["job_description"]["attrs"])
            return Description
        except Exception as e:
            self.logger.exception("exception in job description - %s",e)
            pass


if __name__ == '__main__':
    classcall  = job_links_scraping()
    from pymongo import MongoClient
    database = MongoClient("localhost",27017)["JDParser2"]["Dice_links"]
    keyword = "Python Developer"
    location = "Dallas, TX"
    # page = open("/home/anurag/Desktop/dice_links.html", "r")
    functioncall=classcall.linksAutomation(database,keyword,location,browser="firefox")
    # functioncall = classcall.linksScraper(page)
    # functioncall=classcall.pagecount(page)