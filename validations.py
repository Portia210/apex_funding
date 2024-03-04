def month_year_validation(input_text, correct_values_list):
    ''' this function will take value and create a loop to make sure it's correct'''
    while True:
        entered_value = input(input_text).strip()
        if all(char.isdigit() for char in entered_value):
            if int(entered_value) in correct_values_list:
                return entered_value
            else:
                print("The Value is not correct, enter again")
        else:
            print("please enter only digits")
        print("----------------------------------------------")


def string_or_space_validation(input_text):
    while True:
        entered_value = input(input_text)
        if all(char.isalpha() or char.isspace() for char in entered_value):
            if any(char.isalpha() for char in entered_value):
                return entered_value
            else:
                print("please enter at least one letter")
        else:
            print("Only Letters or spaces please")
        print("----------------------------------------------")


def number_with_length_validation(input_text, optional_length_list):
    while True:
        entered_value = input(input_text).strip()
        if all(char.isdigit() for char in entered_value):
            if len(entered_value) in optional_length_list:
                return entered_value
            else:
                print(f"length {len(entered_value)} is not acceptable")
        else:
            print("please enter only digits")
        print("----------------------------------------------")



def get_cc_details():
    first_name = string_or_space_validation("Enter your first name: ")
    print("---------------------------------------")
    last_name = string_or_space_validation("Enter your last name: ")
    print("---------------------------------------")
    print("credit card month ")
    credit_card_month = month_year_validation("number between 1 to 12: ", list(range(1, 13)))
    print("---------------------------------------")
    print("credit card year")
    credit_card_year = month_year_validation("between 2024 to 2039: ", list(range(2024, 2040)))
    print("---------------------------------------")
    print("Enter your credit card number")
    credit_card_number = number_with_length_validation("number of 14-16 digits: ", [14, 15, 16])
    print("---------------------------------------")
    print("Enter your CVV")
    cvv_number = number_with_length_validation("number of 3-4 digits: ", [3, 5])
    print("---------------------------------------")

    return {
        "first_name": first_name,
        "last_name": last_name,
        "credit_card_month": credit_card_month,
        "credit_card_year": credit_card_year,
        "credit_card_number": credit_card_number,
        "cvv_number": cvv_number
    }