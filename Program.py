from argparse import ArgumentParser
from pathlib import Path
from pathlib import os
import csv


class Email:
    def __init__(self, user, domain):
        self.user = user
        self.domain = domain


class EmailLog:
    def __init__(self, log, user, domain):
        self.log = log
        self.user = user
        self.domain = domain


class EmailEntry:
    def __init__(self, name, address):
        self.name = name
        self.address = address


class EmailParser:
    folder_with_emails = "emails"

    def __init__(self):
        self.correct_emails_list = []    # list with valid e-mail adresses
        self.incorrect_emails_list = []  # list with invalid e-mail adresses

    def csv_load_files(self):
        all_csv_paths = Path(EmailParser.folder_with_emails).glob("*.csv")
        for csv_path in all_csv_paths:
            print(f"Found: {csv_path}")
            with open(csv_path, 'r') as csv_file:
                csv_line = csv.reader(csv_file, delimiter=';')
                for row in csv_line:
                    if(len(row) != 2):
                        continue
                    else:
                        name = row[0]
                        address = row[1]
                        entry = EmailEntry(name, address)
                        if self.valid_email(entry.address):
                            self.correct_emails_list.append(entry.address)
                        else:
                            self.incorrect_emails_list.append(entry.address)

    def txt_file_load(self):
        all_txt_paths = Path(EmailParser.folder_with_emails).glob("*.txt")
        for txt_path in all_txt_paths:
            print(f"Found: {txt_path}")
            with open(txt_path, 'r') as txt_file:
                for line in txt_file:
                    line = line.strip()
                    if self.valid_email(line):
                        self.correct_emails_list.append(line)
                    else:
                        self.incorrect_emails_list.append(line)

    # condition invalid email addresses

    # only once @
    def first_condition(self, email):

        how_many = email.count("@")

        if(how_many == 1):
            return True
        return False

    # length of the part before the @ is at least 1
    def second_condition(self, email):

        index = email.rfind("@")

        if(index <= 1):
            return False
        return True

    # length of the part between @ and . is at least 1
    def third_condition(self, email):

        index_pin = email.rfind("@")
        index_dot = email.rfind(".")

        if((index_pin > 0 and index_dot > 0) and (index_dot - index_pin >= 1)):
            return True
        return False

    # length of the part after the last . is at least 1 and
    # at most 4 and contains only
    # letters and/or digits
    def fourth_condition(self, email):
        length = len(email)
        index_dot = email.rfind(".") + 1
        last_part_length = length - index_dot

        if(last_part_length < 1 or last_part_length > 4):
            return False
        else:
            return True

    def valid_email(self, email):      # finding invalid e-mail adresses

        is_valid_first = self.first_condition(email)
        is_valid_second = self.second_condition(email)
        is_valid_third = self.third_condition(email)
        is_valid_fourth = self.fourth_condition(email)
        if(
            is_valid_first and
            is_valid_second and
            is_valid_third and
            is_valid_fourth
        ):
            return True
        else:
            return False

    def show_incorrect_emails(self):   # show invalid e-mail adresses
        length = len(self.incorrect_emails_list)
        print(
            f"Number of invalid e-mail adresses({length}):"
            )
        for email in self.incorrect_emails_list:
            print(email)

    # finding str
    def search_email(self, found_email, word):
        for email in self.correct_emails_list:
            if(word in email):
                found_email.append(email)

    def show_found_email(self, found_email):
        print(len(found_email))
        for email in found_email:
            print(email)

    def search_str(self, word):
        found_email = []
        self.search_email(found_email, word)
        self.show_found_email(found_email)

    # group e-mail adresses by one domain
    # in alphabetical order
    def group_by_domain(self):
        email_adresses = []
        domain_set = set()
        domain_list = []
        email_with_this_domain = []

        # save email adresses in class Email
        for email in self.correct_emails_list:
            index_pin = email.rfind("@")
            email_adresses.append(Email(email[:index_pin], email[index_pin:]))

        for email in email_adresses:                  # finding unique domains
            domain_set.add(email.domain)
        domain_list = list(domain_set)    # saving unique domains in list
        domain_list.sort()                # sort domains alphabetically

        for domain in domain_list:  # printing domains first, then adresses
            print(domain)
            for username in email_adresses:
                if(domain == username.domain):
                    email_with_this_domain.append(username.user)
            email_with_this_domain.sort()
            for user in email_with_this_domain:
                print(f"  {user}{domain}")
            email_with_this_domain.clear()

    # appends logs from file with logs to the EmailLog class
    def email_in_log(self, path_to_logs_file, email_log):
        with open(path_to_logs_file, 'r') as logs:
            for line in logs:
                colon_index = line.rfind(":")
                end = line.rfind("'")
                start = line.rfind("'", 0, end - 1)
                index_pin = line.rfind("@", start, end)

                email_log.append(EmailLog(
                    line[:colon_index],
                    line[start + 1: index_pin],
                    line[index_pin: end],
                    ))

    # appends email from class the Email to the list
    def email_on_the_list(self, email_to_check):
        for email in self.correct_emails_list:
            index_pin = email.rfind('@')
            email_to_check.append(Email(
                    email[:index_pin],
                    email[index_pin:]
                    ))

    # checking if email is in the log
    def check(self, email_to_check, email_log, not_send_email_list):
        for email in email_to_check:
            to_be_or_not = True  # if true adress will be saved
            str_email = email.user + email.domain  # create full email adress
            for email_from_log in email_log:
                str_email_from_log = (email_from_log.user
                                      + email_from_log.domain)
                if(str_email == str_email_from_log):  # comparing
                    to_be_or_not = False
                    break
            if to_be_or_not:
                not_send_email_list.append(Email(
                        email.user,
                        email.domain,
                ))

    # printing not sent email
    def show_unsent_emails(self, not_send_email_list):
        not_send_email_list.sort(key=lambda x: x.user)
        print(f"Email not sent ({len(not_send_email_list)}):")
        for line in not_send_email_list:
            print(f"   {line.user}{line.domain}")

    # find emails outside of logs
    def find_emails_not_in_logs(self, path_to_logs_file):
        not_send_email_list = []
        email_to_check = []
        email_log = []
        self.email_in_log(path_to_logs_file, email_log)
        self.email_on_the_list(email_to_check)
        self.check(email_to_check, email_log, not_send_email_list)
        self.show_unsent_emails(not_send_email_list)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-ic', '--incorrect-emails',
        dest="incorrect",
        action="store_true",
        help='identify incorrect emails',
        )
    parser.add_argument(
        '-s', '--search',
        dest="search",
        type=str,
        help='search " " in the files'
        )
    parser.add_argument(
        '-gbd', '--group-by-domain',
        dest="group",
        action="store_true",
        help='Group emails by one domain and order \
                domains and emails alphabetically'
        )
    parser.add_argument(
        '-feil', '--find-emails-not-in-logs',
        dest="find",
        type=str,
        help='Find emails that are \
            not in the provided logs file'
        )

    args = parser.parse_args()
    if args.incorrect:
        ep.show_incorrect_emails()
    elif args.search:
        word = args.search
        ep.search_str(word)
    elif args.group:
        ep.group_by_domain()
    elif args.find:
        path_to_logs_file = args.find
        if os.path.exists(path_to_logs_file):
            ep.find_emails_not_in_logs(path_to_logs_file)
        else:
            print("Wrong path, try again")


if __name__ == "__main__":
    ep = EmailParser()
    print("Loading data")
    ep.csv_load_files()
    ep.txt_file_load()
    print("Result:")
    main()
