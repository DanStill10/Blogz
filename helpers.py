def check_length(nput):
    length = len(nput)
    return length
    #check if input == less than three characters, or more than twenty.

def check_spaces(nput):
    for i in nput:
        if i == " ":
            return "error"
def user_name_check(user_name):
    if check_spaces(user_name) == "error":
        return "Username must not contain spaces!"
    if check_length(user_name) < 3 or check_length(user_name) > 20:
        return "Username must be between 3 and 20 characters!"
    return ""
def password_check(password):
    if check_spaces(password) == "error":
        return "Password must not contain spaces!"
    if check_length(password) < 3 or check_length(password) > 20:
        return "Password must be between 3 and 20 characters!"
    return ""
def confirm_password_check(confirm_password,password):
    if confirm_password != password:
        return "Both passwords do not match!"
    return ""  
    #compare both passwords
def field_empty(field):
    if field == "":
        return True
    return False 
