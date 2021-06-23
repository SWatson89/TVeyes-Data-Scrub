import urllib
import urllib.request
import re


from bs4 import BeautifulSoup

dataurl = "http://mms.tveyes.com/PlaybackPortal.aspx?SavedEditID=38ed2612-dc09-4a53-97ff-ba29fbf77907"




html = urllib.request.urlopen(dataurl).read()
soup = BeautifulSoup(html)
for script in soup(["script", "style"]):

    script.extract()

strips = list(soup.stripped_strings)

print(strips[:])
with requests.Session() as req:
    for item in soup.select("#playlist"):
        for href in item.findAll("a"):
            href = href.get("href")
            name = re.search(r"([^\/]+$)", href).group()
            if '.' not in name[-4]:
                name = name[:-3] + '.mp3'
            else:
                pass
            print(f"Downloading File {name}")
            download = req.get(href)
            if download.status_code == 200:
                with open(name, 'wb') as f:
                    f.write(download.content)
            else:
                print(f"Download Failed For File {name}")
