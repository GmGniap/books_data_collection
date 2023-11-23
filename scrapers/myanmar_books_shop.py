import pandas as pd
import requests_html
import ssl

mbl = "https://www.myanmarbookshop.com/All/AllOfBusiness/100?intTake=0&bytIPP=0&intStartRowIndex=0&bytMaximumRows=1000"
# context = ssl._create_unverified_context()
session = requests_html.HTMLSession()
resp = session.get(mbl)
main = resp.html.find(".InnerMost", first=True)
data_table = main.find('table', first=True)

# print(data_table.html)
# print(main.html)
dfs = pd.read_html(data_table.html)
df = pd.concat(dfs)
print(df.shape)
df.to_csv("test_mbs.csv", index=False, encoding='utf-8')
