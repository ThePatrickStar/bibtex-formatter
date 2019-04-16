import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import author
from bibtexparser.bibdatabase import STANDARD_TYPES
from util import *


def format_bib(config):

    with open(config['input_path']) as input_file:
        bib_parser = BibTexParser()
        bib_parser.ignore_nonstandard_types = False
        bib_db = bibtexparser.load(input_file, bib_parser)
        bib_entries = bib_db.entries

        if len(bib_entries) == 0:
            warn("No valid entries in the input bib file: {}".format(
                config['input_path']))

        report = {}

        tidy_up(bib_entries, report, config['verbose'])

        if config['merge']:
            bib_entries = merge_entries(bib_entries, report, config['verbose'])

        write_output(bib_entries, config)


def tidy_up(bib_entries, report, verbose):
    info("tidying up the parsed bib file ...")
    non_standard_entry_list = []
    entry_type_dict = {}

    for bib_entry in bib_entries:
        # reformat the author names
        if 'author' in bib_entry:
            bib_entry = author(bib_entry)
            bib_entry['author'] = ' and '.join(bib_entry['author'])
        # warn about non-standard entry types
        if bib_entry['ENTRYTYPE'] not in STANDARD_TYPES:
            non_standard_entry_list.append(
                (bib_entry['ID'], bib_entry['ENTRYTYPE']))
            if verbose:
                info(
                    "entry: {} has a non-standard type: {}".format(bib_entry['ID'], bib_entry['ENTRYTYPE']))
        # count the number of entries for different entry types
        if bib_entry['ENTRYTYPE'] not in entry_type_dict:
            entry_type_dict[bib_entry['ENTRYTYPE']] = 1
        else:
            entry_type_dict[bib_entry['ENTRYTYPE']] += 1
        # build up signatures for bib entries
        # TODO: maybe use more signatures
        bib_entry['sig1'] = bib_entry['title'].replace(' ', '').lower()

    report['non_standard_list'] = non_standard_entry_list


# currently simple, leave it for future updates on sigs
def sig_matches(bib_entry1, bib_entry2):
    return bib_entry1['sig1'] == bib_entry2['sig1']


def merge_entries(bib_entries, report, verbose):
    info('merging duplicate bib entries ...')
    for bib_entry1 in bib_entries:
        for bib_entry2 in bib_entries:
            if bib_entry1['ID'] != bib_entry2['ID'] and sig_matches(bib_entry1, bib_entry2) and 'dup' not in bib_entry1:
                # mark bib_entry2 as duplicate
                bib_entry2['dup'] = True
                if verbose:
                    info("{} is a duplicate of {}, removing it".format(
                        bib_entry2['ID'], bib_entry1['ID']))

    bib_entries = [
        bib_entry for bib_entry in bib_entries if not 'dup' in bib_entry]

    return bib_entries


def write_output(bib_entries, config):
    db = BibDatabase()
    # clean up the bib_entries
    for bib_entry in bib_entries:
        bib_entry.pop("sig1")
    db.entries = bib_entries
    writer = BibTexWriter()
    writer.indent = ' ' * config['space']
    writer.order_entries_by = ('ENTRYTYPE', 'title')
    if config['sort'] == 'ne':
        writer.order_entries_by = ('title', 'ENTRYTYPE')
    if config['inplace']:
        with open(config['input_path'], 'w') as output_file:
            output_file.write(writer.write(db))
    else:
        print('''
        ##########################################
        # Formatted file preview
        ##########################################
        ''')
        print(writer.write(db))
