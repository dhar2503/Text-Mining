#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import normanpd
from normanpd import normanpd

# url = ("http://normanpd.normanok.gov/filebrowser_download/657/2018-02-12%20Daily%20Arrest%20Summary.pdf")

def main(url):
    # Download data
    normanpd.fetchincidents(url)
    # Extract Data
    incidents = normanpd.extractincidents()
    # Create Dataase
    normanpd.createdb()
    # Insert Data
    normanpd.populatedb(incidents)
    # Print Status
    normanpd.status()
if __name__ == '__main__':
    main(sys.argv[1])