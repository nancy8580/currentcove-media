import sys,json,urllib.request,urllib.parse
q=sys.argv[1]
u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(dict(action="query",generator="search",gsrsearch=q+" filetype:bitmap",gsrnamespace=6,gsrlimit=15,prop="imageinfo",iiprop="url|size|extmetadata",iiurlwidth=1200,format="json"))
r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"CurrentCove/1.0 (nancy8580)"})))
for p in r.get("query",{}).get("pages",{}).values():
  ii=p["imageinfo"][0];m=ii["extmetadata"]
  print(p["title"][:90],ii["width"],ii["height"],m.get("LicenseShortName",{}).get("value"),"|",m.get("DateTimeOriginal",{}).get("value","")[:20])
