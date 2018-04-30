from bs4 import BeautifulSoup
import os
import requests

from config import BASE_DIR

TXT_DIR = os.path.join(BASE_DIR, "txt")
OUTDIR = os.path.join(TXT_DIR, "raw")


def is_valid_resp(resp):
    return resp.status_code == requests.codes.ok


def get_page(url):
    res = requests.get(url)
    if not is_valid_resp(res):
        print("INVALID RESPONSE", url)
        return None
    else:
        content = get_html(res)
        fname = f"{url.replace('http://www.skybrary.aero/index.php/Special:URIResolver/','').replace('/','+')}.txt"
        return (fname, content)


def get_html(resp):
    soup =  BeautifulSoup(resp.content, "html.parser").body
    return soup


def scrape_to_file(url):
    page = get_page(url)
    if page is not None:
        fname, html = page
        for side in html.select("#bodyContent")[0].select(".side"):
            side.decompose()
        for footer in html.select("#bodyContent")[0].select(".printfooter"):
            footer.decompose()
        txt = html.select("#bodyContent")[0].text
        with open(os.path.join(OUTDIR, fname), "w") as outfile:
            print(txt, file=outfile)
        return fname, txt
    else:
        return None, None
