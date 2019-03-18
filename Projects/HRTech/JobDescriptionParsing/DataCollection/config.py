__author__="Anurag"
phantomjspath = "/home/anurag/node_modules/phantomjs/bin/phantomjs"
chromepath = "/usr/lib/chromium-browser/chromedriver"
logfile = "/home/anurag/Desktop/datascraping.log"
logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def CareerBuilder_config():
    elements = {}
    elements["job_count"] = {"name" : "div", "attrs" : {"class" : "count"}}
    elements["job_section"] = {"name" : "div", "attrs" : {"class" : "job-row"}}
    elements["job_title"] = {"name" : "h2", "attrs" : {"class" : "job-title"}}
    elements["job_url"] = {"name" : "h2", "attrs" : {"class" : "job-title"}}
    elements["job_type"] = {"name" : "h4", "attrs" : {"class" : "job-text employment-info"}}
    elements["job_summary"] = {"name" : "div", "attrs" : {"class" : "job-description show-for-medium-up"}}
    elements["job_employer"] = {"name" : "div", "attrs" : {"class" : "columns large-2 medium-3 small-12"}}
    elements["job_employer_text"] = {"name" : "h4", "attrs" : {"class" : "job-text"}}
    elements["job_location"] = {"name" : "div", "attrs" : {"class" : "columns end large-2 medium-3 small-12"}}
    elements["job_posted"] = {"name" : "div", "attrs" : {"class": "show-for-medium-up"}}
    elements["job_morejobs"] = {"name" : "h2", "attrs" : {"class": "job-title hide-for-medium-up"}}
    elements["job_description"] = {"name" : "div", "attrs" : {"class": "description"}}
    elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath
    return elements

def Dice_config():
    elements = {}
    elements["job_count"] = {"name": "span", "attrs": {"id": "posiCountMobileId"}}
    elements["job_section"] = {"name": "div", "attrs": {"class": "complete-serp-result-div"}}
    elements["job_title"] = {"name": "a", "attrs": {"class": "dice-btn-link loggedInVisited easy-apply"}}
    elements["job_url"] = {"name": "a", "attrs": {"class": "dice-btn-link loggedInVisited easy-apply"}}
    elements["job_type"] = {"name": "h4", "attrs": {"class": "job-text employment-info"}}
    elements["job_summary"] = {"name": "div", "attrs": {"class": "shortdesc"}}
    elements["job_employer"] = {"name": "span", "attrs": {"class": "hidden-xs"}}
    elements["job_employer_text"] = {"name": "a", "attrs": {"class": "dice-btn-link"}}
    elements["job_location"] = {"name": "li", "attrs": {"class": "location col-sm-3 col-xs-12 col-md-2 col-lg-3 margin-top-3 text-ellipsis"}}
    elements["job_posted"] = {"name": "li", "attrs": {"class": "posted col-xs-12 col-sm-2 col-md-2 col-lg-2 margin-top-3 text-wrap-padding"}}
    elements["job_morejobs"] = {"name": "a", "attrs": {"rel": "nofollow"}}
    elements["job_description"] = {"name": "div", "attrs": {"id": "jobdescSec"}}
    elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath

    return elements

