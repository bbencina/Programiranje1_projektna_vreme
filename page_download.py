import requests
import os

#CONSTANTS AND TEMPLATES

#format function parametres in _template variables 0 - YEAR, 1 - MONTH (1-12), 2 - DAY (1-31)
page_url_template = r"https://www.wunderground.com/history/airport/LJLJ/{0}/{1}/{2}/DailyHistory.html?req_city=Ljubljana&req_statename=Slovenia"
data_directory = "temp_data"
page_filename_template = "weather_{0}_{1}_{2}.html"

MONTHS = [(1, 31), (2, 28), (3, 31), (4, 30),
            (5, 31), (6, 30), (7, 31), (8, 31),
            (9, 30), (10, 31), (11, 30), (12, 31)]
YEARS = [2013, 2014, 2015, 2016, 2017]

#FUNCTIONS

def download_url_to_string(url):
    '''This function takes a URL as argument and tries to download it
    using requests. Upon success, it returns the page contents as string.'''
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException:
        print('Failed to connect to url ' + url)
        return None
    return r.text


def save_string_to_file(text, directory, filename):
    '''Write "text" to the file "filename" located in directory "directory",
    creating "directory" if necessary. If "directory" is the empty string, use
    the current directory.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as file_out:
        file_out.write(text)
    return None


def download_page_to_file(url, directory, filename):
    '''This functions tries to download a page with "url" and upon success,
    writes the page string to file "filename" at "directory".'''
    content = download_url_to_string(url)
    if content:
        save_string_to_file(content, directory, filename)
    return None

#PROGRAM

for year in YEARS:
    for (month, max_days) in MONTHS:
        for day in range(1, max_days + 1):
            page_url = page_url_template.format(year, month, day)
            page_filename = page_filename_template.format(year, month, day)
            download_page_to_file(page_url, data_directory, page_filename)
            print("Downloaded: {0}.".format(page_filename))

            #taking care of 2016 leap year
            if year == 2016 and month == 2 and day == 28:
                page_url = page_url_template.format(year, month, day + 1)
                page_filename = page_filename_template.format(year, month, day + 1)
                download_page_to_file(page_url, data_directory, page_filename)
                print("Downloaded: {0}.".format(page_filename))
