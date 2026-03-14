### Task 1 – `Write a function count_lines(file) that reads a file and returns the number of lines in it.`
- **File:** lines.txt

### Task 2 – `Write a function read_and_strip(file) that reads a file and returns a list of lines with leading and trailing whitespace removed.`
- **File:** whitespace.txt

### Task 3 – `Write a function read_non_empty_lines(file) that reads a file and returns a list of only the non-empty lines.`
- **File:** non_empty_lines.txt

### Task 4 – `Write a function read_uppercase(file) that reads a file and returns a list of lines converted to uppercase.`
- **File:** uppercase_source.txt

### Task 5 – `Write a function read_csv(file) that reads a CSV file and returns a list of lists, where each inner list represents a row split by commas.`
- **File:** sample.csv

### Task 6 – `Write a function word_count(file) that reads a file and returns the total number of words in the file.`
- **File:** words.txt

### Tasks 7–12 – Validators
- **File:** `validation_test_data.json`
- **Purpose:** Contains arrays of test strings for: emails, phones, PANs, passwords, vehicle numbers, and booking codes. Includes both valid and invalid examples. Use these to check exception handling for:
  - `InvalidEmailException
  - `InvalidPhoneNumberException
  - `InvalidPANException
  - `WeakPasswordException
  - `InvalidVehicleNumberException
  - `InvalidBookingCodeException

### Task 7 - `Write a function validate_email(email) that checks if the email is in a valid format (e.g., example@domain.com). If not, raise a custom InvalidEmailException.`

### Task 8 - `Write a function validate_phone(phone) that ensures the phone number is exactly 10 digits and starts with 7, 8, or 9. Raise InvalidPhoneNumberException if invalid.`

### Task 9 - `Write a function validate_pan(pan) that checks if the PAN number follows the format: 5 uppercase letters, 4 digits, and 1 uppercase letter (e.g., ABCDE1234F). Raise InvalidPANException if invalid.`

### Task 10 - `Write a function validate_password(password) that ensures the password has:`
`At least 8 characters`
`At least one uppercase letter`
`At least one lowercase letter`
`At least one digit`
`Raise WeakPasswordException if the password is weak.`

### Task 11 - `Write a function validate_vehicle_number(number) that checks if the number follows the format: KA01AB1234. Raise InvalidVehicleNumberException if invalid.`

### Task 12 - `Write a function validate_booking_code(code) that checks if the code starts with BOOK followed by exactly 4 digits. Raise InvalidBookingCodeException if invalid.`

### Tasks 13–17 – Date Utilities
- **File:** `date_task_samples.json`

### Task 13 - `Write a function format_date(date_obj) that takes a datetime.date object and returns a string in the format "YYYY-MM-DD".`

### Task 14 - `Write a function convert_ddmmyyyy(str_date) that takes a string in the format "DD/MM/YYYY" and returns a datetime.date object.`

### Task 15 - `Write a function is_valid_date(str_date) that checks if a string is a valid date in the format "YYYY-MM-DD". Return True if valid, otherwise False.`

### Task 16 - `Write a function calculate_age(birthdate_str) that takes a birthdate string in "YYYY-MM-DD" format and returns the age in years.`

### Task 17 - `Write a function reformat_date(str_date) that takes a date string in "YYYY-MM-DD" format and returns it in "Month Day, Year" format (e.g., "2025-06-13" → "June 13, 2025").`

## Suggested Quick Tests
- **Task 1:** Expect `5` lines in `lines.txt`.
- **Task 3:** Expect returned list to be `["Alpha", "Bravo", "Charlie", "Delta"]`.
- **Task 5:** Expect first row (header) `['id','name','email','phone']` and 3 data rows.
- **Task 11:** Only `KA01AB1234` is a strict match for the exact pattern; `DL04CD5678` is present as an *edge* example.

## Notes
- All files are UTF-8 encoded.
- Paths are relative; import and open from `requirements_dummy_data/`.
- You can freely add or edit rows/lines as needed during development.
