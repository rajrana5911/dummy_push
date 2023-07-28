import requests
url='http://suggestqueries.google.com/complete/search?output=youtube&ds=yt&hl=en&q=news&gl=usa'
r=requests.get(url)
av=(r.text)
# print(av.json())
print(av)