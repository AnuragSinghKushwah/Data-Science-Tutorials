__author__="anurag"
from selenium import webdriver
import datetime
from DataCollection.config import Indeed_config
config = Indeed_config()
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import logging,time,random

from DataCollection.config import logfile,logformat
class job_links_scraping():

    def __init__(self):
        self.baseurl = config["baseurl"]
        self.logger = logging.getLogger("Indeed job links scraping")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(filename=logfile)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(logformat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def linksAutomation(self,database, keyword, location,browser="phantomjs"):

        if browser == "firefox":
            self.driver = webdriver.Firefox()
        elif browser == "chrome":
            self.driver = webdriver.Chrome(config["chromepath"])
        else:
            self.driver = webdriver.PhantomJS(config["phantomjspath"])

        self.urldict = {"q": keyword, "l": location, "sort": "date", "radius": "100"}
        self.searchurl = self.baseurl + urlencode(self.urldict)
        self.logger.info("search url - %s",self.searchurl)
        self.driver.get(self.searchurl)
        time.sleep(5)
        response = self.driver.page_source
        ########## calling function to find pages to search #######
        pageCount = self.pageSearch(pagesource=response)
        self.logger.info("total jobs found - %s",pageCount)
        if pageCount>=1:
            if pageCount >100:
                pageCount = 100
            for page in range(0,pageCount):
                try:
                    ############### making query #################
                    if page == 0:
                        self.urldict = {"q":keyword,"l":location,"sort":"date","radius":"100"}
                    else:
                        self.urldict = {"q":keyword,"l":location,"sort":"date","radius":"100","start":str(page*10)}

                    self.searchurl = self.baseurl+urlencode(self.urldict)
                    self.logger.info("search url - %s",self.searchurl)
                    ###### Querying using selenium webdriver #########

                    self.driver.get(self.searchurl)
                    time.sleep(random.randint(5, 20))
                    response = self.driver.page_source

                    ###### calling function to extract the data #######

                    linkdata = self.linksExtract(page=response)
                    if linkdata != "fail":
                        for data in linkdata:
                            data["searchKey"] = keyword
                            data["searchLocation"] = location
                            try:
                                self.logger.info("jobs url - %s",data)
                                self.logger.info("inserting job links - %s",database.insert(data))
                            except Exception as e:
                                self.logger.fatal("Inserting Job Descriptions Links - %s",e)
                                pass
                    else:
                        self.logger.fatal("no result found on this page")

                except Exception as e:
                    self.logger.fatal("Exception in Jobs Link Finding - %s",e)
                    pass

    def linksExtract(self,page):

        ############## Creating Beautiful Soup Element ###########
        Soup = BeautifulSoup(page,"lxml")
        descriptionsArray = []
        searchCount = ""

        ############## Finding Sections ##########################
        try:
            searchCount = Soup.find(config["job_count"]["name"], config["job_count"]["attrs"]).text.split("of")[1].strip()
        except Exception as e:
            self.logger.fatal("job links searchCount - %s",str(e))
            pass

        self.logger.info("total job links found - %s", searchCount)
        if searchCount != "":
            ############## finding General Job Descriptions ##################

            for section in Soup.find_all(config["job_section"]["name"], config["job_section"]["attrs"]):
                descriptionHead = ""
                descriptionId = ""
                employerName =""
                descriptionurl = ""
                location = ""
                salary = ""
                postedDay = ""
                morejobsurl = ""
                summary = ""
                descriptionTitle = ""
                descriptionDict = {}
                ############ Finding Job Description Heading ######################
                try:
                    descriptionHead = section.find(config["job_title_head"]["name"], config["job_title_head"]["attrs"])
                    descriptionId = descriptionHead["id"]
                except Exception as e:
                    self.logger.exception("exception in Title Heading - %s",e)
                    pass

                ########### Finding Job Description Title #########################
                try:
                    descriptionTitle = descriptionHead.find(config["job_title"]["name"], config["job_title"]["attrs"])["title"]
                except Exception as e:
                    self.logger.exception("exception in job title - %s",e)
                    pass

                ########### Finding Job Description URl ###########################
                try:
                    descriptionurl = "http://www.indeed.co.in"+descriptionHead.find(config["job_title"]["name"], config["job_title"]["attrs"])["href"]
                except Exception as e:
                    self.logger.exception("exception in job url - %s",e)
                    pass

                ########### Finding Hiring Organisation Name ######################
                try:
                    employerName = section.find(config["job_employer"]["name"], config["job_employer"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in  employer name - %s",e)
                    pass

                ########### Finding Job Location ##################################
                try:
                    location = section.find(config["job_location"]["name"], config["job_location"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in  job location - %s",e)
                    pass

                ########## Finding Salary ########################################
                try:
                    stipend2 = section.find(config["job_salary"]["name"], config["job_salary"]["attrs"])
                    salary= stipend2.find(config["job_salary_tag"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job salary - %s",e)
                    pass

                ########## Finding Job Summary ###################################
                try:
                    summary = section.find(config["job_summary"]["name"], config["job_summary"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in job summary- %s",e)
                    pass

                ########## Finding Posted Date ###################################
                try:
                    postedDay = section.find(config["job_posted"]["name"], config["job_posted"]["attrs"]).text.strip()
                except Exception as e:
                    self.logger.exception("exception in  job date posted - %s",e)
                    pass

                ########## Finding More Jobs from Employer #######################
                try:
                    morejobsurl = "http://www.indeed.co.in"+section.find(config["job_morejobs"]["name"], config["job_morejobs"]["attrs"]).find_all("a")[0]["href"]
                except Exception as e:
                    self.logger.exception("exception in more jobs url - %s",e)
                    pass
                ######### Checking if its Indeed Job or not #######################
                indeedJob = False
                try:
                    indjob = section.find(config["isindeed"]["name"], config["isindeed"]["attrs"]).text
                    if indjob:
                        indeedJob = True
                except Exception as e:
                    indeedJob = False
                    self.logger.exception("excpetion in indeed flag - %s",e)
                    pass
                # print("******************************************************************")
                # print("description_ID ---->",descriptionId)
                # print("description_Url --->",descriptionurl)
                # print("description_Title ->",descriptionTitle)
                # print("employerName ------>",employerName)
                # print("Job Location------->",location)
                # print("stipend ----------->",salary)
                # print("summary ----------->",summary)
                # print("postedDay --------->",postedDay)
                # print("IndeedJob --------->",indeedJob)
                # print("more jobs from employer ---->",morejobsurl)
                descriptionDict["_id"] = descriptionurl
                descriptionDict["jobDescriptionID"] = descriptionId
                descriptionDict["jobDescriptionURL"] = descriptionurl
                descriptionDict["jobTitle"] = descriptionTitle
                descriptionDict["employer"] = employerName
                descriptionDict["jobLocation"] = location
                descriptionDict["jobSummary"] = summary
                descriptionDict["jobSalary"] = salary
                descriptionDict["jobPosted"] = postedDay
                descriptionDict["moreJobsURL"] = morejobsurl
                descriptionDict["postType"] = "general"
                descriptionDict["jobType"] = ""
                descriptionDict["scrapTime"] = datetime.datetime.now()
                descriptionDict["processFlag"] = "false"
                descriptionDict["jobExperience"] = ""
                if indeedJob:
                    descriptionDict["indeedJob"] = "true"
                else:
                    descriptionDict["indeedJob"] = "false"
                descriptionsArray.append(descriptionDict)
            # # ################## finding Sponsored Jobs Description ######################
            # parentTag = Soup.find_all(spn_mainDiv["name"],spn_mainDiv["attr"])
            # for i in parentTag:
            #     sponsoredJobs = i.parent
            #
            #     sponsoredTitle = ""
            #     sponsoredURL = ""
            #     sponsoredOrganisation = ""
            #     sponsoredRatings = ""
            #     sponsoredLocation = ""
            #     sponsoredOrganisationUrl = ""
            #     sponsoredSummary = ""
            #     sponsoredDatePosted = ""
            #
            #     ################ Finding Sponsered Job Title ###########################
            #     try:
            #         sponsoredTitle = sponsoredJobs.find(spn_LinkTitle["name"], spn_LinkTitle["attr"]).text
            #     except Exception as e:
            #         self.logger.warning("Job Description Sponsored Jobs title - %s ",e)
            #         pass
            #
            #     ################ Finding Sponsered Job Description URL ##################
            #     try:
            #         sponsoredURL = "http://www.indeed.co.in"+sponsoredJobs.find(spn_LinkTitle["name"],spn_LinkTitle["attr"])["href"]
            #     except Exception as e:
            #         self.logger.warning("Job Description Sponsored Job Url - %s",e)
            #         pass
            #
            #     ################ Finding Sponsored Hiring Orgnaisation ##################
            #     try:
            #         sponsoredOrganisation = sponsoredJobs.find(spn_LinkEmp["name"], spn_LinkEmp["attr"]).text.strip()
            #     except Exception as e:
            #         self.logger.warning("Job Description Sponsored Organization - %s", e)
            #         pass
            #
            #     ################ Finding Sponsored Hiring Orgnaisation Url##################
            #     try:
            #         sponsoredOrganisationUrl = "http://www.indeed.co.in"+sponsoredJobs.find(spn_LinkEmp["name"], spn_LinkEmp["attr"]).find("a")["href"].strip()
            #     except Exception as e:
            #         self.logger.warning("Job Description Sponsored Organization Url - %s", e)
            #         pass
            #
            #     ################ Finding Employer Ratings ###############################
            #     try:
            #         sponsoredRatings = sponsoredJobs.find(spn_LinkRating["name"], spn_LinkRating["attr"]).text.strip()
            #     except Exception as e:
            #         self.logger.warning("Job Description Sponsored Ratings - %s", e)
            #         pass
            #
            #     ############### Finding Job Location ####################################
            #     try:
            #         sponsoredLocation = sponsoredJobs.find(spn_LinkLoc["name"],spn_LinkLoc["attr"]).text.strip()
            #     except Exception as e:
            #         self.logger.warning("Job Description Spnosored Location - %s", e)
            #         pass
            #
            #     ############### Finding Job Description Summary #########################
            #     try:
            #         sponsoredSummary = sponsoredJobs.find(spn_LinkSumm["name"],spn_LinkSumm["attr"]).text.strip()
            #     except Exception as e:
            #         self.logger.warning("Job Description Sponsored Summary - %s", e)
            #         pass
            #     ############## Finding Date Posted #######################################
            #     try:
            #         sponsoredDatePosted = sponsoredJobs.find(spn_LinkDate["name"],spn_LinkDate["attr"]).text.strip()
            #     except Exception as e:
            #         self.logger.warning("Job Description Sponsored Date Posted - %s", e)
            #         pass
            #
            #     print("**************************************************************")
            #     print("sponsored Jobs tiltes ------->", sponsoredTitle)
            #     print("sponsoredCompany --->", sponsoredOrganisation)
            #     print("sponsoredCompanyUrl --->", sponsoredOrganisationUrl)
            #     print("sponsored Jobs urls ------->", sponsoredURL)
            #     print("sponsoredRatings --->", sponsoredRatings)
            #     print("sponsoredLocation -->", sponsoredLocation)
            #     print("sponsoredSummary -->", sponsoredSummary)
            #     print("sponsoredDatePosted -->", sponsoredDatePosted)
            #     # print("sponsoredDatePosted -->", sponsoredDatePosted)
            #     ############### Formatting the fields #############################
            #     descriptionDict={}
            #     descriptionDict["_id"] = sponsoredURL
            #     descriptionDict["jobDescriptionID"] = ""
            #     descriptionDict["jobDescriptionURL"] = sponsoredURL
            #     descriptionDict["jobTitle"] = sponsoredTitle
            #     descriptionDict["employer"] = sponsoredOrganisation
            #     descriptionDict["employerUrl"] = sponsoredOrganisationUrl
            #     descriptionDict["jobLocation"] = sponsoredLocation
            #     descriptionDict["jobSummary"] = sponsoredSummary
            #     descriptionDict["jobPosted"] = sponsoredDatePosted
            #     descriptionDict["jobSalary"] = ""
            #     descriptionDict["moreJobsURL"] = ""
            #     descriptionDict["postType"] = "sponsored"
            #     descriptionDict["jobType"] = ""
            #     descriptionDict["source"] = "Indeed"
            #     descriptionDict["scrapTime"] = datetime.datetime.now()
            #     descriptionDict["processFlag"] = "false"
            #     descriptionDict["indeedJob"] = "false"
            #     descriptionsArray.append(descriptionDict)

            return descriptionsArray
        else:
            self.logger.fatal("No result found for this category")
            return "fail"

    def pageSearch(self,pagesource):

        Soup = BeautifulSoup(pagesource, "lxml")
        ############## Finding Sections ##########################
        try:
            searchCount = Soup.find(config["job_count"]["name"], config["job_count"]["attrs"]).text.split("of")[1].strip().replace(",","")
            if searchCount:
                if int(searchCount)>0 and int(searchCount)<10:
                    pageSearch = 1
                    return pageSearch

                elif int(searchCount)> 10:
                    pageSearch = round(int(searchCount)/10)-1
                    return pageSearch

                else:
                    return 0
        except Exception as e:
            self.logger.fatal("job links searchCount - %s", str(e))
            return 0

class job_description_scraping():

    def __init__(self):
        self.baseurl = config["baseurl"]
        self.logger = logging.getLogger("Indeed job description scraping")
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

        for joblink in database.jobDescriptions.find({"processFlag":"false","indeedJob":"true"},
                                                     {"_id":1},no_cursor_timeout=True).limit(1000):
            self.jobDescUrl = joblink["_id"]
            self.logger.info("search url - %s",self.jobDescUrl)
            self.driver.get(self.jobDescUrl)
            time.sleep(random.randint(5,20))
            self.currenturl = self.driver.current_url
            self.logger.info("current url - %s",self.currenturl)
            if "www.indeed.co.in" in self.currenturl:
                self.pagesource = self.driver.page_source
                ########## calling function to extract the data #############
                FullDesc = self.descriptionExtraction(page=self.pagesource)
                if FullDesc:
                    try:
                        self.logger.info("updating job description - %s",
                        database.update({"_id":joblink["_id"]},{"$set":{"full_desc":FullDesc,
                                                                        "processFlag":"true",
                                                                        "source":"Indeed"}}))
                    except Exception as e:
                        self.logger.exception("exception in updating job description - %s",e)
                        pass
            else:
                self.logger.fatal("the page has been re-directed - %s",
                database.update({"_id": joblink["_id"]}, {"$set": {"processFlag": "reDirected",
                                                                   "source":"Indeed"}}))
                pass


    def descriptionExtraction(self,page):
        Soup = BeautifulSoup(page,"lxml")
        JobTitle = ""
        Company = ""
        Location = ""
        Summary = ""
        PostedDate = ""
        ############## Finding Job Title ####################
        try:
            JobTitle = Soup.find(config["job_description_title"]["name"], config["job_description_title"]["attrs"]).text.strip()
        except Exception as e:
            self.logger.exception("exception in Job Description Title - %s",e)
            pass
        ############## Finding Company Name #################
        try:
            Company = Soup.find(config["job_description_employer"]["name"], config["job_description_employer"]["attrs"]).text.strip()
        except Exception as e:
            self.logger.exception("exception in Job Description Employer Name - %s",e)
            pass
        ############## Finding Job Location #################
        try:
            Location = Soup.find(config["job_description_location"]["name"], config["job_description_location"]["attrs"]).text.strip()
        except Exception as e:
            self.logger.exception("exception in Job Description Location - %s",e)
            pass
        ############# Finding Job Summary ###################
        try:
            Summary = Soup.find(config["job_description"]["name"], config["job_description"]["attrs"]).text.strip()
        except Exception as e:
            self.logger.exception("exception in Job Description Summary - %s",e)
            pass
        try:
            PostedDate = Soup.find(config["job_description_date"]["name"], config["job_description_date"]["attrs"]).text.strip()
        except Exception as e:
            self.logger.exception("exception in Job Description PostedDate - %s",e)
            pass
        DescriptionDict = {}
        DescriptionDict["JobTitle"] = JobTitle
        DescriptionDict["Company"] = Company
        DescriptionDict["Location"] = Location
        DescriptionDict["JobDescription"] = Summary
        DescriptionDict["PostedDate"] = PostedDate

        return DescriptionDict

if __name__ == '__main__':
    classcall  = job_links_scraping()
    classcall2 = job_description_scraping()
    from pymongo import MongoClient
    database = MongoClient("localhost",27017)["JDParser2"]["Dice_links"]
    keyword = "customer support representative"
    location = "haridwar"
    # page = open("/home/anurag/Desktop/dice_links.html", "r")
    functioncall=classcall.linksAutomation(database,keyword,location,browser="firefox")
    # functioncall = classcall2.descriptionAutomation(database,browser="firefox")
    # functioncall = classcall.linksExtract(page)
    # functioncall=classcall.pagecount(page)