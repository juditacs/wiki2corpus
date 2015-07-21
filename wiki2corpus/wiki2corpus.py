#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import wikipedia as wp
import re
import logging
from os import path
from collections import defaultdict
from argparse import ArgumentParser
from nltk.tokenize import sent_tokenize


class WPDownloader(object):

    seed_pages = [
        'New York', 'San Francisco', 'London', 'Paris', 'Budapest',
        'Washington', 'Berlin', 'Los Angeles', 'Seattle', 'Tokyo'
    ]
    ws_re = re.compile(r'\s+', re.UNICODE)
    title_re = re.compile(r'^=+', re.UNICODE|re.MULTILINE)

    def __init__(self, wikicode, depth=1, max_pages=0, visited=None, skip_last=0):
        self.wikicode = wikicode
        self.max_depth = depth
        self.max_pages = max_pages
        self.page_counter = 0
        self.skip_last = skip_last
        if visited is None:
            self.visited = set()
        else:
            self.visited = visited
        self.raw_pages = {}

    def set_seed_pages(self, pages):
        if pages is None:
            self.seed_pages = WPDownloader.seed_pages
        else:
            self.seed_pages = pages

    def skip_title(self, title):
        return title.isdigit()

    def download_pages(self):
        wp.set_lang(self.wikicode)
        for title in self.seed_pages:
            self.download_page(title, depth=self.max_depth)

    def download_page(self, title, depth):
        # skip if already visited
        if title in self.visited:
            return
        # skip if maximum depth reached
        if depth < 1:
            return
        # skip if max_pages reached
        if self.max_pages > 0 and self.page_counter >= self.max_pages:
            return
        # skip if title is undesirable
        if self.skip_title(title):
            return
        res = wp.search(title, results=1)
        if len(res) < 1:
            return
        try:
            page = wp.page(res[0])
        except (wp.exceptions.DisambiguationError, wp.exceptions.PageError):
            return
        if page.title in self.visited:
            return
        # now actually adding the page to the collection
        self.visited.add(page.title)
        self.page_counter += 1
        self.raw_pages[page.title] = page.content
        try:
            for link in page.links:
                self.download_page(link, depth - 1)
        except KeyError:
            return
        except Exception as e:
            logging.exception('Unexpected exception, please report: {}'.format(e))

    def save_raw_pages(self, base_dir):
        sep = '%%%##PAGE##%%%\n'
        with open(path.join(base_dir, self.wikicode), 'a+') as f:
            for title, page in sorted(self.raw_pages.iteritems(), key=lambda x: x[0]):
                f.write(u'{0}\n{1}\n{2}\n'.format(sep, title, page).encode('utf8'))

    def convert_raw_pages(self):
        self.corpus = []
        for title, page in self.raw_pages.iteritems():
            if self.skip_last:
                sections = WPDownloader.title_re.split(page)[:-self.skip_last]
            else:
                sections = WPDownloader.title_re.split(page)
            for section in sections:
                p = '\n'.join(section.split('\n')[1:])  # skip section title
                sentences = sent_tokenize(p)
                for s in sentences:
                    s_ = WPDownloader.ws_re.sub(' ', s).strip()
                    if s_:
                        self.corpus.append(s_)

    def save_corpus(self, base_dir):
        with open(path.join(base_dir, self.wikicode), 'a+') as f:
            f.write('\n'.join(self.corpus).encode('utf8') + '\n')

    def save_visited(self, fn):
        with open(fn, 'a+') as f:
            f.write('\n'.join(u'{0}\t{1}'.format(self.wikicode, title) for title in self.visited).encode('utf8') + '\n')


def parse_args():
    p = ArgumentParser()
    p.add_argument('--depth', type=int, default=1, help='Specify recursion maximum depth level')
    p.add_argument('--visited-pages', dest='visited', type=str, default='visited', help='Specify file with list of visited pages. The file is read and updated as well')
    p.add_argument('--max-pages', type=int, dest='max_pages', default=0, help='Stop downloading in a given language if the number of downloaded pages reaches MAXIMUM_PAGES')
    p.add_argument('--save-raw', type=str, default='', help='Save raw pages in directory. Raw pages are only kept if this option is specified')
    p.add_argument('--output-dir', type=str, default='corpus', help='Save corpus to OUTPUT_DIR')
    p.add_argument('--seed-pages', type=str, default='', help='Provide a list of seed articles')  # TODO better explanation
    p.add_argument('--skip-last-sections', type=int, default=1, help='Skip last N sections (such as references and external links) of every Wikipedia article')
    p.add_argument('langcodes', type=str, nargs='+', help='list of Wikipedia codes')
    return p.parse_args()


def read_visited(fn):
    visited = defaultdict(set)
    if fn and path.exists(fn):
        with open(fn) as f:
            for l in f:
                wc, title = l.decode('utf8').strip().split('\t')
                visited[wc].add(title)
    return visited


def main():
    args = parse_args()
    visited = read_visited(args.visited)
    if args.seed_pages:
        with open(args.seed_pages) as f:
            seed_pages = set(l.decode('utf8').strip() for l in f)
    else:
        seed_pages = None
    for wikicode in args.langcodes:
        wp = WPDownloader(wikicode, depth=args.depth, max_pages=args.max_pages, visited=visited.get(wikicode, None), skip_last=args.skip_last_sections)
        wp.set_seed_pages(seed_pages)
        wp.download_pages()
        if args.save_raw:
            wp.save_raw_pages(args.save_raw)
        wp.convert_raw_pages()
        wp.save_visited(args.visited)
        wp.save_corpus(args.output_dir)

if __name__ == '__main__':
    main()
