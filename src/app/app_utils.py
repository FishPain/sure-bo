import requests
import json
import bs4
import re


def get_job_from_jobstreet(url: str)->dict:
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    job_details = json.loads(soup.findAll('script')[1].text.replace("window.REDUX_STATE = ", "").replace(";", ""))["details"]
    job_dict = dict()
    job_dict["title"] = job_details["header"]["jobTitle"]
    job_dict["location"]=job_details["location"][0]["location"]
    job_dict["salary_range"] = job_details["header"]["salary"]["min"] + "-" + job_details["header"]["salary"]["max"] if job_details["header"]["salary"]["isVisible"] else ''
    job_dict["company_profile"] = job_details["companyDetail"]["companyOverview"]["html"]
    job_dict["description"] = job_details["jobDetail"]["jobDescription"]["html"]
    job_dict["benefits"] = " ".join([i for i in job_details["jobDetail"]["jobRequirement"]["benefits"] if i != "-"])
    job_dict["has_company_logo"] = str(all([job_details["header"]["logoUrls"] is not None]))
    job_dict["employment_type"] = job_details["jobDetail"]["jobRequirement"]["employmentType"]
    job_dict["required_experience"] = job_details["jobDetail"]["jobRequirement"]["careerLevel"]
    job_dict["required_education"] = job_details["jobDetail"]["jobRequirement"]["qualification"]
    job_dict["industry"] = job_details["jobDetail"]["jobRequirement"]["industryValue"]["value"]
    job_dict["function"] = job_details["jobDetail"]["jobRequirement"]["jobFunctionValue"][0]["name"]
    return job_dict

def is_valid_jobstreet_url(url):
    return re.match(r'https:\/\/www\.jobstreet\.com\.sg\/[^\s"]+', url)