#!/bin/bash

# Remove temporary stuff
[ -d tmp ] && rm -r tmp

# Delete cfl and hdr files
[ -d results ] && rm -r results
