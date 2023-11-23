import requests
import re
import json
from bs4 import BeautifulSoup
from links import WEinfo
from datetime import datetime
from support_functions import set_logger, write_json_file

info = WEinfo(0)


## Request function from author url
def request_author(url):
    r = requests.get(url)
    # print(r.status_code)

    if r.status_code == 200:
        data = BeautifulSoup(r.content, "html.parser")

        ## find the first div with onclick element
        all_onclick = data.find_all("div", onclick=True)
        # print(f"Len of onclick : {len(all_onclick)}")
        if len(all_onclick) > 0:
            author_result = []
            for oc in all_onclick:
                id_tag = oc["onclick"]
                id = re.match(r"^.*\(\'(.*)\'\)$", id_tag).group(1).strip()
                id_name_dict = {"id": id}
                name_tag = oc.find("h5").text.strip()
                id_name_dict["name"] = name_tag
                author_result.append(id_name_dict)
            return author_result
        ## else: onclick is length 0 -> return None (same as return blank list)
        return None

    ## if not 200, Raise connection error
    r.raise_for_status()


def get_author_data():
    ## get today as Month_day (example : Jan_01)
    get_today = datetime.now().strftime("%b_%d")

    ## index -> 1 to 83
    all_authors = []
    try:
        for index in range(1, 1000):
            info.change(index)
            if get_authors := request_author(info.authors_url):
                all_authors += get_authors
            else:
                # print(f"Return blank for {index}")
                raise ValueError(f"Return blank for {index}")
            # print(f"Done for {index} with {len(all_authors)}")
    except ValueError as e:
        # print(f"Page index can be out of range : {e}")
        log.error(f"Page index out of range : {e}")
    finally:
        write_json_file(f"json_files/all_authors_{get_today}", all_authors)
    log.info(f"Total : {len(all_authors)} for {get_today}")
    print("Finished!")


if __name__ == "__main__":
    log = set_logger()
    get_author_data()
