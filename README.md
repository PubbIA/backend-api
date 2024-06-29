# PubAIAPI
![Visualization System](./docs/api-image.png)

## Description

PubAIAPI is a API for the PubAI project.

## Project Structure :
This project's directory structure is inspired by the article "[Structuring a FastAPI App: An In-Depth Guide](https://medium.com/@ketansomvanshi007/structuring-a-fastapi-app-an-in-depth-guide-cdec3b8f4710)" on Medium.

- **models** : The `models` directory holds the data models or schemas used by the application. It includes files for defining the application's models and their relationships. This also helps us to implement DTO(Data Transfer through Objects) pattern where we are exchanging data in between different layers through these model instances.
- **requirements** : Directory for requirements related files
- **scripts** : The `scripts` directory contains utility scripts for various purposes, such as setting up the database or generating data. It typically includes scripts like init_db.sql for initializing the database.
- **tests** : The `tests` directory contains unit tests to ensure the correctness of the application. It typically includes subdirectories for different components, such as service tests, and each test file corresponds to a specific component or module.
- **utils** : The `utils` directory houses utility modules and files required for the application's functionality. It typically includes files for handling exceptions, providing helper functions, and implementing common functionality such as JWT token handling and password hashing.
- **temp** : Directory for temporary files
- **templates** : Directory for HTML templates
- **env** :  Directory for envrenment variables



## Envirenment Variable :
### 1. `env/database.env` :
#### USER_NAME (ALL - {sqlite})
- **Description**: The username used to authenticate to the database.
- **Example**: `USER_NAME="root"`

#### PASSWORD (ALL - {sqlite})
- **Description**: The password used to authenticate to the database.
- **Example**: `PASSWORD="admin"`

#### PORT (ALL - {sqlite})
- **Description**: The port number on which the database server is listening.
- **Example**: `PORT="3306"`

#### HOST (ALL - {sqlite})
- **Description**: The hostname or IP address of the database server.
- **Example**: `HOST="localhost"`

#### DB_NAME (ALL - {sqlite})
- **Description**: The name of the database.
- **Example**: `DB_NAME="gpe-x-pubai"`

#### DB_TYPE (ALL)
- **Description**: The type of the database ['mysql','mariadb','postgresql','oracle','oracledb','mssql','sqlserver','sqlite'].
- **Example**: `DB_TYPE="mysql"`

#### SERVICE_NAME (Only for Oracle)
- **Description**: The service name or SID of the Oracle database. This parameter is used to identify the specific Oracle instance to connect to.
- **Example**: `SERVICE_NAME="ORCL"`


#### TABLESPACE_NAME (Only for Oracle)
- **Description**: Specifies the name of the tablespace where the data file will be stored.
- **Example**: `TABLESPACE_NAME="USERS"`

#### DATAFILE_SIZE (Only for Oracle)
- **Description**: Sets the initial size of the data file in the specified tablespace. It determines how much disk space is initially allocated for the data file.
- **Example**: `DATAFILE_SIZE="100M"`

#### DB_FILE_PATH (Only for Sqlite)
- **Description**: The file path for the SQLite database. This parameter is used when the database type is set to 'sqlite'.
- **Example**: `DB_FILE_PATH="/path/to/database.db"`

### 2. `env/secrets.env` :
#### FERNET_KEY
- **Description**: The key used for encryption and decryption with Fernet symmetric encryption.
- **Example**: `FERNET_KEY="Zsy6-8REWdN0-FkIhgBy8k19MJ7elYNAv3MxkWHFGOk="`
#### ALGORITHM
- **Description**: The algorithm used for JWT token encoding and decoding.
- **Example**: `ALGORITHM="HS256"`

#### ACCESS_TOKEN_EXPIRE_MINUTES
- **Description**: The duration (in minutes) after which JWT access tokens expire.
- **Example**: `ACCESS_TOKEN_EXPIRE_MINUTES=60`

#### JWT_SECRET_KEY
- **Description**: The secret key used for JWT token encoding and decoding.
- **Example**: `JWT_SECRET_KEY="abababababababbabhha"`


### 3. `env/communication.env` :
#### EMAIL_PROJECT
- **Description**: The password of project used for send emails for users.
- **Example**: `EMAIL_PROJECT="laamiri.laamiri@etu.uae.ac.ma"`

#### PASSWORD_EMAIL_PROJECT
- **Description**: The password of project used for send emails for users.
- **Example**: `PASSWORD_EMAIL_PROJECT="fyxx cazo wmyo mnfu"`



