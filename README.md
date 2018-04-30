# Skybrary Data

An application to download and scrape additional information from
Skybrary.

Options:

```sh
python3 run.py --injest
```

Download RDF data from Skybrary regarding Accident and Incident Reports

```sh
python3 run.py --scrape
```

Scrape additional text from Skybrary for all A&I Reports. Stores in text
format. Also performs some cleaning on the text to reduce the content to
the narrative. 

```sh
python3 run.py --bin
```

Categorises scraped text documents according to the components they
mention.

```sh
python3 run.py --update
```

Overwrite stored RDF file with new data.

```sh
python3 run.py --offline
```

Clean scraped files, bin them, and store new RDF data, doesn't hit
Skybrary website.

```sh
python3 run.py --all
```
Complete new data set.
