import urllib, json

disqus = "http://disqus.com/api/3.0/posts/list.json"


def makeURL(base, key, forum, thread, cursor=None):
  url = "%s?api_key=%s&forum=%s&thread=%s" % (base, key, forum, thread)
  if cursor:
    url = "%s&cursor=%s" % (cursor)
  return url

def getJSON(url):
  resp = urllib.urlopen(url)
  data = json.loads(resp.read())
  return data

def getNext(data):
  if data and data.has_key("cursor"):
    cursor = data["cursor"]
    if cursor.has_key("next"):
      return cursor["next"]
  return None


api_key = open("api_key.txt").read().strip()
forum = "breitbartproduction"
thread = "link:http://www.breitbart.com/tech/2016/11/12/report-university-of-pennsylvania-offers-puppies-coloring-books-to-students-distraught-over-trump-win"


url = makeURL(disqus, api_key, forum, thread)
data = getJSON(url)
hops = 0
while data and hops < 3:
  nextPage = getNext(data)
  print nextPage
  if nextPage:
    url2 = "%s&cursor=%s" % (url, nextPage)
    data = getJSON(url2)
  else:
    break
  hops += 1