## Install requirements :
### create a virtual envirement (Optional)
```bash
# Create venv (optional)
$ python3 -m venv pubai
#activate pubai
$ source pubai/bin/activate
# for deactivate the pubai
(pubai)$ deactivate
```
### Instal requirements:
```bash
# Create venv (optional)
$ pip install -r requirements/dev.txt
```
## Running the app : 
```bash
# Run application
$ uvicorn main:app --host 127.0.0.1 --port 5000 --reload
```
## Build Docker image : 
```bash
# build a docker image
$ docker build -t pubai .
```
## Running the app in the Docker : 
```bash
# Run docker image
$ docker run -p you_port:5000 pubai
```



## Database Tables :

### Users : 

| Attribute       | Description                                         |
|-----------------|-----------------------------------------------------|
| id              | Unique identifier for the user.                     |
| username        | User's username.                                    |
| email           | User's email address (unique).                      |
| password_hash   | Hashed password for user authentication.            |
| phone_number    | User's phone number.                                |
| date            | Date of the account creation.                       |
| time            | Time of the account creation.                       |
| points          | The points of user                                  |
---




## API Endpoints

### Index Endpoint

- **URL**: `GET /api/`
- **Description**: Check if the server is running.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "I am working good !"
    }
    ```

### Sending Verification Code

- **URL**: `POST /api/email/send-verification-code`
- **Description**: Send a verification code to the provided email address.
- **Request Body**:
  - `to` (string): Recipient email address.
  - `language` (string, optional): Language of the email content (default: "fr").
  - `type_` (string, optional): The type of code : number,string,mixte (default: "number").
  - `length` (int, optional): The length of code sended (default: 4).
  
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "code": "verification-code"
    }
    ```

### User Management

- **URL**: `POST /api/users/`
- **Description**: Create a new user.
- **Request Body**:
  - `username` (string): User's username.
  - `email` (string): User's email address.
  - `password` (string): User's password.
  - `phone_number` (string): User's phone number.
\- **Password Constraint**:
  - Passwords must meet the following criteria:
    - Contains at least one lowercase character
    - Contains at least one uppercase character
    - Contains at least one digit
    - Has a minimum length of 8 characters
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "User created successfully"
    }
    ```

### User Login

- **URL**: `POST /api/users/login`
- **Description**: Authenticate a user and generate an access token.
- **Request Body**:
  - `email` (string): User's email address.
  - `password` (string): User's password.
- **Response**:
  - **Status Code**:
    - 200 OK: Successful authentication.
    - 401 Unauthorized: Invalid credentials.
  - **Response Body** (for 200 OK):
    ```json
    {
        "access_token": "your-access-token",
        "token_type": "bearer"
    }
    ```

### Check Email Existence

- **URL**: `POST /api/users/email-exist`
- **Description**: Check if an email exists.
- **Request Body**:
  - `email` (string): The email address to check.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "exist": true,
        "access_token":"xswhdhdjsdhhdjcbdhh3hd4h43ud23u33odj8339"
    }
    ```
    - `exist` (boolean): Indicates whether the email exists (`true`) or not (`false`).
    - `access_token` (string): Token for accessing the user account expired in 5 minutes.



### Changing Password

- **URL**: `PUT /api/users/change-password`
- **Description**: Change the password for a user.
- **Request Body**:
  - `new_password` (string): The new password for the user.
  - `access_token` (string): Token for accessing the user account.
- **Password Constraint**:
  - Passwords must meet the following criteria:
    - Contains at least one lowercase character
    - Contains at least one uppercase character
    - Contains at least one digit
    - Has a minimum length of 8 characters
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "Password changed successfully"
    }
    ```

  

### Add Points to User

- **URL**: `PUT /api/users/points/add`
- **Description**: Add points to a user's account.
- **Request Body**:
  - `points` (integer, form parameter): The number of points to add. Defaults to 0 if not provided.
  - `access_token` (string, form parameter): The JWT access token for authentication.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "{points} points added to {username} successfully"
    }
    ```
    - `message` (string): Confirmation message indicating how many points were added to which user's account.

  - **Errors**:
    - **403 Forbidden**: If `points` is negative.
    - **401 Unauthorized**: If the access token is missing, invalid, or the user cannot be authenticated.



### Deduct Points from User

- **URL**: `PUT /api/users/points/deduct`
- **Description**: Deduct points from a user's account.
- **Request Body**:
  - `points` (integer, form parameter): The number of points to deduct. Defaults to 0 if not provided.
  - `access_token` (string, form parameter): The JWT access token for authentication.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "{points} points deducted from {username} successfully"
    }
    ```
    - `message` (string): Confirmation message indicating how many points were deducted from which user's account.

  - **Errors**:
    - **403 Forbidden**: If `points` is negative.
    - **401 Unauthorized**: If the access token is missing, invalid, or the user cannot be authenticated.
    - **401 Unauthorized**: If the user has insufficient points to deduct the specified amount.


## Stay in touch :
- Author - [Ouail Laamiri](https://www.linkedin.com/in/ouaillaamiri/)

## License

PubAIAPI is [GPL licensed](LICENSE).