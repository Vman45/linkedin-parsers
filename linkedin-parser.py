#!/usr/bin/env python3
"""
Script that reads data from LinkedIn web log (req & resp) and output
their name and job title to a csv file
"""

from pathlib import Path
import re
import csv


HTML_INPUT = Path(r"C:\Data\Customers\YYYY-MM\XXXXX-Super Corporation"
    r"\linkedin-SC-001-320.log")
CSV_OUTPUT = Path(r"C:\Data\Customers\YYYY-MM\XXXXX-Super Corporation"
    r"\linkedin-SC-001-320.csv")
PATTERN_NAME = re.compile(r"\"title\":.*?\"text\":\".*?\"")
PATTERN_POSITION = re.compile(r"\"headline\":.*?\"text\":\".*?\"")

with HTML_INPUT.open(mode="r", encoding="utf-8") as fin, \
    CSV_OUTPUT.open(mode="w", encoding="utf-8", newline="") as fout:
    text = fin.read()
    match_name = re.findall(PATTERN_NAME, text)
    match_position = re.findall(PATTERN_POSITION, text)
    names = [i.split(":")[-1].strip("\"") for i in match_name]
    positions = [i.split(":")[-1].strip("\"") for i in match_position]
    # create a tuple as dup keys won't work in dict
    combined = tuple(zip(names, positions))
    writer = csv.DictWriter(fout, fieldnames=["Name", "Job Description"])
    writer.writeheader()
    for name, position in combined:
        row = {"Name": name, "Job Description": position}
        writer.writerow(row)