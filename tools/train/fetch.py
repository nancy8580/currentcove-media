import sys,json,urllib.request,urllib.parse,time,re,os
key,title=sys.argv[1],sys.argv[2];w=sys.argv[3] if len(sys.argv)>3 else "1400"
H={"User-Agent":"CurrentCoveBot/1.0 (https://github.com/nancy8580/currentcove-media; nancy8580)"}
def get(u):
  for a in range(6):
    try: return urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30).read()
    except Exception as e: print(e,file=sys.stderr);time.sleep(15*(a+1))
  raise SystemExit("fail "+key)
u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(dict(action="query",titles=title,prop="imageinfo",iiprop="url|extmetadata",iiurlwidth=w,format="json"))
r=json.loads(get(u));p=list(r["query"]["pages"].values())[0];ii=p["imageinfo"][0];m=ii["extmetadata"]
b=get(ii.get("thumburl") or ii["url"]);open(f"media/{key}.jpg","wb").write(b)
cr=json.load(open("media/credits.json")) if os.path.exists("media/credits.json") else {}
strip=lambda s:re.sub("<[^>]+>","",s or "").strip()
cr[key]=dict(title=title,license=m.get("LicenseShortName",{}).get("value"),artist=strip(m.get("Artist",{}).get("value"))[:80],date=strip(m.get("DateTimeOriginal",{}).get("value"))[:30],url=ii["descriptionurl"])
json.dump(cr,open("media/credits.json","w"),indent=1);print(key,cr[key])
