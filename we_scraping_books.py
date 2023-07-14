import json
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def request_books(id):
    index = 1
    Flag = True
    all_books = []
    while Flag:
        book_url = f"http://webookbot.yammobots.com/Item/_list?name=*&authorguid={id}&pageindex={index}&categorytitle=*"
        r = requests.get(book_url)
        check = r.text.strip().lower().replace('\"','')
        if check == 'noresult':
            # print(f"End: {r.text}")
            Flag = False
        else:
            ## scraping from current book list
            data = BeautifulSoup(r.content, 'html.parser')
            ## find the first div with onclick element
            grid_items = data.find_all('div', {"class": "grid-item"})
            print(len(grid_items))
            
            
            for item in grid_items:
                book_data = {}
                ## find book cover & name
                find_img = item.find('img')
                book_url = find_img['src']
                # print(book_url)
                book_data["book_url"] = book_url
                
                ## instead of this header text, I should take data from pricing section
                ## or take both? sometime, burmese writing can be wrong
                header_name = item.find('h4').get_text(strip=True)
                # print(header_name)
                book_data["book_header_name"] = header_name
                
                ## find author info again - that can be useful to re-check
                find_author = item.find('div', {'class': 'mt-5'})
                find_author_id = find_author.find('a', onclick=True)
                author_id = re.match(r"^.*\(\'(.*)\'\)$", find_author_id['onclick']).group(1).strip()
                author_name = find_author.get_text(strip=True)
                # print(f"{author_id} : {author_name}")
                book_data["author_id"] = author_id
                book_data["author_name"] = author_name
                
                ## find pricing & name
                find_button = item.find('button')
                book_id = find_button['data-id']
                book_name = find_button['data-name']
                book_price = find_button['data-price']
                item_type = find_button['data-itemtype']
                
                # print(book_id)
                book_data["book_id"] = book_id
                book_data["book_name"] = book_name
                book_data["book_price"] = book_price
                book_data["item_type"] = item_type
                
                ## append to list
                all_books.append(book_data)
            ## Flag is still true , add 1 to index for the next checking url
            index += 1
        
    return all_books
            



with open('./all_authors_final.json', 'r', encoding='utf-8') as f:
    all_authors = json.load(f)
    # print(len(all_authors))
    # print(type(all_authors[0]))
    book_df = pd.DataFrame(
        columns=["book_id", "book_name", "book_price", "book_url", "book_header_name", "author_id", "author_name","item_type"])
    
    for author in all_authors:
        id = author["id"]
        books = request_books(id) ## return type is List of Dictionaries
        print(f"ID:{id} -> Length:{len(books)}")
        
        ## no more append in Pandas new version, need to use concat
        book_df = pd.concat([book_df, pd.DataFrame(books)], ignore_index=True)
        book_df['check_id'] = id
        book_df['check_name'] = author["name"]
        
    print(book_df.shape)
    print(book_df.columns)
    # print(book_df.head(5))
    book_df.to_csv("all_books.csv", encoding='utf-8')
    book_df.to_parquet("all_books.parquet", index=False , engine="auto")
            
            
            
        
    