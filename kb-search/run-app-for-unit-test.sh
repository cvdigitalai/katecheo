#!/bin/sh
env $(cat env-vars.props | xargs) python3 KBSearch.py
