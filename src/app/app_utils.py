import requests
import json
import bs4
import re
from constants import ModelsConst


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

def get_mock_job():
    job_dict = {'title': 'Senior Software Engineer QA Automation',
    'location': 'US, CA, San Mateo',
    'department': 'Engineering',
    'salary_range': "",
    'company_profile': '<p><img src="#URL_7dd25bbdf11346f7789ced0f5989ec294c4798d31563fb9542a59e162e6829af#"></p>\r\n<p>#URL_ddb080358fa5eecf5a67c649cfb4ffc343c484389f1bbaf2a1cb071e3f2b6e7e# and Aptitude Staffing Solutions have partnered up in an effort to streamline the hiring process and provide a more efficient and effective recruitng model.\xa0 Our focus is to help develop and achieve your career goals while makeing a solid geographical, cultural and professional fiit when leveraging your career into your new and exciting professional venture!</p>\r\n<p>Please direct all communications throughout this process to the HR department at Aptitude Staffing Solutions</p>\r\n<p><a href="mailto:#EMAIL_0c020555b4dbc1c1e03d03c46cc181bcfde81bf5b20fea95d1bc7dc64c79814c#" rel="nofollow" class="external">#EMAIL_0c020555b4dbc1c1e03d03c46cc181bcfde81bf5b20fea95d1bc7dc64c79814c#</a></p>\r\n<p>Darren Lawson | VP of Recruiting | <a href="mailto:#EMAIL_f4da338e899ddba983ac771b001681d1d2d93b3327ddc420a15f4e5a310071a9#" rel="nofollow" class="external">#EMAIL_f4da338e899ddba983ac771b001681d1d2d93b3327ddc420a15f4e5a310071a9#</a>\xa0| #PHONE_90d33c9d7ec1484aebfe37b153d677decc6f5f53b316489ed24061544c04eb66#</p>\r\n<p></p>\r\n<p></p>',
    'description': '<p><b><img src="#URL_7dd25bbdf11346f7789ced0f5989ec294c4798d31563fb9542a59e162e6829af#"></b></p>\r\n<p></p>\r\n<p><b>Senior Software Engineer, QA Automation</b></p>\r\n<p><b>Quality Assurance | San Mateo, CA</b></p>\r\n<p></p>\r\n<p>As a Sr. Software Engineer on our QA Automation team, you will play a key role in continuous deployment in environment and processes. You will be responsible for designing and implementing test infrastructure, and develop “Immune system” - a set of automated test suites that run in less than 10 minutes before every deployment.</p>\r\n<p>Your primary responsibility will be to work with the development, product management and functional testing teams to create new test harnesses and automated test cases. These test systems validate the software functional correctness and performance capabilities.</p>\r\n<p>\xa0</p>\r\n<p><b>Responsibilities:</b></p>\r\n<p>• Build advanced automated test suites to exercise our world-class applications</p>\r\n<p>• Work with the development and functional test teams to automate test cases</p>\r\n<p>• Analyze and decompose a complicated software system and design a strategy to test this system.</p>\r\n<p>• Train and mentor other team members.</p>\r\n<p>\xa0</p>\r\n<p></p>',
    'requirements': "<p><b>Qualifications:</b></p>\r\n<p>• BS in Computer Science or similar field (In lieu of degree, 3 years of relevant work experience).</p>\r\n<p>• 3-5 years of relevant work experience in software development and/or test automation</p>\r\n<p>• Good scripting skills in at least one common language (Python, Perl, Shell)</p>\r\n<p>• Excellent problem solving and debugging skills</p>\r\n<p>• Proven ability to quickly learn new technologies</p>\r\n<p>\xa0</p>\r\n<p><b>Preferred qualifications:</b></p>\r\n<p>• Master's degree or PhD in Computer Science or related field.</p>\r\n<p>• 5 years of relevant work experience.</p>\r\n<p>• Excellent coding skill in C, C++, Java, or Python.</p>\r\n<p>• Highly proficient in a UNIX/Linux environment.</p>\r\n<p>• Deep knowledge of internet technologies</p>\r\n<p>• Experience with Javascript, AngularJS, Jamine Test Framework</p>\r\n<p>• Experience with Selenium Web Driver</p>\r\n<p>• Familiarity with Continuous Deployment</p>\r\n<p>• Experience with static code analysis</p>\r\n<p></p>",
    'benefits': '<p>Our core values drive our culture. This is what we believe: <a href="#URL_975b6fb195fdb1c17219b1b672586545c479eee51ac7085bc5c2ecd85a22beb4#"><img src="#URL_bb11c3e11938d66936d9e23cd512972fba3f1d13b3076834b86efdf65404727d#"></a></p>\r\n<p>Why #URL_ddb080358fa5eecf5a67c649cfb4ffc343c484389f1bbaf2a1cb071e3f2b6e7e#? Watch our culture video to learn more.</p>\r\n<ul>\r\n<li>MAKE OUR CUSTOMERS SUCCESSFUL Our customers\' success is ours. We live to solve their problems, improve their futures, and exceed their expectations. When our customers win, we win.</li>\r\n<li>SET THE BAR HIGH. We\'re trying to revolutionize an industry, so we can\'t be just good—we have to be the best. That means striving for the best team, product, and company on the planet.</li>\r\n<li>BE ACCOUNTABLE. We own our work. We keep our promises. And we always follow through. We take responsibility for failures, and humble bows for successes. There\'s no time for excuses and finger pointing.</li>\r\n<li>SHOW INTEGRITY. Forget loopholes, back doors, and shades of gray. We just say it. We are honest and straightforward with everyone. The only way we can bring clarity to a chaotic world is to walk-the-walk ourselves.</li>\r\n<li>MAKE EACH OTHER BETTER. Everything we achieve, we achieve together. Nobody is too important to grab a broom.</li>\r\n<li>ALWAYS MOVE FORWARD. We see the world as it could be, not just as it is. With our passion for finding new solutions to old problems, we\'re creating that new world. It\'s a future worth adapting to.</li>\r\n</ul><p>The Benefits <img src="http://#URL_ddb080358fa5eecf5a67c649cfb4ffc343c484389f1bbaf2a1cb071e3f2b6e7e#/styles/images/careers/overview2.jpg"></p>\r\n<ul>\r\n<li>Generous paid time off to help you maintain a good work-life balance</li>\r\n<li>Fully catered lunches available everyday to all employees at the corporate office</li>\r\n<li>Offices fully stocked with snacks and refreshments to keep you energized and productive</li>\r\n<li>Extensive employee benefits and perks to show how much we value your efforts</li>\r\n<li>Fun team events, company events, employee sponsored events, employee recognition awards, and more!</li>\r\n</ul><p></p>\r\n<p><b>\xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0 \xa0\xa0<img src="https://workablehr.s3.amazonaws.com/uploads/account/logo/5233/small_#URL_ddb080358fa5eecf5a67c649cfb4ffc343c484389f1bbaf2a1cb071e3f2b6e7e#_logo_horiz_-_Final.jpg"></b></p>',
    'telecommuting': 'f',
    'has_company_logo': 't',
    'has_questions': 'f',
    'employment_type': 'Full-time',
    'required_experience': "",
    'required_education': "Bachelor's Degree",
    'industry': 'Marketing and Advertising',
    'function': 'Engineering',
    'fraudulent': 't',
    'in_balanced_dataset': 'f'}
    return job_dict

def get_model_list():
    return [model.name for model in ModelsConst]