def FreshersWorld_config():
    elements = {}
    elements["job_count"] = {"name": "span", "attrs": {"id": "total_job"}}
    # elements["job_count"] = {"name": "span", "attrs": {"id": "pull-left text-info"}}

    # "pull-left text-info"
    elements["job_section"] = {"name": "tr", "attrs": {"itemtype": "http://schema.org/JobPosting"}}
    elements["job_title"] = {"name": "span", "attrs": {"class": "position"}}
    elements["job_url"] = {"name": "a", "attrs": {"itemprop": "url"}}
    elements["job_employer"] = {"name": "a", "attrs": {"itemprop": "url"}}
    elements["job_location"] = {"name": "span", "attrs": {"itemprop": "jobLocation"}}
    elements["job_skills"] = {"name": "a", "attrs": {"class": "mouse_hover"}}
    elements["job_posted"] = {"name": "span", "attrs": {"class": "post_date"}}
    elements["job_applied"] = {"name": "td", "attrs": {"itemprop": "datePosted"}}
    elements["job_summary"] = {"name": "td", "attrs": {"itemprop": "qualifications"}}
    elements["job_description"] = {"name": "div", "attrs": {"class": "detail-job-details-second-level"}}
    elements["job_description_1"] = {"name": "p", "attrs": {"class": "desc-font"}}
    elements["job_description_2"] = {"name": "div", "attrs": {"class": "detail-container-profile-sub-level"}}
    elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath
    # elements["job_type"] = {"name": "h4", "attrs": {"class": "job-text employment-info"}}
    # elements["job_employer_text"] = {"name": "a", "attrs": {"class": "dice-btn-link"}}
    # elements["job_morejobs"] = {"name": "a", "attrs": {"class": "company-collapse-link"}}
    return elements

def Indeed_config():
    elements = {}
    elements["baseurl"]="http://www.indeed.co.in/jobs?"
    elements["job_count"] = {"name": "div", "attrs": {"id": "searchCount"}}
    elements["job_section"] = {"name": "div", "attrs": {"data-tn-component": "organicJob"}}
    elements["job_title_head"] ={"name":"h2","attrs":{"class":"jobtitle"}}
    elements["job_title"] =  {"name":"a","attrs":{"class":"turnstileLink"}}
    elements["job_url"] = {"name":"a","attrs":{"class":"turnstileLink"}}
    elements["job_employer"] = {"name":"span","attrs":{"class":"company"}}
    elements["job_location"] = {"name":"span","attrs":{"class":"location"}}
    elements["job_salary"] = {"name":"span","attrs":{"class":"salary no-wrap"}}
    
    elements["job_summary"] = {"name":"span","attrs":{"class":"summary"}}
    elements["job_posted"] = {"name":"span","attrs":{"class":"date"}}
    elements["job_morejobs"] = {"name":"span","attrs":{"class":"mat"}}
    elements["isindeed"]={"name":"span","attrs":{"class":"iaLabel"}}
    elements["job_description"] = {"name":"span","attrs":{"class":"summary"}}
    elements["job_description_title"] = {"name":"b","attrs":{"class":"jobtitle"}}
    elements["job_description_employer"] = {"name":"span","attrs":{"class":"company"}}
    elements["job_description_location"] = {"name":"span","attrs":{"class":"location"}}
    elements["job_description_date"] = {"name":"span","attrs":{"class":"date"}}
    elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath

    # elements["job_type"] = {"name": "h4", "attrs": {"class": "job-text employment-info"}}
    # elements["job_employer_text"] = {"name": "a", "attrs": {"class": "dice-btn-link"}}
    return elements

def Monster_config():

    elements = {}
    elements["job_count"] = {"name": "div", "attrs": {"class": "count pull-left"}}
    elements["job_section"] = {"name": "div", "attrs": {"class": "jobwrap "}}
    elements["job_title"] = {"name": "span", "attrs": {"itemprop": "title"}}
    elements["job_url"] = {"name": "a", "attrs": {"class": "joblnk"}}
    elements["job_summary"] = {"name": "span", "attrs": {"itemprop": "description"}}
    elements["job_employer"] = {"name": "span", "attrs": {"itemprop": "hiringOrganization"}}
    elements["job_location"] = {"name": "span", "attrs": {"itemprop": "jobLocation"}}
    elements["job_skills"] = {"name": "span", "attrs": {"itemprop": "skills"}}
    elements["job_experience"] = {"name": "span", "attrs": {"itemprop": "experienceRequirements"}}
    elements["job_posted"] = {"name": "div", "attrs": {"itemprop": "datePosted"}}
    elements["job_description"] = {"name": "div", "attrs": {"class": "job_description "}}
    elements["job_description_skills"] = {"name": "a", "attrs": {"class": "keylink lft"}}
    elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath

    # elements["job_type"] = {"name": "h4", "attrs": {"class": "job-text employment-info"}}
    # elements["job_employer_text"] = {"name": "a", "attrs": {"class": "dice-btn-link"}}
    # elements["job_morejobs"] = {"name": "a", "attrs": {"class": "company-collapse-link"}}

    return elements

