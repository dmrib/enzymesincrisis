from bs4 import BeautifulSoup
import glob2
import os
import collections
import json


def create_pages_list():
    ''' Creates a list containing all pages paths excluding indexes.

    Args:
        None.
    Returns:
        List of pages paths.
    '''

    pages_paths = []
    all_pages = glob2.glob('../data/www.chem.qmul.ac.uk/iubmb/enzyme/**/'
                           '*.html')
    for page in all_pages:
        if not page.endswith('index.html'):
            pages_paths.append(page)

    return pages_paths

def scrape_pages():
    ''' Scrapes data source for relevant data.

    Args:
        None.
    Returns:
        List of tuples pairing protein name(0) and history(1).
    '''

    data = []
    pages = create_pages_list()
    for page in pages:
        data.append(scrape_page(page))
    return data

def scrape_page(path):
    ''' Scrapes a IUBMB enzyme page and gets her name and history.

    Args:
        path (str): The page file path.
    Returns:
        Tuple containing the enzyme name(0) and history(1).
    '''

    soup = load_page(path)
    name = soup.find_all('title')[0].get_text()
    centered = soup.find_all('center')[1].get_text()
    return (name, centered)


def load_page(path):
    ''' Loads a page in a BeautifulSoup object.

    Args:
        path (str): Absolute path for page.
    Returns:
        A BeautifulSoup object.
    '''

    with open(path) as file:
        return BeautifulSoup(file, 'html.parser')

def create_parsed_data_file(data):
    ''' Creates csv-like file containing parsed data.

    Args:
        data (tuple): Tuple containing protein name(0) and history(1).
    Returns:
        None.
    '''

    with open('../data/parsed_data.csv', mode='w', encoding='utf-8') as file:
        for data_point in data:
            file.write(data_point[0] + ', ' + data_point[1] + '\n')

def create_json_data_file(data):
    ''' Creates json-like file containing parsed data.

    Args:
        data (dict): Ordered Dictionary with enzyme name as key and tuple of
                        events[0]/year[1] as value.
    Returns:
        None.
    '''
    ec_list = []
    for item in data:
        colors = ["red","black", "blue", "yellow", "purple", "gray", "green", "white"]
        ec_dict = collections.OrderedDict()
        ec_dict["measure"] = item
        ec_dict["interval_s"] = 60*60*24*365
        ec_dict["categories"] = {}
        ec_dict["data"] = []
        for index, event in enumerate(data[item]):
            #print('   ' + event[0] + '  ' + event[1])
            ec_dict["categories"][str(index) + ' - ' + event[0]] = {"color" : colors[index]}
            ec_dict["data"].append([event[1]+"-01-01", event[0] + '  ' + event[1]])
        ec_list.append(ec_dict)
    with open('../enzymes/static/parsed_json.json', mode='w', encoding='utf-8') as file:
        json.dump(ec_list, file, indent=4)

def load_from_parsed():
    ''' Loads data from an already pre processed source file.

    Args:
        None.
    Returns:
        List of tuples pairing protein name(0) and history(1).
    '''

    with open('../data/parsed_data.csv', mode='r', encoding='utf-8') as source:
        data = []
        for line in source:
            data_point = line.rstrip('\n').split(',', 1)
            data.append(tuple(data_point))
    return data

def create_events_file(dataset):
    ''' Create events file from dataset list.

    Args:
        dataset (list): List pairing enzyme name and her history.
    Returns:
        None.
    '''

    with open('../data/events.csv', mode='w', encoding='utf-8') as events_file:
        for datum in dataset:
            history = datum[1].split(' ')
            for position, word in enumerate(history):
                if word.endswith('ed'):
                    events_file.write(datum[0] + ' '
                                      + word + ' '
                                      + history[position+1][:-1]
                                      + '\n')

def load_events():
    ''' Read events file and returns in proper format.

    Args:
        None.
    Returns:
        entries (dict): Ordered Dictionary with enzyme name as key and tuple of
                        events[0]/year[1] as value.
    '''

    entries = collections.OrderedDict()
    with open('../data/events.csv', mode='r', encoding='utf-8') as events_file:
        for entry in events_file:
            ignore, enzyme, event, year = entry.split()
            if enzyme not in entries:
                entries[enzyme] = []
                entries[enzyme].append((event, year))
            else:
                entries[enzyme].append((event, year))

    return entries



if __name__ == '__main__':
    data = load_from_parsed()
    create_events_file(data)
    data = load_events()
    # for item in data:
    #     print(item + ':')
    #     for event in data[item]:
    #         print('   ' + event[0] + '  ' + event[1])
    #     print('\n')
    create_json_data_file(data)
