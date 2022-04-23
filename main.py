# Simple user validation using Pastebin by joshuagress/joda12345

# Installs:
# pip install pbwrap
# pip install key_generator

from os.path import exists
import os
from key_generator.key_generator import generate
import random
import subprocess
from pbwrap import Pastebin
import re
import sys


# setup of pastebin
# everyone gets an api dev key upon creating a pastebin account
API_DEV_KEY = ""
p = Pastebin(api_dev_key=API_DEV_KEY)
USERNAME = ""
PASSWORD = ""
p.authenticate(username=USERNAME, password=PASSWORD)
# ALL_HWID will hold the id of the private pastebin containing all the HWIDs. e.g. https://pastebin.com/id_of_paste
# check out pbwrap docs for more information on Pastebin methods
ALL_HWID = ""
HWID_RAW = p.get_user_raw_paste(ALL_HWID)


# with this we generate a random serial key
# check out key_generator docs for more information on their methods
def generate_random_serial_key():
    serial_key = generate(seed=random.randint(1, 500), num_of_atom=5, separator="-", min_atom_len=5, max_atom_len=5).get_key()
    return serial_key


# with this function we get the HWID of the user
def get_user_id():
    cmd = "wmic csproduct get uuid"
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    return uuid


# with this function we handle sending the users HWID to our pastebin
# a new private paste name NEW HWID will show up on your pastebin. You'll have to manually add the new HWID to your main HWID storage paste. 
def pastebin():
    try:
        if get_user_id() != "your_own_hwid":
            p.create_paste(api_paste_code=get_user_id(), api_paste_name="NEW HWID", api_paste_private=2)
    except Exception:
        input("Error! Please contact me at ####")


# here we can create a new user incase the HWID matches yours aka the admins.
# we store the new unique serial key in unique_serial_key.txt and overwrite this file every time we create a new user
# we also got a file called all_serial_keys which we append all created users to
# we keep generating new serial keys while serial key already exists
# when distributing your app you will have to include the unique_serial_key.txt in the same folder as your .exe
def create_new_user():
    if get_user_id() == "your_own_hwid":
        serial_key = generate_random_serial_key()
        admin_input = input("ADMIN: Generate new user? (Y/N):> ")
        if admin_input.lower() == "y":
            new_user_name = input("ADMIN: Enter the name of the new user >:")
            with open("unique_serial_key.txt", "w") as usk:
                with open("all_serial_keys.txt", "a") as sk:
                    try:
                        while serial_key in sk.read():
                            serial_key = generate_random_serial_key()
                    except Exception:
                        pass
                    sk.write(f"\n{new_user_name} : {serial_key}")
                usk.write(f"{new_user_name} : {serial_key}")
            return input("New user created!")
        else:
            return


# with this function we check whether the serial key generated by generate_random_serial_key
# matches the user input. We also use regex so we can check whether the user input matches our regex format
# after this was successful we run the pastebin method to get the HWID
# removing the unique_serial_key.txt so this if condition never gets met again
#
# so after the user entered the serial key once
# we use their HWID in the future to login which we store on a private pastebin
def check_serial_key():
    if get_user_id() != "your_own_hwid" and exists("unique_serial_key.txt"):
        try:
            serial_key = input("Enter your serial key >: ")
            with open("unique_serial_key.txt", "r") as sk:
                # . means any character, {5} the number of occurences, ^ start of regex, $ end of regex
                rex = re.compile("^.{5}-.{5}-.{5}-.{5}-.{5}$")
                user_serial_key = sk.read()
            if serial_key in user_serial_key and rex.match(serial_key):
                pastebin()
                os.remove("unique_serial_key.txt")
                return input("Welcome!")
            else:
                input("Wrong key!")
                sys.exit()
        except Exception as e:
            input(e)
            sys.exit()

    else:
        pass

    if get_user_id() != "your_own_hwid":
        if get_user_id() in HWID_RAW:
            return input("Logged in! Welcome")
        else:
            input("Error! Closing program..")
            sys.exit()


def main():
    create_new_user()
    check_serial_key()

if __name__ == '__main__':
    main()
