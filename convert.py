#!/usr/bin/env python3.7

import csv
import json
import sys

def mapLabel(x):
    return {
        'Website': 'URL',
        'E-mail': 'Email',
    }.get(x, x)

def combineFields(fields):
    return { mapLabel(field['label']): field['value'] for field in fields if field['value'] }

def createEntry(item):
    fields = combineFields(item['fields'])

    username = fields.pop('Username', None)
    if not username:
        username = fields.pop('Email', None)

    entry = {
        'Title': item['title'],
        'Username': username,
        'Password': fields.pop('Password', None),
        'URL': fields.pop('URL', None),
        'Notes': '\n'.join('%s: %s' % (key, value) for (key, value) in fields.items())
    }
    entry['Notes'] += item['note']

    return entry

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <enpass json export file>')
        exit(1)

    fname = sys.argv[1].rsplit('.', 1)[0]

    with open(f'{fname}.json') as f:
        data = json.load(f)

    entries = [ createEntry(item) for item in data['items'] ]

    with open(f'{fname}.csv', 'w', newline='') as csvfile:
        fieldnames = ['Title', 'Username', 'Password', 'URL', 'Notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)
