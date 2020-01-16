import json
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Process JSON config file.')
parser.add_argument('target', type=str, help='NER or KB target to set')
args = parser.parse_args()

with open('config.template.json', 'r') as f:
    config = json.load(f)

kb_entries = []

for topic in config["model"]:
    kb_entry = topic['name'] + '=' + topic['kb_file']
    kb_entries.append(kb_entry)

if args.target == 'kb':
    print(','.join(kb_entries).replace('/', '\/'))

if args.target == 'article_id':
    print(config["article_id"])

if args.target == 'article_title':
    print(config["article_title_key"])

if args.target == 'article_body':
    print(config["article_body_key"])

if args.target == 'sim_threshold':
    print(config["similarity_threshold"])
    
if args.target == 'comp_model':
    print(config["comprehension_model"])