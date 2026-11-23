import sys,json,urllib.request,urllib.parse,time
q=sys.argv[1]
u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(dict(action="query",generator="search",gsrsearch=q+" filetype:bitmap",gsrnamespace=6,gsrlimit=12,prop="imageinfo",iiprop="url|size|extmetadata",iiurlwidth=1200,format="json"))
for a in range(4):
  try: r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"CurrentCoveBot/1.0 (https://github.com/nancy8580/currentcove-media)"}),timeout=20));break
  except Exception as e: time.sleep(8*(a+1))
else: print("FAIL");sys.exit()
for p in r.get("query",{}).get("pages",{}).values():
  ii=p["imageinfo"][0];m=ii["extmetadata"]
  print(p["title"][:100],ii["width"],ii["height"],m.get("LicenseShortName",{}).get("value"),"|",m.get("DateTimeOriginal",{}).get("value","")[:20])