def Naukri_config():
    elements = {}
    elements["job_count"] = {"span": "div", "attrs": {"class": "cnt"}}
    elements["job_section"] = {"name": "div", "attrs": {"type": "tuple"}}
    elements["job_url"] = {"name": "a", "attrs": {"class": "content"}}
    elements["job_title"] = {"name": "span", "attrs": {"itemprop": "title"}}
    elements["job_summary"] = {"name": "span", "attrs": {"itemprop": "description"}}
    elements["job_employer"] = {"name": "span", "attrs": {"itemprop": "hiringOrganization"}}
    elements["job_location"] = {"name": "span", "attrs": {"itemprop": "jobLocation"}}
    elements["job_skills"] = {"name": "span", "attrs": {"itemprop": "skills"}}
    elements["job_salary"] = {"name": "span", "attrs": {"itemprop": "baseSalary"}}
    elements["job_experience"] = {"name": "span", "attrs": {"itemprop": "experienceRequirements"}}
    elements["job_recruiter"] = {"name": "a", "attrs": {"class": "rec_name"}}
    elements["job_posted"] = {"name": "span", "attrs": {"class": "date"}}
    elements["job_description"] = {"name": "div", "attrs": {"class": "JD"}}
    elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath

    return elements

def Shine_config():
    elements = {}
    elements["job_count"] = {"name": "div", "attrs": {"class": "num_key"}}
    elements["job_section"] = {"name": "div", "attrs": {"class": "search_listingleft search_listingleft_100"}}
    elements["job_title"] = {"name": "strong", "attrs": {"itemprop": "title"}}
    elements["job_url"] = {"name": "a", "attrs": {"class": "cls_searchresult_a"}}
    elements["job_summary"] = {"name": "b", "attrs": {"class": "srcresult"}}
    elements["job_employer"] = {"name": "em", "attrs": {"itemprop": "hiringOrganization"}}
    elements["job_location"] = {"name": "em", "attrs": {"itemprop": "jobLocation"}}
    elements["job_posted"] = {"name": "time", "attrs": {"class": "share_links jobDate cls_job_date_format"}}
    elements["job_skills"] = {"name": "ul", "attrs": {"itemprop": "skills"}}
    elements["job_experience"] = {"name": "span", "attrs": {"class": "snp_yoe"}}
    elements["job_description"] = {"name": "div", "attrs": {"class": "jobdescription pull-left"}}
    elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath
    # elements["job_salary"] = {"name": "span", "attrs": {"itemprop": "baseSalary"}}
    # elements["job_recruiter"] = {"name": "a", "attrs": {"class": "rec_name"}}
    return elements

def WisdomJobs_config():
    elements = {}
    elements["job_count"] = {"name": "div", "attrs": {"class": "col-md-12 text-center"}}
    elements["job_section"] = {"name": "span", "attrs": {"itemtype": "http://schema.org/JobPosting"}}
    elements["job_title"] = {"name": "span", "attrs": {"itemprop": "title"}}
    elements["job_url"] = {"name": "a", "attrs": {"itemprop": "url"}}
    elements["job_summary"] = {"name": "p", "attrs": {"itemprop": "description"}}
    elements["job_employer"] = {"name": "span", "attrs": {"itemprop": "hiringOrganization"}}
    elements["job_location"] = {"name": "span", "attrs": {"itemprop": "jobLocation"}}
    elements["job_posted"] = {"name": "ul", "attrs": {"class": "job-post-det"}}
    elements["job_skills"] = {"name": "ul", "attrs": {"class": "skills-list"}}
    elements["job_experience"] = {"name": "span", "attrs": {"itemprop": "experienceRequirements"}}
    elements["job_description"] = {"name": "p", "attrs": {"itemprop": "description"}}
    elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath

    return elements
