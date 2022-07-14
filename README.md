# Email Task
## Author 
    Piotr Wołoszyk 
## Overview 
This program allows you to valid email, search email, and group by domains. 
## Requirements 
Python 3.10 
## Instruction 
Put Profil_Software_backend.py in the folder that contains the sub-folder "emails". Sub-folder "emails" should contain a txt or CSV file with email entries. To run the program use the terminal.
Use: 
- '-h' or '--help' to see instructions in the terminal. 
- '-ic' or '--incorrect-emails' to see incorrect emails from files. 
- '-s [str]' or '--search [str]' to find all emails which contain selected fraze. 
- '-gbd' or '--group-by-domain' view emails grouped by one domain and organized alphabetically. 
- '-feil [path_to_logs_file]' or '--find-emails-not-in-logs [path_to_logs_file]' to show all email addresses that did not receive the email.[path_to_logs_file] is the path to the file which logs. 