import urllib.request, urllib.parse, urllib.error, json

disqus = "http://disqus.com/api/3.0/threads/listPosts.json"


def makeURL(disqus, key, forum, thread, cursor=None):
  url = "%s?api_key=%s&forum=%s&thread=%s" % (disqus, key, forum, thread)
  if cursor:
    url = "%s&cursor=%s" % (cursor)
  return url

def getJSON(url):
  resp = urllib.request.urlopen(url)
  data = json.loads(resp.read().decode('utf-8'))
  return data

def getNext(data):
  if data and "cursor" in data:
    cursor = data["cursor"]
    if "next" in cursor:
      return cursor["next"]
  return None


api_key = open("api_key.txt").read().strip()
forum = "breitbartproduction"
thread = "ident:5513922&limit=100"


url = makeURL(disqus, api_key, forum, thread)
data = getJSON(url)
hops = 0

while data and hops < 200:
  nextPage = getNext(data)
  with open("Output.txt", "a", encoding='utf-8') as text_file:
    print(data, file=text_file)
  if nextPage:
    url2 = "%s&cursor=%s" % (url, nextPage)
    data = getJSON(url2)
  else:
    break
  hops += 1
