import csv
import io

def read_csv_file(filepath):
    """
    Reads a CSV file and returns the data as a list of dictionaries.
    """
    with io.open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        return list(reader), fieldnames

def join_data(primary_list, secondary_list, primary_key, foreign_key):
    """
    Joins two datasets together based on matching key fields.
    Similar to a SQL JOIN.
    """
    secondary_list_map = {secondary[foreign_key]: secondary for secondary in secondary_list}
    joined_data = []
    for primary in primary_list:
        key = primary[foreign_key]
        if key in secondary_list_map:
            merged_record = primary.copy()
            merged_record.update(secondary_list_map[key])
            joined_data.append(merged_record)
    return joined_data

def filter_by_field(data_list, field_name, field_value):
    """Filters records where a specific field matches a given value."""
    filtered_list = [item for item in data_list if item[field_name] == field_value]
    return filtered_list

def find_record_by_id(data_list, id_field, id_value):
    """Finds a specific record by its ID field."""
    record = [item for item in data_list if item[id_field] == id_value]
    return record


def get_unique_values(data_list_1, data_list_2, data_list_3):
    """Gets all unique values for a specific field in the dataset."""
    two_lists = list(dict.fromkeys(data_list_1 + data_list_2))
    all_lists = list(dict.fromkeys(two_lists + data_list_3))
    return all_lists


def write_report_to_file(content, fieldnames):
    """Writes a text report to a file."""
    with io.open('test/merged_accession_tracker.csv', "w", newline= '', encoding= 'utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(content)
