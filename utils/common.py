import utils.date as date_utils


def get_sentence_case(input_string):
    """
    Converts a given string to sentence case.

    This function takes an input string and capitalizes the first letter of each word, transforming the entire string into sentence case. If the input string is empty, it returns an empty string.

    Parameters:
    - input_string (str): The string to be converted to sentence case.

    Returns:
    - str: A string converted to sentence case. If the input string is empty, returns an empty string.
    """
    # Check if the input_string is not empty
    if not input_string:
        return ""
    # Split the input string into words, capitalize each word, then join them back
    return " ".join(word.capitalize() for word in input_string.split())


def modify_assignee(assignee_name):
    """
    Modifies an assignee's name to a standardized format if it exists in a predefined list of names.

    This function takes an assignee's name as input and checks it against a predefined dictionary of names that require modification to a standardized format (usually for consistency or to meet certain data format requirements). If the assignee's name is found in the dictionary, it is replaced with the modified name. If the assignee's name is not in the dictionary, it is returned unchanged.

    Parameters:
    - assignee_name (str): The name of the assignee to be modified.

    Returns:
    - str: The modified name of the assignee if it exists in the predefined list; otherwise, returns the original name.
    """
    name_changes = {
        "Gupta Dipti": "Gupta, Dipti",
        "Siddiqui Aman": "Siddiqui, Aman",
        "Dilip Mohite Balaji": "Dilip Mohite, Balaji",
        "Shivanshu Joshi": "Joshi, Shivanshu",
        "Joshi Shivanshu": "Joshi, Shivanshu",
        "Joshi Kunal": "Joshi, Kunal",
        "Pujari Saroja": "Pujari, Saroja",
        "Sai Lakshmi Paritala": "Sai Lakshmi, Paritala",
        "Charu Mishra": "Mishra, Charu",
        "Husain Boltwala": "Boltwala, Husain",
        "Pooja S": "S, Pooja",
        "Indhu Ponnusamy": "Ponnusamy, Indhu",
        "Karambelkar Makarand": "Karambelkar, Makarand",
        "Nipane Sagar": "Nipane, Sagar",
        "Reddy Gaddam Nirnaya": "Reddy, Gaddam Nirnaya",
        "Sirisha Konduru": "Konduru, Sirisha",
        "Pulikanti Venkat Krishna": "Pulikanti, Venkat Krishna",
        "B S Anupama": "B S, Anupama",
        "Divya Pandey": "Pandey, Divya",
        "divypandey@deloitte.com": "Pandey, Divya",
        "Sufia Syeda": "Syeda, Sufia",
        "Kashyap Atul": "Kashyap, Atul",
        "Manisha Tiwari": "Tiwari, Manisha",
        "Sahebrao Salunkhe Anjali": "Sahebrao Salunkhe, Anjali",
        "Raviteja Aytha": "Aytha, Raviteja",
        "Mehraj Shaik Sameena": "Shaik, Mehraj Sameena",
        "KarthikR": "Karthik, R",
        "Pulkit Mathur": "Mathur, Pulkit",
        "Pandey Abhijeet": "Pandey, Abhijeet",
        "Jha Rajiv": "Jha, Rajiv Ranjan",
        "Rajiv Jha": "Jha, Rajiv Ranjan",
        "Rajiv Ranjan Jha": "Jha, Rajiv Ranjan",
        "Chadha Bhavya": "Chadha, Bhavya",
        "Rajiv Chugh": "Chugh, Rajiv",
        "Yadav Pragati": "Yadav, Pragati",
        "Suneja Vaibhav": "Suneja, Vaibhav",
        "Jain Jagrati": "Jain, Jagrati",
        "Vani Konda": "Konda, Vani",
        "Preethi Bheemreddy": "Bheemreddy, Preethi",
        "Rabin Ale": "Ale, Rabin",
        "Goel Shruti": "Goel, Shruti",
        "Shruti Goel": "Goel, Shruti",
        "Shruti": "Goel, Shruti",
        "Shruti, Goel": "Goel, Shruti",
        "Anmol Adhikari": "Adhikari, Anmol",
        "Addagalla Sumanth": "Addagalla, Sumanth",
        "SrivastavaPrakhar": "Srivastava, Prakhar",
        "Himanshu Joshi": "Joshi, Himanshu",
        "Poorna Rakesh Anagani": "Poorna Rakesh, Anagani",
        "Venkataswamy Budige": "Venkataswamy, Budige",
        "Tanvir Toor": "Toor, Tanvir",
        "Digambar Patil Himanshu": "Digambar Patil, Himanshu",
        "Singh Tirupati": "Singh, Tirupati",
        "Prathyusha Bindu Prathyusha": "Prathyusha, Bindu Prathyusha",
        "Sengar, Abhishek": "Sengar, Abhishek kumar",
        "Sengar Abhishek kumar": "Sengar, Abhishek kumar",
        "Hemant Kumar Kurdia": "Kurdia, Hemant Kumar",
        "SikarwarPrakhar": "Sikarwar, Prakhar",
        "Parag Pratim": "Baruah, Parag Pratim",
        "Vamsi Krishna Pentakota": "Pentakota, Vamsi Krishna",
        "viskhandelwal@deloitte.com": "Khandelwal, Vishal",
        "Javali Kiran urf Srinivas": "Javali, Kiran urf Srinivas",
        "SharmaNaman": "Sharma, Naman",
        "Madhurima Yalamanchili": "Yalamanchili, Madhurima",
        "Faysal Mazed": "Mazed, Faysal",
        "Shukla Harshit": "Shukla, Harshit",
        "Rajasekharcrajasekhar": "Rajasekhar, Chilakam",
        "Aravind Sreeram": "Sreeram, Aravind",
        "Abhilash Sadhale": "Sadhale, Abhilash Sudhakar",
        "Tanu Srivastava": "Srivastava, Tanu",
        "Pranav Vijay": "Vijay, Pranav",
        "Tim Golio": "Golio, Tim",
        "Nishant Parikh": "Parikh, Nishant",
        "Lakshay Kaura": "Kaura, Lakshay",
        "Rakib Ahmed": "Ahmed, Rakib",
        "Denis Moore": "Moore, Denis",
        "John Lang": "Lang, John",
        "Gururaj": "M, Gururaja",
        "Maurya Shivam": "Maurya, Shivam",
        "Ravi kiran": "N, Ravi Kiran",
        "Harshit Shukla": "Shukla, Harshit",
        "Chaturya Doddi": "Chaturya, Doddi",
        "Tirupati Singh": "Singh, Tirupati",
    }
    return name_changes.get(assignee_name, assignee_name)


def check_if_value_is_updated(value, current_value):
    """
    Checks if a given value is different from the current value, considering special handling for date values.

    This function determines whether the `value` (which can be of any type) differs from `current_value`. For date values (identified by the `is_date` function), it compares just the date parts (ignoring time and timezone) to see if they are different. For non-date values, it simply checks if `value` and `current_value` are not equal. The function also ensures that `value` is not empty or None before comparing.

    Parameters:
    - value (str, datetime.datetime, pandas.Timestamp, or any): The new value to check.
    - current_value (str, datetime.datetime, pandas.Timestamp, or any): The current value for comparison.

    Returns:
    - bool: True if `value` is considered updated (different from `current_value`); otherwise, False.
    """
    return (
        value != ""
        and value is not None
        and (
            (
                date_utils.is_date(value)
                and not date_utils.are_dates_equal(current_value, value)
            )
            or (not date_utils.is_date(value) and current_value != value)
        )
    )
