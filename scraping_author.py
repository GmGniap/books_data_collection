import requests
import re
import json
from bs4 import BeautifulSoup


## Request function from author url 
def request_author(url):
    r = requests.get(url)
    print(r.status_code)

    if r.status_code == 200:
        data = BeautifulSoup(r.content, 'html.parser')
        
        ## find the first div with onclick element
        all_onclick = data.find_all('div', onclick=True)
        # print(len(all_onclick))
        author_result = []
        for oc in all_onclick:
            id_name_dict = {}
            id_tag = oc['onclick']
            id = re.match(r"^.*\(\'(.*)\'\)$", id_tag).group(1).strip()
            id_name_dict["id"] = id
            name_tag = oc.find("h5").text.strip()
            id_name_dict["name"] =name_tag
            author_result.append(id_name_dict)
        return author_result
    else:
        ## Raise connection error
        r.raise_for_status()

## index -> 1 to 83
all_authors = []
for index in range(1,84):
    authors_url = f"http://webookbot.yammobots.com/Author/_list?name=*&tags=*&pageindex={index}&categorytitle=*&author=*"
    get_authors = request_author(authors_url)
    if get_authors:
        all_authors += get_authors
    else:
        print(f"Return blank for {index}")
    print(f"Done for {index} with {len(all_authors)}")

print(len(all_authors))
with open("all_authors_final.json", "w", encoding='utf-8') as out:
    json.dump(all_authors, out, ensure_ascii=False)
    