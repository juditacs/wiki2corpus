# wiki2corpus

Fast collection of multilingual Wikipedia corpus.

## Introduction

This is a simple script I created for a language identification project when I needed a small multilingual corpus and didn't want to download full Wikipedia dumps.

wiki2corpus is a Wikipedia crawler designed to quickly build a *small* multilingual corpus from Wikipedia articles. It is not suited for crawling a large number of pages (see the --max-pages option).

## Quick start

If you're really impatient, you can have wiki2corpus running with a couple of commands:

1. install dependencies `pip install wikipedia nltk requests[security]` (you need either root access or virtualenv to be able to install the packages)
1. clone the repository
2. create a directory for the corpus e.g. `mkdir -p data/corpus`
3. create a directory for the raw articles if you would like to keep them e.g. `mkdir data/raw`
4. choose a list of language and their corresponding Wikipedia codes (e.g. de en hu)

    python wiki2corpus/wiki2corpus.py de en hu --output data/corpus --save-raw data/raw


This command will download the 10 pages - from the German, the English and the Hungarian Wikipedia - provided in the default seed list and save the results in `data/corpus`.

## Options

| Name | Description | Default |
| ----- | ------ | --- | 
| langcodes | list of Wikipedia codes, positional argument | |
|  --depth |  Recursion maximum depth level | 1 (no recursion) |
| --visited-pages | Visited articles file, this file is both read and written | visited |
|  --max-pages | Stop downloading after N pages if N > 0 | N=0 |
|  --save-raw | Save raw pages in directory. Raw pages are only kept if this option is specified | |
| --output-dir | Save corpus to OUTPUT\_DIR | |
| --seed-pages | Specify your own seed articles | |
|  --skip-last-sections | Skip last N sections (such as references and external links) | 1 | 

### Recommended parameters

It is very important to specify a small depth OR the max-pages argument.
For example if depth=4, then max-pages should be kept to a couple hundred, unless you want a link explosion in large Wikipedias.

For example:

    python wiki2corpus/wiki2corpus.py en de hu --depth 4 --max-pages 100 --output data/corpus --save-raw data/raw

### Seed list

The default seed list:

New York, San Francisco, London, Paris, Budapest, Washington, Berlin, Los Angeles, Seattle, Tokyo

## Python package

wiki2corpus can be installed as a Python package:

    cd wiki2corpus
    pip install .

This command will install all dependencies, otherwise you have to install them manually.

## Author contact

Please report bugs and send feedback to judit@sch.bme.hu
