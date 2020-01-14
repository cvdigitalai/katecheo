import json
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Process JSON config file.')
parser.add_argument('target', type=str, help='NER or KB target to set')
args = parser.parse_args()

with open('config.json', 'r') as f:
    config = json.load(f)

kb_entries = []

for topic in config["model"]:
    kb_entry = topic['name'] + '=' + topic['kb_file']
    kb_entries.append(kb_entry)

if args.target == 'kb':
    print(','.join(kb_entries).replace('/', '\/'))
