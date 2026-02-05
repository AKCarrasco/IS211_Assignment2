"""Aaron Carrasco Assignment 2"""

import argparse
import csv
import urllib.request
import logging
import datetime

def downloadData(url):
    """Downloads the data"""
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")

def processData(file_content):
    data_dict= {}
    logger= logging.getLogger('assignment2')
    csv_reader = csv.reader(file_content.splitlines())

    for linenum, row in enumerate(csv_reader, start=1):
        person_id, name, birthday = row
        try:
            birthday = datetime.datetime.strptime(birthday, '%m/%d/%Y').date()
            data_dict[int(person_id)] = (name, birthday)
        except ValueError:
            logger.error(f"Error reading line #{linenum} for ID #{person_id}")

    return data_dict

def displayPerson(id, personData):
    """Display the person data"""
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id}: is {name} with a birthday of {birthday}")
    else:
        print("ID not found")

def setuplogger():
    logging.basicConfig(filename='error.log', level=logging.ERROR)

def main(url):
    print(f"Running main with URL = {url}...")
    setuplogger()

    try:
        csv_data = downloadData(url)
    except urllib.error.URLError as e:
        print(f"Error downloading data from {url}: {e.reason}")
        return

    person_data = processData(csv_data)

    while True:
        try:
            user_input = int(input("Enter a person ID to display (0 to quit): "))
            if user_input == 0:
                break
            displayPerson(user_input, person_data)
        except ValueError:
            print("Please enter a valid ID")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
