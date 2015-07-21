# wiki2corpus

Fast collection of multilingual Wikipedia corpus

## Quick start

1. clone the repository
2. create a directory for the corpus e.g. `mkdir -p data/corpus`
3. create a directory for the raw articles if you would like to keep them e.g. `mkdir data/raw`
4. choose a list of language and their corresponding Wikipedia codes (e.g. de en hu)

    python wiki2corpus/wiki2corpus.py de en hu --output data/corpus --save-raw data/raw


This command will download the 10 pages - from the German, the English and the Hungarian Wikipedia - provided in the default seed list and save the results in `data/corpus`.

## Options

| Name | Description |
| ----- | ------ |
| langcodes | list of Wikipedia codes, positional argument |

positional arguments:
  langcodes             list of Wikipedia codes

optional arguments:
  -h, --help            show this help message and exit
  --depth DEPTH         Specify recursion maximum depth level
  --visited-pages VISITED
                        Specify file with list of visited pages. The file is
                        read and updated as well
  --max-pages MAX_PAGES
                        Stop downloading in a given language if the number of
                        downloaded pages reaches MAXIMUM_PAGES
  --save-raw SAVE_RAW   Save raw pages in directory. Raw pages are only kept
                        if this option is specified
  --output-dir OUTPUT_DIR
                        Save corpus to OUTPUT_DIR
  --seed-pages SEED_PAGES
                        Provide a list of seed articles
  --skip-last-sections SKIP_LAST_SECTIONS
                        Skip last N sections (such as references and external
                        links) of every Wikipedia article


