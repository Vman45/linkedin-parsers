#!/usr/bin/env python3
"""
Script that reads employee names from Excel and output email in these formats:
 a) {first_initial}{last}@{company}.com
 b) {first_initial}{[A-Z]}{last}@{company}.com
v2 - allows for argparse + auto cleaning of Out Of Scope targets
"""

from pathlib import Path
import pandas as pd
import re
from string import ascii_lowercase
import argparse


def email_gen(names, exclusion, sheet):
    """ Function that do the following in order:
    1. Take first_initial and join with last, remove all punctuations, append
    {entity}.com
    2. Take the emails from the exclusion file to form two lists:
     a) as is
     b) remove second index from the emails
    3. If emails is not in the exclusion lists (2.a & 2.b), it is not OOS
    4. The emails from the list is then inserted to a new list that has 27 
    variations:
     a) as is
     b) insert second index with [a-z] """
    emails = [name.split(maxsplit=1)[0][0] + re.sub(r"[ -.]", "", \
        name.split(maxsplit=1)[1]) + "@" + sheet.lower() + ".com" \
            for name in names]
    emails_cleansed = []
    with exclusion.open(mode="r", encoding="utf-8") as fin:
        emails_exc_orig = [email.lower() for email in fin.read().splitlines()]
        emails_exc = [email[:1] + email[2:] for email in emails_exc_orig]
        for email in emails:
            if (email.lower() not in emails_exc) and \
            (email.lower() not in emails_exc_orig):
                emails_cleansed.append(email.lower())
    emails_final = []
    for email in emails_cleansed:
        emails_final.append(email)
        for char in ascii_lowercase:
            emails_final.append(email[:1] + char + email[1:])
    return emails_final


def main(input, exclusion, sheet, output):
    """ Load the excel file, desired sheet and column, then convert to a list 
    Then do all the filtering and formatting, finally save the result """
    excel_file = input
    excel_data_df = pd.read_excel(excel_file, sheet_name=sheet)
    excel2list = excel_data_df["Name"].tolist()
    names_non_li = list(filter(lambda a: a != "LinkedIn Member" and \
        a != "LinkedIn Mitglied", excel2list))
    names_cleansed = [
        name.split(",")[0] if "," in name else name for name in names_non_li
        ]
    output_file = output
    with output_file.open(mode="w", encoding="utf-8") as fout:
        fout.writelines(line + "\n" for line in email_gen\
            (names_cleansed, exclusion, sheet))


def create_parser():
    parser = argparse.ArgumentParser(
        prog="PROG", 
        formatter_class=argparse.RawDescriptionHelpFormatter, 
        description="""
A parser that reads employee names from Excel and output email in this format:
{first_initial}{[A-Z]}{last}@{company}.com
    """)
    parser.add_argument("-e", "--exclude", type=Path, 
    help="File that contains emails to exclude")
    parser.add_argument("-i", "--inputf", type=Path, 
    help="Excel file to parse", required=True)
    parser.add_argument("-o", "--outputf", type=Path, 
    help="Output file name", required=True)
    parser.add_argument("-s", "--sheetname", 
    help="Sheet with Excel to parse", required=True)
    return parser


def handle_args(args=None):
    if args is None:
        parser = create_parser()
        args = parser.parse_args()

    if args.inputf and args.exclude and args.outputf and args.sheetname:
        main(args.inputf, args.exclude, args.sheetname, args.outputf)
    else:
        raise SystemExit


if __name__ == "__main__":
    handle_args()