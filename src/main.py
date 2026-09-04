"""
Week 2 Final Project - Starter Code
Console Application Template

This is a basic structure to get you started. Modify it for your project!
"""
import io
import csv
from typing import cast
import cadet_data_manager as rf


def load_files():
    accessions_tracker, accession_header = rf.read_csv_file('data/accession_tracker_example.csv')
    ussf_cadets_ssn, ussf_cadets_ssn_header = rf.read_csv_file('data/ussf_cadets_ssn_example.csv')
    ussf_cadets, ussf_cadets_header = rf.read_csv_file('data/ussf_cadets_example.csv')
    return accessions_tracker, accession_header, ussf_cadets_ssn, ussf_cadets_ssn_header, ussf_cadets, ussf_cadets_header


def prepare_files(ussf_cadets_ssn, filtered_accessions_tracker, ussf_cadets):
    accessions_data = rf.join_data(ussf_cadets_ssn, filtered_accessions_tracker, primary_key='Cadet_ID', foreign_key='SSN')
    full_ussf_cadet_data = rf.join_data(accessions_data, ussf_cadets, primary_key='SSN', foreign_key='Cadet_ID')
    return full_ussf_cadet_data


def get_headers(accessions_tracker_header, ussf_cadet_ssn_header, ussf_cadets_header):
    headers = rf.get_unique_values(accession_header, ussf_cadets_ssn_header, ussf_cadets_header)
    return headers

def display_menu():
    """
    Show the main menu to the user.
    Customize this for your application.
    """
    print("\n" + "="*60)
    title = "AFROTC USSF Cadet Data Application"
    print(title.center(60))
    print("="*60)
    print("1. View Cadets by Detachment")
    print("2. Find Cadet Email")
    print("3. Find Cadet Phone Number")
    print("4. Print Full Accession Report")
    print("help - Show this menu")
    print("quit - Exit application")
    print()


def handle_choice(choice, full_ussf_cadet_data, headers):
    """
    Process the user's choice and call appropriate functions.

    Args:
        choice (str): The user's input

    Returns:
        bool: True to continue, False to exit
    """
    if choice == "1":
        print("You chose option 1!")
        # TODO: Call your function here
        requested_det = input("For which Detachment do you want to view cadet data: \n")
        requested_det_data = rf.filter_by_field(full_ussf_cadet_data, 'Det', requested_det)
        print(f"There are {len(requested_det_data)} USSF cadets from Det {requested_det} in the Accessions Tracker: \n")
        for item in requested_det_data:
            print(f"Cadet ID: {item['Cadet_ID']}, Name: {item['FirstName']} {item['LastName']} \n")
    elif choice == "2":
        print("You chose option 2!")
        # TODO: Call your function here
        cadet_id = input("Enter the cadet's Cadet_ID: \n")
        cadet_records = rf.find_record_by_id(full_ussf_cadet_data, 'Cadet_ID', cadet_id)
        cadet_data = next(iter(cadet_records), None)
        if cadet_data is None:
            print(f"No cadet found with Cadet_ID {cadet_id}.")
        else:
            print(f"Cadet {cadet_data['FirstName']} {cadet_data['LastName']}'s email address is {cadet_data['email']}")

    elif choice == "3":
        print("You chose option 3!")
        # TODO: Call your function here
        cadet_id = input("Enter the cadet's Cadet_ID: \n")
        cadet_records = rf.find_record_by_id(full_ussf_cadet_data, 'Cadet_ID', cadet_id)
        cadet_data = next(iter(cadet_records), None)
        if cadet_data is None:
            print(f"No cadet found with Cadet_ID {cadet_id}.")
        else:
            print(f"Cadet {cadet_data['FirstName']} {cadet_data['LastName']}'s phone number is {cadet_data['phone']}")

    elif choice == "4":
        rf.write_report_to_file(full_ussf_cadet_data, headers)
        print("The full Accession Report is saved in the test/ directory.")

    elif choice == "help":
        display_menu()

    elif choice == "quit":
        print("Thanks for using the application. Goodbye!")
        return False

    else:
        print(f"'{choice}' is not a valid option. Type 'help' to see available commands.")

    return True


def main(full_ussf_cadet_data):
    """
    Main application loop.
    Displays menu, gets user input, processes choices.
    """
    print("Welcome to AFROTC's OTC Inbound Tracker Application!")
    display_menu()

    running = True
    while running:
        choice = input("Enter your choice: ").strip().lower()
        running = handle_choice(choice, full_ussf_cadet_data, headers)


if __name__ == "__main__":
    accessions_tracker, accession_header, ussf_cadets_ssn, ussf_cadets_ssn_header, ussf_cadets, ussf_cadets_header = load_files()
    filtered_accessions_tracker = rf.filter_by_field(accessions_tracker, 'Branch', 'USSF')
    full_ussf_cadet_data = prepare_files(ussf_cadets_ssn, filtered_accessions_tracker, ussf_cadets)
    headers = get_headers(accession_header, ussf_cadets_ssn_header, ussf_cadets_header)
    main(full_ussf_cadet_data)

