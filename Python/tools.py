#!/usr/bin/python3
# By Pytel

import os
import sys
import csv
import json


def clear():
    """ Clear console """
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    #os.system('cls' if os.name == 'nt' else 'clear')


def printf(format: str, *args):
    """ Print to console 

    Use the same syntax as in C printf function.

    Args:
        format : format string
        *args : arguments
    """
    sys.stdout.write(format % args)


def unique(array) -> list:
    """ Return unique values from array """
    return list(set(array))


def flatten(l) -> list:
    """ Flatten list """
    return [item for sublist in l for item in sublist]


def sort_by_columm(array, columm: int = 0, reverse: bool = False):
    """ Sort array by columm

    Args:
        array : array to sort
        columm : columm to sort by
        reverse : reverse order

    Returns:
        sorted array
    """
    return (sorted(array, key=lambda x: x[columm], reverse=reverse))


def append_to_json(filepath, data: dict, indent: int = 4):
    """
    Append data in JSON format to the end of a JSON file.
    NOTE: Assumes file contains a JSON object (like a Python
    dict) ending in '}'. 

    Args:
        filepath : path to file
        data : dict to append
        indent_ : indent
    """

    # construct JSON fragment as new file ending
    new_ending = ", " + json.dumps(data, indent=indent)[1:-1] + "}\n"

    # edit the file in situ - first open it in read/write mode
    with open(filepath, 'r+') as f:

        f.seek(0, 2)        # move to end of file
        index = f.tell()    # find index of last byte

        # walking back from the end of file, find the index
        # of the original JSON's closing '}'
        while not f.read().startswith('}'):
            index -= 1
            if index == 0:
                raise ValueError(
                    "can't find JSON object in {!r}".format(filepath))
            f.seek(index)

        # starting at the original ending } position, write out
        # the new ending
        f.seek(index)
        f.write(new_ending)


def save_to_json(file_name, data: dict, indent: int = 4, append: bool = False):
    if os.path.isfile(file_name) and append:
        append_to_json(file_name, data, indent=indent)
    else:
        with open(file_name, "w") as outfile:
            json_object = json.dumps(data, indent=indent)
            outfile.write(json_object)


def load_dic_from_json(file_path) -> dict:
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def load_dic_from_csv(file_path) -> dict:
    with open(file_path, 'r') as csv_file:
        data = csv.DictReader(csv_file)
    return data


def load_dic_from_file(file_path) -> dict:
    """ Load dictionary from file
    
    Args:
        file_path : path to file
        
    Returns:
        dictionary : loaded dictionary from file
    
    Raises:
        Exception: unknown file format
        
    ### Usage:
    Supported file formats:
    - json
    - csv
    """
    file_format = file_path.split('.')[-1]
    if not os.path.isfile(file_path):
        return None
    if file_format == "json":
        return load_dic_from_json(file_path)
    if file_format == "csv":
        return load_dic_from_csv(file_path)
    else:
        raise Exception("ERROR: unknown file format!")


def append_to_file(file_path, text : str):
    with open(file_path, "a") as file:
        file.write(text + "\n")

# END
