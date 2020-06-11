#!/usr/bin/env python3
"""
Script that reads data from LinkedIn web log (req & resp) and produced a CSV
and files with commonly seen email address formats.

Author: Jeffrey Soh
"""

from pathlib import Path
import re
import csv
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        prog="linkedin2email.py", 
        formatter_class=argparse.RawDescriptionHelpFormatter, 
        description="""
=========================================================================
#                           linkedin2email.py                           #
#                                                                       #
#  A parser that reads employee names from LinkedIn web log to produce: #
#  1. Output a csv that contains their name and job title               #
#  2. Takes names and output files with the following email formats:    #
#     2.1 {first_initial}{last}@{domain}                                #
#     2.2 {first}{last}@{domain}                                        #
#     2.3 {first}.{last}@{domain}                                       #
#     2.4 {first}_{last}@{domain}                                       #
#     2.5 {first}{last_initial}@{domain}                                #
#     2.6 {first}@{domain}                                              #
#     2.7 {last}{first_initial}@{domain}                                #
=========================================================================
    """)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.2")
    parser.add_argument("-i", "--inputf", type=Path, 
    help="LinkedIn web log to parse", required=True)
    parser.add_argument("-d", "--domain", 
    help="Domain name to append to the emails", required=True)
    
    args = parser.parse_args()

    if args.inputf and args.domain:
        email_format_gen(args.inputf, args.domain)
    else:
        raise SystemExit

    return args


def create_csv(file):
    html_input = file
    csv_output = Path.cwd() / "names_positions.csv"
    pattern_name = re.compile(r"\"title\":.*?\"text\":\".*?\"")
    pattern_position = re.compile(r"\"headline\":.*?\"text\":\".*?\"")

    with html_input.open(mode="r", encoding="utf-8") as fin, csv_output.open(mode="w", encoding="utf-8", newline="") as fout:
        text = fin.read()
        match_name = re.findall(pattern_name, text)
        match_position = re.findall(pattern_position, text)
        names = [i.split(":")[-1].strip("\"") for i in match_name]
        positions = [i.split(":")[-1].strip("\"") for i in match_position]
        names_cleansed = [re.sub(r"[-.']", "", name.split(",")[0]) if "," in name else re.sub(r"[-.']", "", name) for name in names]
        # create a tuple as dup keys won't work in dict
        combined = tuple(zip(names_cleansed, positions))
        writer = csv.DictWriter(fout, fieldnames=["Name", "Job Description"])
        writer.writeheader()
        names_cleansed_nonli = []
        for name, position in combined:
            if name != "LinkedIn Member" and name != "LinkedIn Mitglied":
                row = {"Name": name, "Job Description": position}
                writer.writerow(row)
                names_cleansed_nonli.append(name)
        output_text = "[*] CSV file saved at:"
        print("{:<30}{}".format(output_text, csv_output))
        return names_cleansed_nonli


def email_format_gen(input, domain):
    names = [name.lower() for name in create_csv(input)]
    output_dir = Path.cwd() / domain
    output_dir.mkdir(exist_ok=True)
    f1 = output_dir / "flast.txt"
    f2 = output_dir / "firstlast.txt"
    f3 = output_dir / "first.last.txt"
    f4 = output_dir / "first_last.txt"
    f5 = output_dir / "firstl.txt"
    f6 = output_dir / "first.txt"
    f7 = output_dir / "lastf.txt"
    with f1.open(mode="w") as f1, f2.open(mode="w") as f2, \
        f3.open(mode="w") as f3, f4.open(mode="w") as f4, \
            f5.open(mode="w") as f5, f6.open(mode="w") as f6, \
                f7.open(mode="w") as f7:
        emails_f1 = [name.split(maxsplit=1)[0][0] + re.sub(r"[ ]", "", name.split(maxsplit=1)[1]) + "@" + domain for name in names]
        f1.write("\n".join(emails_f1))
        emails_f2 = [name.split(maxsplit=1)[0] + re.sub(r"[ ]", "", name.split(maxsplit=1)[1]) + "@" + domain for name in names]
        f2.write("\n".join(emails_f2))
        emails_f3 = [name.split(maxsplit=1)[0] + "." + re.sub(r"[ ]", "", name.split(maxsplit=1)[1]) + "@" + domain for name in names]
        f3.write("\n".join(emails_f3))
        emails_f4 = [name.split(maxsplit=1)[0] + "_" + re.sub(r"[ ]", "", name.split(maxsplit=1)[1]) + "@" + domain for name in names]
        f4.write("\n".join(emails_f4))
        emails_f5 = [name.split(maxsplit=1)[0] + re.sub(r"[ ]", "", name.split(maxsplit=1)[1][0]) + "@" + domain for name in names]
        f5.write("\n".join(emails_f5))
        emails_f6 = [name.split(maxsplit=1)[0] + "@" + domain for name in names]
        f6.write("\n".join(emails_f6))
        emails_f7 = [re.sub(r"[ ]", "", name.split(maxsplit=1)[1]) + name.split(maxsplit=1)[0][0] + "@" + domain for name in names]
        f7.write("\n".join(emails_f7))
        output_text = "[*] Email lists saved under:"
        print("{:<30}{}\\*".format(output_text, output_dir))
        

if __name__ == "__main__":
    create_parser()