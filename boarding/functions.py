import re

usernameRegex = re.compile("^[a-zA-Z0-9]{3,}$")
passwordRegex = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$")
emailRegex = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+")
nameRegex = re.compile("^[a-zA-Z]{1,}$")


def validate(type, data):

    if type == 'username':
        if re.match(usernameRegex, data) is None:
            return 'Username incorrect format, only letters, numbers and minimum 3 letters'
        else:
            return 'Pass'

    if type == 'password':
        if re.match(passwordRegex, data) is None:
            return 'Password incorrect format, minimum 6 characters, 1 letter, 1 number and 1 special character'
        else:
            return 'Pass'

    if type == 'name':
        if re.match(nameRegex, data) is None:
            return 'Firstname or Surname is in the incorrect format, minimum 1 letters'
        else:
            return 'Pass'

    if type == 'email':
        if re.match(emailRegex, data) is None:
            return 'Email incorrect format'
        else:
            return 'Pass'
