1. **Title and Description**:

This django Project about online slot booking of class,It consist 3 table custom user model, available timme and reservation, we used JWT token for the authentication also  using DJANGO Rest API end Point you can easily book your class.

## Features

- User registration and login
- JWT authentication
- List and create available time slots
- Slot -Reservation system
- List of Reserve Students

## Requirements

- Python 3.7+
- Django 3.0+
- djangorestframework
- djangorestframework-simplejwt


## Installation

### Clone the repository

git clone https://github.com/online_class_book.git

## Create VirtualENV
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

## Install Dependencies

pip install -r requirements.txt

## Fr running test case 
    python manage.py test

##  ----------------------------API Endpoints-------------------------


1. User Registration:

    URL: /api/users/register/
    Method: POST

    PAYLOAD:JSON
    {
    "first_name":"stu1",
    "last_name":"stu1",
    "role": "student",
    "phone": "1234567898",
    "age": 20,
    "email": "stu1@example.com",
    "subject":"history",
    "password":"Stu1@1234"
}

2. User Login:

    URL: /api/users/login/
    Method: POST

    PAYLOAD:JSON
    {
    "email":"stu1@example.com",
    "password":"Stu1@1234"
    }
    

3. Setting-Available-Time :

    URL: /api/users/available-times/
    Method: POST
    Headers: Authorization: Bearer <token>
    PAYLOAD:JSON

    {
    "start_time": "2024-06-02T11:00:00Z",
    "end_time": "2024-06-02T17:00:00Z",
    "teacher":2
}

4. Create Reservation of slot

    URL: /api/users/reserve-slot/
    Method: POST
    Headers: Authorization: Bearer <token>
    Payload:JSON

    {
  "reserved_starttime": "2024-06-02T12:00:00Z",
  "reserved_endtime": "2024-06-02T13:00:00Z",
  "student": 5,
  "available_time": 1 
}

5.  Reserve Students

    URL: /api/users/reserve-student/
    Method: GET
    Headers: Authorization: Bearer <token>
    Payload:JSON


