from collections import namedtuple
import os
from multiprocessing import Pool

from config import BASE_DIR
from src.html_scraper import OUTDIR as INPUTDIR
from src.html_scraper import TXT_DIR


OUTPUTDIR = os.path.join(TXT_DIR, "cleaned")
FILES = os.listdir(INPUTDIR)

File = namedtuple('File', ['filename', 'content'])

def pmap(func, iterable):
    with Pool(4) as pool:
        yield from pool.map(func, iterable)


def notnl(l):
    return l != '\n' and len(l) > 0


def sections(content):
    approved = []
    lines = filter(notnl, content)
    skip_sections = ["Related Articles", "Further Reading"]
    for line in lines:
        if line.strip() == "Contents":
            line = next(lines)
            while line[0].isdigit():
                line = next(lines)
        elif line.strip() in skip_sections:
            break
        else:
            approved.append(line)
    return approved


def input_file(filename):
    with open(os.path.join(INPUTDIR, filename)) as f:
        content = "".join(sections(f.readlines()))
        if 100 <= len(content.split(" ")) < 1400 and "helicopter" not in content.lower():
            return File(filename=filename, content=content)


def output_file(file):
    if file is None:
        return None
    with open(os.path.join(OUTPUTDIR, file.filename), "w+") as f:
       f.write(file.content)


def clean_files():
    print("Cleaning scraped")
    list(pmap(output_file, map(input_file, FILES)))
