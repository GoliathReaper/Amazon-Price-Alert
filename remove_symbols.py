import re


def clean_number_string(input_string):
    # Remove all non-digit characters and spaces
    cleaned_string = re.sub(r'[^0-9]', '', input_string)
    return int(cleaned_string)
