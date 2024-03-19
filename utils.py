import requests
import yaml
from yaml import SafeLoader
from bs4 import BeautifulSoup
import re
import json as JSON
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html
from resources import clf_base_URL, sam_api_url, sam_base_URL, test_url, improper_resource, fixed_resource, types
response_url=[]
def is_json(myjson):
    try:
        json_object = JSON.loads(myjson)
    except ValueError as e:
        return False
    return True
def fix_json(text):
    text = text.replace(", ... ","")
    text = text.replace(", ...","")
    text = text.replace("{Key:Value}","Object")
    STR_MATCHES = re.findall(r':\s*([a-zA-Z0-9]+)\s*[,}]', text)
    STR_MATCHES = list(set(STR_MATCHES))
    ARRAY_MATCHES = re.findall(r'\[*([a-zA-Z]+)\]', text)
    ARRAY_MATCHES = list(set(ARRAY_MATCHES))
    for match in STR_MATCHES:
        text = text.replace(":"+match+",", ":\""+match + "\",")
        text = text.replace(":"+match+"}", ":\""+match + "\"}")
    for match in ARRAY_MATCHES:
        text = text.replace(" String","String")
        text = text.replace("["+match+"]", "[\""+match + "\"]")
    text = text.replace("\"\"","\"")
    return text

def get_clf_json(soup, type):
    data=soup.find('div', attrs = {'id':'main'})
    if data is None:
        print("No data found",soup)
        print("No data found")
    if data is None:
        return None
    for record in data.findAll('code', attrs = {'class':type}):
        if type == 'yaml':
            cf=record.get_text('', strip=False)
            if "<" in cf:
                pass
            else:
                return cf 
        
        else:
            cf=record.get_text('', strip=True)
            return fix_json(cf)
    
def scrap_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup # If this line causes an error, run 'pip install html5lib' or install html5lib
   
def get_links(soup):
    links = {}
    for a in soup.find_all('a', href=True):
        if a.text in links.keys():
            links[a.text].append(a["href"])
        else:
            links[a.text]=[a["href"]]
    return links

def get_clf_properties(cf, links):
    for key in cf.keys():
        if key == "Type":
            pass
        elif(isinstance(cf[key],dict)):
            cf[key]=get_clf_properties(cf[key],links)
        elif(isinstance(cf[key],list)):
             if(cf[key][0] in links.keys()):
                if len(links[cf[key][0]])>0:
                    TEMP_CLF=generate_clf_schema(links[cf[key][0]],cf[key][0])
                    cf[key][0] = TEMP_CLF
        elif(cf[key] in links.keys()):
                if len(links[cf[key]])>0:
                    TEMP_CLF=generate_clf_schema(links[cf[key]],cf[key])
                    cf[key] = TEMP_CLF
        elif re.match(r'[a-zA-Z0-9 ]* \| [a-zA-Z0-9 ]*', cf[key]):
             cf[key]=cf[key].replace("List of ","")
             cf[key]=cf[key].replace(" ","")
             cf_properties=cf[key].split("|")
             CLF={}
             for cf_property in cf_properties:
                if cf_property not in types and cf_property in links.keys():
                    CLF[cf_property]=generate_clf_schema(links[cf_property],cf_property)
                else:
                    CLF[cf_property]=cf_property
             cf[key] = CLF
    return cf

def generate_clf_schema(urls,key):
    count=1
    dummy_soup=scrap_data(test_url)
    url=""
    baseURL=clf_base_URL
    while True:
        count = count+ 1
        url=urls.pop()
        if "https://" not in url:
            if "sam-" in url:
                url=url.replace("./",sam_base_URL)
                # print("1",url)  
            else:
                url=url.replace("./",baseURL)
                # print("2",url)  
        else:
            if "#" in url:
                temp_url=url.split("#")
                # print("test",temp_url[1])
                if temp_url[1].replace("cfn","") in fixed_resource:
                    # print("3",temp_url)
                    temp_url[1]=temp_url[1].replace("-target","")   
                    url=clf_base_URL+"aws-properties"+fixed_resource[temp_url[1].replace("cfn","")]
                    # print("3","final",url)
                    
                elif  temp_url[1].replace("cfn","") not in improper_resource:
                    # print("4",temp_url)
                    temp_url[1]=temp_url[1].replace("-target","")     
                    url=clf_base_URL+"aws-properties"+temp_url[1].replace("cfn","")
                else:
                    return key
        response_url.append(url)                         
        soup=scrap_data(url)
        links= get_links(soup)
        # print(links)
        if(dummy_soup!=soup):
            break
        if len(urls)==0:
            break
    # print(links)
    response_json=get_clf_json(soup, 'json')
    if response_json is None or is_json(get_clf_json(soup, 'yaml')) is False:
        yaml_data=get_clf_json(soup, 'yaml')
        response_json=yaml.load(yaml_data,Loader=SafeLoader)
        cf=response_json
    else:
        cf=JSON.loads(response_json)
    return get_clf_properties(cf,links)