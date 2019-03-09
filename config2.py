chromepath = "C:\\Users\\IND\\Desktop\\chromedriver"
logfile = "C:\\Users\\IND\\Desktop\\res.log"
logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def Monster_config():
    elements = {}
    elements["job_count"] = {"name": "div", "attrs": {"class": "count pull-left"}}
    elements["job_section"] = {"name": "div", "attrs": {"class": "jobwrap"}}
    elements["job_title"] = {"name": "span", "attrs": {"class": "hightlighted_keyword"}}
    elements["job_url"] = {"name": "a", "attrs": {"target": "_blank"}}
    elements["job_summary"] = {"name": "span", "attrs": {"class": "black"}}
    elements["job_employer"] = {"name": "a", "attrs": {"class": "jtxt orange"}}
    elements["job_location"] = {"name": "div", "attrs": {"class": "jtxt jico ico1"}}
    elements["job_skills"] = {"name": "div", "attrs": {"class": "jtitle"}}
    elements["job_experience"] = {"name": "div", "attrs": {"class": "jtxt jico ico2"}}
    elements["job_posted"] = {"name": "div", "attrs": {"itemprop": "datePosted"}}
    elements["job_description"] = {"name": "div", "attrs": {"class":  "desc"}}
    elements["job_description_skills"] = {"name": "div", "attrs": {"class": "desc"}}
    # elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath


    # elements["job_type"] = {"name": "h4", "attrs": {"class": "job-text employment-info"}}
    # elements["job_employer_text"] = {"name": "a", "attrs": {"class": "dice-btn-link"}}
    # elements["job_morejobs"] = {"name": "a", "attrs": {"class": "company-collapse-link"}}

    return elements