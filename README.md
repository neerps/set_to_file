# Script to create and expand a set of items stored in a file

This script was created to help to maintain a sorted set of some items which
come from different sources. I. e. if you need to get a list of interesting
places in your city, and there are 100 suggestions, you can filter them out
to a set of interesting places. Another possible application - get a list
of key skills for some jobs from different job postings.

User still should make some effort, though

Script can work in two modes:

1. user input where user enters each item through the terminal;
2. file input where user prepares a file with items to load into a set.

Mode of operation, paths to files are set through configuration file.
To my experience, it's not convenient to manually write file names in cases where there is a need to work with the same
file in several sessions.
