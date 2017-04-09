from bs4 import BeautifulSoup
import glob2
import os



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

def load_from_parsed(path):
    ''' Loads data from an already pre processed source file.

    Args:
        path (str): Path to source file.
    Returns:
        List of tuples pairing protein name(0) and history(1).
    '''

    with open(path) as source:
        data = []
        for line in source:
            data_point = line.rstrip('\n').split(',')
            data.append(tuple(data_point))
    print(data)
    return data

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


class Protein():
    ''' An IUBMB Enzyme nomenclature. '''

    def __init__(self, name, history):
        self.name = name
        self.history = history


if __name__ == '__main__':
    data = load_from_parsed(os.path.join(os.getcwd(), '../data/parsed_data.csv'))
