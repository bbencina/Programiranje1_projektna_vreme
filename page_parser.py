import os
import re
import csv

#CONSTANTS AND TEMPLATES

#format function parametres in _template variables 0 - YEAR, 1 - MONTH (1-12), 2 - DAY (1-31)
page_url_template = r"https://www.wunderground.com/history/airport/LJLJ/{0}/{1}/{2}/DailyHistory.html?req_city=Ljubljana&req_statename=Slovenia"
data_directory = "temp_data"
page_filename_template = "weather_{0}_{1}_{2}.html"
csv_filename = "weather.csv"
csv_data_directory = 'csv_data2'

column_names = ['date', 'mean_temp', 'max_temp', 'min_temp',
                'dew_point', 'avg_humidity', 'max_humidity',
                'min_humidity', 'precipitation', 'sea_level_pressure',
                'wind_speed', 'max_wind_speed', 'visibility']

MONTHS = [(1, 31), (2, 28), (3, 31), (4, 30),
            (5, 31), (6, 30), (7, 31), (8, 31),
            (9, 30), (10, 31), (11, 30), (12, 31)]
YEARS = [2013, 2014, 2015, 2016, 2017]

#FUNCTIONS

def read_file_to_string(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.
    '''
    path = os.path.join(directory, filename)
    with open(path, 'r') as file_in:
        return file_in.read()

def extract_info_from_page(page_str):
    '''Takes in a string of html. Uses regexes to extract pieces
    of weather information.
    Returns a dictionary.
    '''

    #REGEX STRINGS ::DONE

    regex_meantemp = r'<span>Mean Temperature</span></td>.*?class="wx-value">(?P<mean_temp>.*?)</span>'
    regex_maxtemp = r'<span>Max Temperature</span></td>.*?class="wx-value">(?P<max_temp>.*?)</span>'
    regex_mintemp = r'<span>Min Temperature</span></td>.*?class="wx-value">(?P<min_temp>.*?)</span>'

    regex_dewpoint = r'<span>Dew Point</span></td>.*?class="wx-value">(?P<dew_point>.*?)</span>'
    regex_avghum = r'<span>Average Humidity</span>.*?<td>(?P<avg_humidity>.*?)</td>'
    regex_maxhum = r'<span>Maximum Humidity</span>.*?<td>(?P<max_humidity>.*?)</td>'
    regex_minhum = r'<span>Minimum Humidity</span>.*?<td>(?P<min_humidity>.*?)</td>'

    regex_prec = r'<span>Precipitation</span></td>.*?class="wx-value">(?P<precipitation>.*?)</span>'

    regex_slp = r'<span>Sea Level Pressure</span></td>.*?class="wx-value">(?P<sea_level_pressure>.*?)</span>'

    regex_ws = r'<span>Wind Speed</span></td>.*?class="wx-value">(?P<wind_speed>.*?)</span>'
    regex_maxws = r'<span>Max Wind Speed</span></td>.*?class="wx-value">(?P<max_wind_speed>.*?)</span>'
    #regex_maxgustspeed
    regex_vis = r'<span>Visibility</span></td>.*?class="wx-value">(?P<visibility>.*?)</span>'

    #regex_events = r'<span>Events</span>.*?<td>(?P<events>.*?)</td>'

    info = {}

    rx = re.compile(regex_meantemp + r'.*?' + regex_maxtemp + r'.*?' +
                    regex_mintemp + r'.*?' + regex_dewpoint + r'.*?' +
                    regex_avghum + r'.*?' + regex_maxhum + r'.*?' +
                    regex_minhum + r'.*?' + regex_prec + r'.*?' +
                    regex_slp + r'.*?' + regex_ws + r'.*?' +
                    regex_maxws, re.DOTALL)

    match = rx.search(page_str)
#if match:
#    print('Done')
#else:
#    print('None')
    info = match.groupdict()

    rx_vis = re.compile(regex_vis, re.DOTALL)
    m_vis = rx_vis.search(page_str)
    if m_vis:
        info['visibility'] = m_vis.group('visibility')
    else:
        info['visibility'] = 'n/a'

    return info

def file_to_list(filename, w_list):
    page_str = read_file_to_string('temp_data', filename)
    w_dict = extract_info_from_page(page_str)

    f, _ = filename.split('.')
    f_list = f.split('_')
    if len(f_list[2]) == 1:
        f_list[2] = '0' + f_list[2]
    if len(f_list[3]) == 1:
        f_list[3] = '0' + f_list[3]

    w_dict['date'] = f_list[1] + '-' + f_list[2] + '-' + f_list[3]

    w_list.append(w_dict)
    return None



def write_csv(fieldnames, rows, directory, filename):
    '''Write a CSV file to directory/filename. The fieldnames must be a list of
    strings, the rows a list of dictionaries each mapping a fieldname to a
    cell-value.
    '''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

def dictlist_to_csv(weather_list):
    '''Function takes a list of dictionaries and creates a csv file containing
    information from these dictionaries.
    '''
    write_csv(column_names, weather_list, csv_data_directory, csv_filename)
    return None
 #TODO


#PROGRAM
directory = os.fsencode(data_directory)
weather_list = []

for f in os.listdir(directory):
    filename = os.fsdecode(f)
    try:
        file_to_list(filename, weather_list)
    except:
        print('Error: ' + filename)

dictlist_to_csv(weather_list)
#REGEX MATCH ERROR TESTER
'''directory = os.fsencode(data_directory)
errors = []

for f in os.listdir(directory):
    filename = os.fsdecode(f)
    try:
        a = read_file_to_string('temp_data', filename)
        b = extract_info_from_page(a)
        print('Done')
    except:
        errors.append(filename)
print(len(errors), errors)
'''
