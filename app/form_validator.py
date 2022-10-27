import re
from flask import flash

def validate_name(firstname, minlen):
#Checks if the received firstname matches the required conditions.
    if type(firstname) != str:
        return False
    if minlen < 1:
        return False

    # firstnames can't be shorter than minlen
    if len(firstname) < minlen:
        return False
    # firstnames can only use letters, numbers, dots and underscores
    if not re.match("^[A-Za-z0-9_-]*$", firstname):
        return False
    # firstnames can't begin with a number
    if firstname[0].isnumeric():
        return False
    return True
def validateSpace(firstname):
     if not re.match("^[A-Za-z0-9_ -]*$", firstname):
        return False
# def validate_street(street):
#     #validate street
#     street_address_validate_pattern = "^(\\d{1,}) [a-zA-Z0-9\\s]+(\\,)? [a-zA-Z]+(\\,)? [A-Z]{2} [0-9]{5,6}$"
#     if not re.match(street_address_validate_pattern,street):
#         return False