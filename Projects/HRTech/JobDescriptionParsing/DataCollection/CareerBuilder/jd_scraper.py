__author__="Anurag"
import datetime,time,random,logging,re
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from DataCollection.config import CareerBuilder_config
from DataCollection.config import logfile,logformat
config = CareerBuilder_config()
class jobs_links_scraping():

    def __init__(self):
        self.logger = logging.getLogger("CareerBuilder job links scraping")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(filename=logfile)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def linksAutomation(self,database,keyword,location=None,browser="phantomjs"):
        if browser == "firefox":
            self.driver = webdriver.Firefox()
            self.logger.info("browser_selected - firefox")
        elif browser == "chrome":
            self.driver = webdriver.Chrome(config["phantomjspath"])
            self.logger.info("browser_selected - chrome")
        else:
            self.driver = webdriver.PhantomJS(config["phantomjspath"])
            self.logger.info("browser_selected - phantomjs")

        baseurl = "http://www.careerbuilder.com/jobs-"
        searchurl = ""
        if location:
            searchurl = baseurl+keyword.replace(" ","-")+"-in-"+location
        else:
            searchurl = baseurl+keyword.replace(" ","-")
        self.logger.info("search url - %s",searchurl)
        self.driver.get(searchurl)

        pageSearch = self.pageCount(self.driver.page_source)
        self.logger.info("total job found - %s",pageSearch)

        for pagenumber in range(round(pageSearch/25)):
            nexturl = ""
            if pagenumber <2:
                nexturl = searchurl
            else:
                nexturl = searchurl+"?page_number="+str(pagenumber)
            time.sleep(random.randint(5,15))
            self.logger.info("currenturl - %s",nexturl)
            self.driver.get(nexturl)
            for jobsdata in self.linksExtraction(self.driver.page_source):
                try:
                    self.logger.info("parsed job - %s",jobsdata)
                    self.logger.info("inserting job links in database %s",database.insert(jobsdata))
                except Exception as e:
                    self.logger.error("exception in inserting job link in database - %s",e)
                    pass

    def pageCount(self,page):
        Soup= BeautifulSoup(page,"lxml")
        try:
            pagecount =int(re.findall(r'\d+', Soup.find(config["job_count"]["name"],config["job_count"]["attrs"]).text)[0])
            return pagecount
        except Exception as e:
            self.logger.fatal("exception in finding page_count - %s",e)
            return "error"

    def linksExtraction(self,page):
        Page = BeautifulSoup(page,"lxml")
        jobs = []
        if Page:
            for job in Page.find_all(config["job_section"]["name"],config["job_section"]["attrs"]):
                jobtitle = ""
                joblink = ""
                jobid = ""
                jobtype = ""
                jobsummary = ""
                jobemployer = ""
                jobemployer_url = ""
                joblocation= ""
                jobposted = ""
                morejobs = ""

                try:
                    jobtitle = job.find(config["job_title"]["name"],config["job_title"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job title - %s",e)
                    pass

                try:
                    joblink = "http://www.careerbuilder.com"+job.find(config["job_url"]["name"],config["job_url"]["attrs"]).find("a")["href"].strip()
                except Exception as e:
                    self.logger.exception("exception in job url - %s",e)
                    pass

                try:
                    jobid = job.find(config["job_title"]["name"],config["job_title"]["attrs"]).find("a")["data-job-did"].strip()
                except Exception as e:
                    self.logger.exception("exception in job id - %s",e)
                    pass

                try:
                    jobtype = job.find(config["job_type"]["name"],config["job_type"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job type - %s",e)
                    pass
                try:
                    jobsummary = job.find(config["job_summary"]["name"],config["job_summary"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job summary - %s",e)
                    pass

                try:
                    jobemployer = job.find(config["job_employer"]["name"],config["job_employer"]["attrs"]).find(config["job_employer_text"]["name"],config["job_employer_text"]["attrs"]).find("a").text.strip()
                except Exception as e:
                    try:
                        jobemployer = job.find(config["job_employer"]["name"],config["job_employer"]["attrs"]).find(config["job_employer_text"]["name"],config["job_employer_text"]["attrs"]).text.strip()
                    except Exception as e:
                        self.logger.exception("exception in job employer - %s",e)
                        pass
                    pass

                try:
                    jobemployer_url = "http://www.careerbuilder.com"+job.find(config["job_employer"]["name"],config["job_employer"]["attrs"]).find(config["job_employer_text"]["name"],config["job_employer_text"]["attrs"]).find("a")["href"].strip()
                except Exception as e:
                    self.logger.exception("exception in job employer url - %s",e)
                    pass

                try:
                    joblocation = job.find(config["job_location"]["name"],config["job_location"]["attrs"]).find(config["job_employer_text"]["name"],config["job_employer_text"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job location - %s",e)
                    pass

                try:
                    jobposted= job.find(config["job_posted"]["name"],config["job_posted"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job posted date - %s",e)
                    pass
                try:
                    morejobs = "http://www.careerbuilder.com"+job.find(config["job_morejobs"]["name"],config["job_morejobs"]["attrs"])["href"].strip()
                except Exception as e:
                    self.logger.exception("exception in more jobs - %s",e)
                    pass

                # print("jobtitle ----------->",jobtitle)
                # print("joblink  ----------->",joblink)
                # print("jobid    ----------->",jobid)
                # print("jobtype  ----------->",jobtype)
                # print("jobsummary---------->",jobsummary)
                # print("jobemployer--------->",jobemployer)
                # print("jobemployer_url----->",jobemployer_url)
                # print("joblocation    ----->",joblocation)
                # print("jobposted      ----->",jobposted)
                # print("morejobs_url   ----->",morejobs)

                if joblink:
                    descriptionDict = {}
                    descriptionDict["_id"] = joblink
                    descriptionDict["jobDescriptionID"] = jobid
                    descriptionDict["jobDescriptionURL"] = joblink
                    descriptionDict["jobTitle"] = jobtitle
                    descriptionDict["jobEmployer"] = jobemployer
                    descriptionDict["jobEmployer_url"] = jobemployer_url
                    descriptionDict["jobLocation"] = joblocation
                    descriptionDict["jobSummary"] = jobsummary
                    descriptionDict["jobSalary"] = ""
                    descriptionDict["jobPosted"] = jobposted
                    descriptionDict["moreJobs"] = morejobs
                    descriptionDict["postType"] = "general"
                    descriptionDict["jobType"] = jobtype
                    descriptionDict["source"] = "CareerBuilder"
                    descriptionDict["scrapTime"] = datetime.datetime.now()
                    descriptionDict["processFlag"] = "false"
                    descriptionDict["jobExperience"] = ""
                    jobs.append(descriptionDict)

        return jobs

class job_description_scraping():
    def __init__(self):
        self.logger = logging.getLogger("CareerBuilder job description scraping")
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

                    self.logger.info("updating job description - %s",database.update({"_id":joblink["_id"]},{"$set":{"full_desc":FullDesc,
                                                                    "descriptionPage":self.driver.page_source,
                                                                    "processFlag":"true",
                                                                    "descTime":datetime.datetime.now()}}))
                except Exception as e:
                    self.logger.exception("exception in updating job description - %s",e)
                    pass
        self.driver.close()

    def descriptionExtraction(self,page):
        Soup = BeautifulSoup(page,"lxml")
        Description = ""
        #############################################################################
        desc = []
        try:
            for des in Soup.find_all(config["job_description"]["name"],config["job_description"]["attrs"]):
                desc.append(str(des))
            Description = "<br>".join(desc)
        except Exception as e:
            self.logger.exception("exception in finding job description - %s",e)
            pass

        return Description

    def descriptionExtraction_int(self,page):
        Soup = BeautifulSoup(page,"lxml")
        description = ""
        title = ""
        employer=""
        dayposted=""
        industry=""
        tags=""
        categories=""
        metadata={}
        ####################### Full Job Description ######################
        try:
            desc = []
            for des in Soup.find_all(config["job_description"]["name"],config["job_description"]["attrs"]):
                desc.append(str(des))
            description = "<br>".join(desc)
        except Exception as e:
            self.logger.exception("exception in finding job description - %s",e)
            pass
        ####################### Job Title ################################
        try:
            title = Soup.find("div",{"class":"small-12 item"}).find("h1").text
        except Exception as e:
            self.logger.exception("exception in job description title - %s",e)
            pass
        ####################### Job Employer #############################
        try:
            employer = Soup.find("h2",{"id":"job-company-name"}).text
        except Exception as e:
            self.logger.exception("exception in job employer - %s",e)
            pass
        ####################### job posted date ##########################
        try:
            dayposted = Soup.find("h3",{"id":"job-begin-date"}).text
        except Exception as e:
            self.logger.exception("exception in job posted day - %s",e)
            pass
        ###################### job industry ##############################
        try:
            industry = Soup.find("div",{"id":"job-industry"}).text
        except Exception as e:
            self.logger.exception("exception in job industry - %s",e)
            pass
        ##################### job categories #############################
        try:
            categories = Soup.find("div",{"id":"job-categories"}).text
        except Exception as e:
            self.logger.exception("exception in job categories - %s",e)
            pass
        #################### job tags ####################################
        try:
            tags = Soup.find_all("div",{"class":"tag"})
        except Exception as e:
            self.logger.exception("exception in job tags - %s",e)
            pass

        print("description ->",description)
        print("title    ---->",title)
        print("employer ---->",employer)
        print("dayposted --->",dayposted)
        print("industry ---->",industry)
        print("categories -->",categories)
        print("tags -------->",tags)
        return description,metadata

    def description_integrated(self,url):
        pagesource=""
        try:
            pagesource = urlopen(url=url).read()
        except Exception as e:
            self.logger.exception("exception in loading url - %s",e)
            pass

        if pagesource:
            description,meta_data = self.descriptionExtraction_int(page=pagesource)
            print("description ------->",description)
            print("meta_data   ------->",meta_data)

if __name__ == '__main__':
    # classcall = job_description_scraping()
    classcall = jobs_links_scraping()
    from pymongo import MongoClient
    database = MongoClient("localhost",27017)["JDParser_scrap"]["CB_links"]
    functioncall = classcall.linksAutomation(database=database,keyword="python developer",browser="firefox")

    # page = open("/home/anurag/Desktop/cbdesc.html","r").read()
    # functioncall = job_description_scraping().descriptionAutomation(database=database)