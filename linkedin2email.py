#!/usr/bin/env python3
"""
A script that, given a company name, extracts a list of its employees from 
LinkedIn to produce text files that consist of commonly seen email formats

Author: Jeffrey Soh
"""

from pathlib import Path
import re
import argparse
import unicodedata
from termcolor import colored
import linskrap


def create_parser():
    parser = argparse.ArgumentParser(
        prog="linkedin2email.py", 
        formatter_class=argparse.RawDescriptionHelpFormatter, 
        description="""
=========================================================================
#                           linkedin2email.py                           #
#                                                                       #
# A script that, given a company name, extracts a list of its employees #
# from LinkedIn to produce:                                             #
#  1. Email addresses in the following email formats:                   #
#     1.1 {first_initial}{last}@{domain}                                #
#     1.2 {first}{last}@{domain}                                        #
#     1.3 {first}.{last}@{domain}                                       #
#     1.4 {first}_{last}@{domain}                                       #
#     1.5 {first}{last_initial}@{domain}                                #
#     1.6 {first}@{domain}                                              #
#     1.7 {last}{first_initial}@{domain}                                #
=========================================================================
    """)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v1.0")
    parser.add_argument("-w", "--webdriver", help="Chrome webdriver location", type=Path, required=True)
    parser.add_argument("-u", "--username", help="LinkedIn username", required=True)
    parser.add_argument("-p", "--password", help="LinkedIn password", required=True)
    parser.add_argument("-c", "--company", help="Company to scrape", required=True)
    parser.add_argument("-d", "--domain", help="Domain name to append to the generated emails", required=True)
    
    args = parser.parse_args()

    if args.webdriver and args.username and args.password and args.company and args.domain:
        email_format_gen(args.webdriver, args.username, args.password, args.company, args.domain)
    else:
        raise SystemExit

    return args


def replace_accents(text):
    """ Given a text, transforms any accented chars to its Latin alphabet equiv
    for e.g. ä > a, ç > c, é > e """
    try:
        text = unicode(text, "utf-8")
    except NameError:
        pass

    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    return str(text)


def email_format_gen(driver, username, password, company, domain):
    """ main function that takes the employee list to output them into various 
    common email address formats """
    names = [replace_accents(name.lower()) for name in linskrap.skrap_emp(driver, username, password, company)]
    if names:
        # Remove any occurrence of , and ( which people regularly use to broadcast about their credentials/certs
        names_cleansed = [re.sub(r"[.']", "", re.split(r"[,(]+", name)[0]) 
        if "," or "(" in name else re.sub(r"[.']", "", name) for name in names]
        # Ensure we have more than 1 name (at least first+last) on each row
        names_cleansed = [name for name in names_cleansed if len(name.split()) > 1]
        print(colored(f"[+] Success! A total of {len(names_cleansed)} employees found:", "green"))
        print(*names_cleansed, sep="\n")
        print("\n" * 2)
        print(f"[*] Generating email addresses in the following formats:")
        print(f"{{first_initial}}{{last}}@{domain}")
        print(f"{{first}}{{last}}@{domain}") 
        print(f"{{first}}.{{last}}@{domain}")
        print(f"{{first}}_{{last}}@{domain}")
        print(f"{{first}}{{last_initial}}@{domain}")
        print(f"{{first}}@{domain}")
        print(f"{{last}}{{first_initial}}@{domain}")
        print("\n" * 2)
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
            emails_f1 = [name.split(maxsplit=1)[0][0] + re.sub(r"[ ]", "", 
            name.split(maxsplit=1)[1]) + "@" + domain for name in names_cleansed]
            f1.write("\n".join(emails_f1))
            emails_f2 = [name.split(maxsplit=1)[0] + re.sub(r"[ ]", "", 
            name.split(maxsplit=1)[1]) + "@" + domain for name in names_cleansed]
            f2.write("\n".join(emails_f2))
            emails_f3 = [name.split(maxsplit=1)[0] + "." + re.sub(r"[ ]", "", 
            name.split(maxsplit=1)[1]) + "@" + domain for name in names_cleansed]
            f3.write("\n".join(emails_f3))
            emails_f4 = [name.split(maxsplit=1)[0] + "_" + re.sub(r"[ ]", "", 
            name.split(maxsplit=1)[1]) + "@" + domain for name in names_cleansed]
            f4.write("\n".join(emails_f4))
            emails_f5 = [name.split(maxsplit=1)[0] + re.sub(r"[ ]", "", 
            name.split(maxsplit=1)[1][0]) + "@" + domain for name in names_cleansed]
            f5.write("\n".join(emails_f5))
            emails_f6 = [name.split(maxsplit=1)[0] + "@" + domain 
            for name in names_cleansed]
            f6.write("\n".join(emails_f6))
            emails_f7 = [re.sub(r"[ ]", "", name.split(maxsplit=1)[1]) + 
            name.split(maxsplit=1)[0][0] + "@" + domain for name in names_cleansed]
            f7.write("\n".join(emails_f7))
            output_text = "[+] Email lists saved under:"
            print(colored("{:<30}{}\\*".format(output_text, output_dir), "green"))
    else:
        print(colored(f"[!] Uh-oh, list is empty! Either no employees found or something's wrong.", "red"))
        

if __name__ == "__main__":
    create_parser()