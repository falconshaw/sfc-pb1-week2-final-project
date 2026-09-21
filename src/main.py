"""
Week 2 Final Project - Starter Code
Console Application Template

This is a basic structure to get you started. Modify it for your project!
"""
import io
import csv
import sys
from typing import cast
import argparse
import cadet_data_manager as rf


def prepare_files(ussf_cadets_ssn, filtered_accessions_tracker, ussf_cadets, cadet_loss):
    active_cadet_data = rf.join_different_data(ussf_cadets_ssn, filtered_accessions_tracker, foreign_key='SSN')
    loss_cadet_data = rf.join_different_data(cadet_loss, filtered_accessions_tracker, foreign_key= 'SSN')
    accessions_data = rf.join_similar_data(active_cadet_data, loss_cadet_data)
    full_ussf_cadet_data = rf.join_different_data(accessions_data, ussf_cadets, foreign_key='Cadet ID')
    return full_ussf_cadet_data


def get_headers(accession_header, ussf_cadet_ssn_header, ussf_cadets_header, cadet_loss):
    headers = rf.get_unique_values(accession_header, ussf_cadet_ssn_header, ussf_cadets_header, cadet_loss)
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
        requested_det = input("For which Detachment do you want to view cadet data (001-940): \n")
        requested_det_data = rf.filter_by_field(full_ussf_cadet_data, 'Detachment', requested_det)
        print(f"There are {len(requested_det_data)} USSF cadets from Det {requested_det} in the Accessions Tracker: \n")
        for item in requested_det_data:
            print(f"Cadet ID: {item['Cadet ID']}, Name: {item['FirstName']} {item['LastName']} \n")
    elif choice == "2":
        print("You chose option 2!")
        # TODO: Call your function here
        cadet_id = input("Enter the cadet's Cadet_ID: \n")
        cadet_records = rf.find_record_by_id(full_ussf_cadet_data, 'Cadet ID', cadet_id)
        cadet_data = next(iter(cadet_records), None)
        if cadet_data is None:
            print(f"No cadet found with Cadet ID {cadet_id}.")
        else:
            print(f"Cadet {cadet_data['FirstName']} {cadet_data['LastName']}'s email address is {cadet_data['email']}")

    elif choice == "3":
        print("You chose option 3!")
        # TODO: Call your function here
        cadet_id = input("Enter the cadet's Cadet ID: \n")
        cadet_records = rf.find_record_by_id(full_ussf_cadet_data, 'Cadet ID', cadet_id)
        cadet_data = next(iter(cadet_records), None)
        if cadet_data is None:
            print(f"No cadet found with Cadet ID {cadet_id}.")
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


def main(full_ussf_cadet_data, headers):
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
    parser = argparse.ArgumentParser(description="Process multiple files.")
    parser.add_argument('-i', '--inputs', nargs= 4, required = True)
    args = parser.parse_args()
    accessions_tracker, accession_header = rf.read_csv_file(args.inputs[0])
    ussf_cadets_ssn, ussf_cadets_ssn_header = rf.read_csv_file(args.inputs[1])
    ussf_cadets, ussf_cadets_header = rf.read_csv_file(args.inputs[2])
    cadet_loss, cadet_loss_header = rf.read_csv_file(args.inputs[3])
    filtered_accessions_tracker = rf.filter_by_field(accessions_tracker, 'Branch', 'USSF')
    full_ussf_cadet_data = prepare_files(ussf_cadets_ssn, filtered_accessions_tracker, ussf_cadets, cadet_loss)
    headers = get_headers(accession_header, ussf_cadets_ssn_header, ussf_cadets_header, cadet_loss_header)
    main(full_ussf_cadet_data, headers)
