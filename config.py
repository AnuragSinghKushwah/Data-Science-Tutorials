chromepath = "C:\\Users\\IND\\Desktop\\chromedriver"
logfile = "C:\\Users\\IND\\Desktop\\res.log"
logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
def Naukri_config():
    elements = {}
    elements["job_count"] = {"name": "span", "attrs": {"class": "cnt"}}
    elements["job_section"] = {"name": "div", "attrs": {"type": "tuple"}}
    elements["job_url"] = {"name": "div", "attrs": {"class": "jdurl"}}
    elements["job_title"] = {"name": "font", "attrs": {"class": "hlite"}}
    elements["job_summary"] = {"name": "li", "attrs": {"class": "desig"}}
    elements["job_employer"] = {"name": "span", "attrs": {"class": "org"}}
    elements["job_location"] = {"name": "span", "attrs": {"class": "loc"}}
    elements["job_skills"] = {"name": "span", "attrs": {"class": "skill"}}
    elements["job_salary"] = {"name": "span", "attrs": {"class": "salary"}}
    elements["job_experience"] = {"name": "span", "attrs": {"class": "exp"}}
    elements["job_recruiter"] = {"name": "a", "attrs": {"class": "rec_name"}}
    elements["job_posted"] = {"name": "span", "attrs": {"class": "date"}}
    elements["job_description"] = {"name":"span", "attrs": {"class": "desc"}}
    # elements["phantomjspath"] = phantomjspath
    elements["chromepath"] = chromepath

    return elements
