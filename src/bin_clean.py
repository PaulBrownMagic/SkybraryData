import re
import os
from functools import partial
from collections import namedtuple, Counter
import shutil

from src.clean_scraped import OUTPUTDIR as INPUTDIR
from src.clean_scraped import TXT_DIR

OUTDIR = os.path.join(TXT_DIR, "bins")

FILES = os.listdir(INPUTDIR)
Category = namedtuple('Category', ['filename', 'bins', 'subject'])


leaf_bins = dict(pylon=r"pylon",
                 nacelle=r"nacelle",
                 rudder=r"rudder",
                 verticalStabilizer=r"vertical stabili[zs]er",
                 constantSection=r"constant section",
                 aftNonConstantSection=r"aft non[ -]*constant section",
                 cargoCompartment=r"cargo *(hold|compartment)",
                 cockpit=r"flight[ -]*deck|cockpit",
                 passengerCompartment=r"passenger *(compartment|cabin)",
                 singleLandingGearSystem="single landing gear *(system)*",
                 elevator=r"elevator",
                 horizontalStabilizer=r"horizontal stabili[sz]er",
                 stabilator=r"stabilator",
                 fuelTank=r"fuel[ -]*tank",
                 winglet=r"winglet"
                 )

bins = dict(engine=r"engine",
            fin=r"\Wfin\W",
            fuselage=r"fuselage",
            cabin=r"cabin",
            cabinSection=r"cabin section",
            landingGear=r"landing gear",
            tailplane=r"tail[ -]*plane",
            tankSystem=r"tank system",
            wing=r"\Wwing\W",
            )


def iterate_bins(filename, binset):
    assigned = []
    for name, regex in binset.items():
        if assign(regex, filename):
            assigned.append(name)
    return assigned


def find_bin(filename):
    leafs = iterate_bins(filename, leaf_bins)
    major = iterate_bins(filename, bins)
    if len(leafs) > 0:
        subject = Counter(leafs).most_common(1)[0][0]
    elif len(major) > 0:
        subject = Counter(major).most_common(1)[0][0]
    else:
        subject = "other"
    assigned = leafs + major
    if len(assigned) == 0:
        assigned.append(subject)
    return assigned, subject


def assign(regex, filename):
    with open(srcfile(filename)) as infile:
        contents = " ".join(infile.readlines()).lower()
        return bool(re.search(regex, contents))


def categorise(filename):
    bins, subject = find_bin(filename)
    return Category(filename, bins, subject)

def srcfile(filename):
    return os.path.join(INPUTDIR, filename)

def dstfile(subject):
    return os.path.join(OUTDIR, subject)

def copy(category):
    outdir = dstfile(category.subject)
    os.makedirs(outdir, exist_ok=True)
    shutil.copy(src=srcfile(category.filename), dst=outdir)
    return category

def bin_clean():
    return list(map(copy, map(categorise, FILES)))
