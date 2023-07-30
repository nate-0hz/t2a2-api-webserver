# Index of files for rubric requirements

| # | Index |
|----|----|
| .0 | Important Links |
| .1 | Installation and setup |
| R1 | Identification of the problem you are trying to solve by building this particular app |
| R2| Why is it a problem that needs solving? |
| R3 | Why have you chosen this database system. What are the drawbacks compared to others? |
| R4 | Identify and discuss the key functionalities and benefits of an ORM |
| R5 | Document all endpoints for your API |
| R6 | An ERD for your app |
| R7 | Detail any third party services that your app will use |
| R8 | Describe your projects models in terms of the relationships they have with each other |
| R9 | Discuss the database relations to be implemented in your application |
| R10 | Describe the way tasks are allocated and tracked in your project |

## .0 Important Links

[Github Repo](https://github.com/nate-0hz/t2a2-api-webserver)

[Trello Board](https://trello.com/b/g2Opst0X/nate-picone-t2a2-a-crud-app)

## .1 Installation and setup

### Requirements

1. Python 3 installed and updated to 3.11.4 (Tested on Homebrew, MacOS)

2. PostgreSQL installed and updated to version 15.3 (Tested on Homebrew, MacOS)

3. This repository - a clone or download of this repository.

4. An installed API platform, such as Postman or Insomnia.

### PostgreSQL

1. Log into your PSQL instance from your shell, and create a user `license_dev` with password and ability to log in. 

2. Create a new database `license_db`

3. Grant the user `license_dev` all privellages on the database

4. Change to the user and connect to the database

### Environment setup

1. In your shell, navigate to the parent directory of the application. If you saved it to `~/gitapps`, change to this directory.

2. From the terminal create a virtual environment with `python3 -m venv .venv`. Python3 is required for MacOS. Please check for your OS.

3. Activate the virtual environment from the terminal with `source .venv/bin/activate`

4. Install the requirements from requirements.txt file with: `pip3 -r install requirements.txt`. This will install the required packages and libraries.

5. In the terminal, navigate to `/src`.

6. Open `.flaskenv` in your terminal text editor and check the variables. `FLASK_APP` sets the primary .py file to use as the application and should not need changing. `FLASK_DEBUG` keeps the localhost server running and it is recommended to leave this. `FLASK_RUN_PORT` sets the port for the server. It is set to 8083 by default. Change this is there is a conflict, but the port set here is the port required for your API platform. Save and exit.

7. In the terminal, copy `.envsample` to `.env` in the same directory.

8. Open `.env` in your terminal text editor  

9. To the end of `DATABASE_URL=` add `"postgresql+psycopg2://license_dev:[PASSWORD]@localhost:5432/license_db"` Where:

    - `license_dev` is the name of the user you created in postgres
    - `[PASSWORD]` is the password you set for the user
    - `localhost` is the name of the server
    - `5432` is the default password used for the connection between psycopg2 and postgres
    - `license_db` is the database you created in your database

10. To the end of `JWT_SECRET_KEY=`, add a randomly generated secret key. For best results, use randomly generatedupper and lower case letters, and numbers of 40 characters length.

11. Save and exit.

### Database table set up

1. From the `/src` directory within the parent of the application.

2. In the terminal, enter `flask db drop`, to ensure there are no tables remaining from preinstalled attempts. If successful, you should receive the message `Tables dropped.` This can be repeated, if you need to remove the tables from the database at a later time, for some reason.

3. To create the tables, enter `flask db create`. This will create the table structure required for the application. If successfult, you will receive the message `Tables created.`

4. To seed the tables with test data, enter `flask db seed.` If successful, you will receive the following responses, indicating all four tables have been seeded:

``` zsh
Users table seeded and committed.
Applications table seeded and committed.
Licenses table seeded and committed.
allocations table seeded and committed.
```

5. To run the server, enter `flask run`. You will receive some dialogue in the terminal indicating the server is running:

``` zsh
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8083
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: [PIN number shown]
 ```

> Note: I find this dialogue helpful as it reminds me I have a server running with an open port, but if it is bothersome for you, you can turn off debugging mode by editing the `FLASK_DEBUG=1` value to 0 in `.flaskenv`

6. Open your API platform of choice. My preference is Postman.

7. In the url field, if you have kept the defaults, enter localhost:8083/ followed by the route and required verb needed. More details on these routes can be found in the endpoint documentation, below.

8. To quit the server, return to your terminal and press ctrl-C

---

## R1 Identification of the problem you are trying to solve by building this particular app

The license management component of User Access Management within an enterprise can be difficult where there is a large workforces, dozens or hundreds of applications, many with several licensing options at various price points.

Keeping track of costs associated with license tiers being incorrectly, and reclaiming licenses issued to employees who have left the organisation can be challenging.

## R2 Why is it a problem that needs solving?

Some solutions exist, such as ServiceNow Software Asset Management among others, but these often offer outstandingly expensive licensing models, often charging per user or per license, or they take significant infrastructure effort and expenditure to set up and maintain discovery tools, to assist with the management of licenses.

For a large enterprise, willing to invest time and energy into designing and deploying these solutions, it may pay off in the long run.

It has been difficult to find a simpler and quicker solution, and without the enterprise price tag. Within my place of employment, this frequently comes at a cost: either through hours spent on trawling through license allocations to find recovery or downgrade opportunities, or through the cost of wasted or disused licenses.

## R3 Why have you chosen this database system? What are the drawbacks compared to others?

While the chosen Database Management System (DBMS) for this application, PostgreSQL can be deployed as a noSQL database, in this configuration it has been instantiated as a relational database, which is most appropriate for the structure required for the application.

As this application is designed to store multiple sets of identical types of data (schemas), and the application calls for this data to be compared and calculated, an ORM can be easily utilised to complete this. The structure of a noSQL database, being more aligned to a collection of documents with potentially inconsistent information, and lacking a schema mechanism, would make this process difficult.

With the relational structure in place, the volume of data within the database’s tables is easily scalable, and the number of files managed by the application is relatively stable, without adversely impacting infrastructure overhead. This might not be the case if using a document-oriented noSQL solution, where the document number and complexity increases as the volume of data increases.

One drawback here, relating to scalability, is that relational databases are generally more difficult to scale across multiple servers or locations, which, for very large, or high traffic data stores, can adversely impact speed and operation of the server. As this application uses a relatively small database, with relatively low traffic demands, this is not anticipated to be an issue.

Data can be retrieved, manipulated and stored with relatively straightforward commands, resulting in ease of development for the application, as new and improved features are added. In contrast, were a noSQL database be deployed as a solution for this application, the potential for inconsistency in data would make the creation of new features difficult.

SQL databases offer protection, when multiple sessions are accessing the database. While some offer locks, which prevents data being read or written while it is being used by another session, PostgreSQL uses Multi-Version Currency Control (MVCC). Rather than locking access to the data, MVCC offers all sessions a snapshot of the data, and reconciles any downstream data impacts after the fact.

While relational databases require specialised knowledge of SQL for maintenance and development, and noSQL databases do not require this specialisation, the requirements in this case a simple, and the associated cost for this application would be minimal, when compared with the cumulative additional cost and complexity of deploying a noSQL database.

## R4 Identify and discuss the key functionalities and benefits of an ORM

Object Relational Mapping effectively operates as an interpreting layer between an application and an underlying database. It allows the application to create, read, update and delete data within the database, in an abstracted fashion through the ORM, rather than directly using SQL. [4.1] This creates a logical model, and allows for the manipulation of an application’s objects without constant consideration of how it relates to the underlying data source, instead converting table data and generating the required SQL code for the developer. [4.2]

This abstraction layer makes for more efficient code, speeding up development time and reducing complexity. [4.2]

As the abstraction layer provides parameterised SQL, it goes some way to limit SQL injection attacks, improving the security of the application. [4.3] With SQL, parameters can be directly injected into a query by a bad actor. For example, a website using a direct SQL SELECT query may return results, based on parameters, designed to limit what the user can see, based on their access or profile. This query can can be altered with an always-truthy OR statement, which returning all results, without limitation. 

Because an ORM handles the logic and communicates with the SQL database directly, it manipulates and limits the data being returned to the client, thus preventing this type of direct injection. [4.3]


[4.1] https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/

[4.2] https://www.theserverside.com/definition/object-relational-mapping-ORM

[4.3] https://www.appsecmonkey.com/blog/sql-injection

## R5 Document all endpoints for your API

### Authorisation

Within the auth_controller, two decorators have been defined to control authorisation for certain functions:

#### @authorise_as_admin

Endpoints with this decorator restrict authorisation only to users who have the `is_crud_admin` attribute with a `True` value, allowing authorisation restriction to elevated privellage actions, such as creating and deleting applications and licenses.

#### @authorise_as_access

The bulk of the endpoints within this application have level restrictions for this decorator, as most of the endpoitns and functions of the CRUD application are for the use of users of this applciation. These users can perform activities such as registering new users, adding and removing license allocations, and returning details of licenses.

Three types of users exist:

- __User without CRUD application access or admin rights__ - These are employees of the business who have enterprise licenses allocated to them but have no access to the CRUD application. The following attribute values should be used:  
    >    `is_crud_access: Flase`  
    >    `is_crud_admin: False`  

- __User with CRUD application access but no admin rights__ - These users can access all GET endpoints in the the application and are able to GET, POST and PUT/PATCH most of the defined endpoints, as this type of user is the main user of the application. The following attribute values should be used:
    >   `is_crud_access: True`  
    >   `is_crud_admin: Flase`

- __User with CRUD application access and admin rights__ - These users can access all enspoints, including those restricted to admin users. The following attribute values should be used:
    >   `is_crud_access: True`  
    >   `is_crud_admin: True`

### Endpoints

### /auth/register (POST)

Endpoint used to register user details in the application.

Requires user to be registered and `@authorise_as_access` decorator to be satisfied.

__Required data__ 

- `name` is the employee's name (not nullable)  
- `email` is the employee's email address; must be unique  
- `password` is the employee's password  
- `is_crud_access` - set True to give the user access to the CRUD application, through the `@authorise_as_access` decorator. Admin users should also be set True here  
- `is_crud_admin` - set True to give the user admin access to the crud access via the `@authorise_as_admin` decorator
- `employment_start_date` - Add date in yyyy/mm/dd format

__Optional data__

- `employment_end_date` - Add date to signify the ser's termination date in yyyy/mm/dd format. This data is used to identify license allocations that can be removed through another endpoint.

Example JSON request body:

``` JSON
{
    "name": "Name Name",
    "email": "name@email.com",
    "password": "password",
    "is_crud_access": false,
    "is_admin_access": false,
    "employment_start_date": "2022/12/2"
}
```

This route validates the input and will return an error is a non-nullable field does not contain a value, or if the requirement for a unique email address has not been met.

On successful posting, the user will receive a response containing a dump of the data submitted, eg:

``` python
{
    "email": "name@email.com",
    "employment_end_date": null,
    "employment_start_date": "2022-01-11",
    "id": 5,
    "is_crud_access": true,
    "is_crud_admin": false,
    "name": "Blah Blah"
}
```

Where any non-nullable fields have no value, the API will respond with an error message advising one of the required fields are missing:

```JSON
{
    "error": "Name, email, password and employment start date are required"
}
```
### /auth/login (POST)

Endpoint used to authorise user access to the application. Successful login will return a bearer token that can be used to access other endpoints, using Postman, Insomnia or other API platforms.

Bearer token has a validity period of 24 hours.

__Required data__

- `email`
- `password`

Example JSON request body:

``` JSON
{
    "email": "name@email.com",
    "password": "password"
}
```

This route validates that the email address and password provided match the username and hashed password in the database table.

On successful posting, the user received a response with a dump of the user's email address, access level and bearer token, eg:

``` JSON
{
    "email": "admin@email.com",
    "is_crud_access": true,
    "is_crud_admin": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5MDU5ODIzNCwianRpIjoiNTlhYzNkNzgtZTlkYy00MDI3LWIwM2MtNWM0Y2I0YmQ4NWZlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE2OTA1OTgyMzQsImV4cCI6MTY5MDY4NDYzNH0.zM9LUrymw1NUydCkAaq-TpifQOiW5CEJlLb_WGQ8--0"
}

```

Where the email address or password is incorrect, the user will receive a message adivising this, eg:

``` JSON
{
    "error": "Invalid email or password."
}
```

Where the user exists but does not have `is_crud_access` as True, the log in attempt receives a message advising that the email address does not have application access, eg:

``` JSON
{
    "error": "ncuser2@email.com does not have application access."
}
```

### /user (GET)

Endpoint used to retrieve all users.

No JSON body is required for GET but requires bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Expected result is a list of all users' emails, names, employment start and end dates, their employee ID, and whether they have application and/or admin access. For example:

``` JSON
[
    {
        "email": "ncuser2@email.com",
        "employment_end_date": null,
        "employment_start_date": "2021-10-01",
        "id": 4,
        "is_crud_access": false,
        "is_crud_admin": false,
        "name": "NonCRUD User2"
    },
    {
        "email": "ncuser1@email.com",
        "employment_end_date": "2022-10-23",
        "employment_start_date": "2010-06-12",
        "id": 3,
        "is_crud_access": false,
        "is_crud_admin": false,
        "name": "NonCRUD User1"
    }
]
```

### /user/\<id\> (GET)

Endpoint used to retreive a single user.

No JSON body is required for GET but requires the user ID in the path, a bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Expeceted result is the values for email, name, employment start and end dates, employee ID, and whether application and/or admin access is True, for a sepcific user. For example:

``` JSON
{
    "email": "cuser@email.com",
    "employment_end_date": null,
    "employment_start_date": "2001-01-13",
    "id": 2,
    "is_crud_access": true,
    "is_crud_admin": false,
    "name": "CRUD User"
}
```

Where a user is not found with the specified id, the API will return an error message advising the same:

``` JSON
{
    "error": "User with id 7 not found."
}
```

### /user/\<id\> (DELETE)

Endpoint used to delete a single user.

No JSON body is required to delete the user, but the user ID is required int he path, a bearer token from authentication access, and that the user satisfies the `@authorise_as_access` requirements.

Where the user is successfully deleted, the API will return a confirmation message showing the user name and ID number:

``` python
{
    "message": "User 'NonCRUD User2' with id 4 deleted successfully."
}
```

Where no user is found with that ID, the API will return an error message:

``` python
{
    "error": "User not found with id 4."
}
```

### /application (GET)

Endpoint used to retreive a list of all applications, and the license types associated with them.

No JSON body is required for GET but requires bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Expected result is a list of: application name, description, application id, whether the application is active, and a list of licenses associated with the application, eg:

``` JSON
[
    {
        "description": "Salesforce platform",
        "id": 3,
        "isActive": true,
        "licenses": [
            {
                "application_id": 3,
                "description": "Standard Salesforce license for Sales and Service Teams",
                "id": 5,
                "is_position_level_restricted": true,
                "monthly_cost": "44.95",
                "name": "Sales-Force-Standard",
                "total_purchased": 15
            }
        ],
        "name": "Salesforce"
    },
    {
        "description": "Adobe Creative Cloud platform",
        "id": 2,
        "isActive": true,
        "licenses": [
            {
                "application_id": 2,
                "description": "Adobe Creative Cloud License",
                "id": 4,
                "is_position_level_restricted": true,
                "monthly_cost": "78.95",
                "name": "Adobe-Creative-Cloud",
                "total_purchased": 15
            }
        ],
        "name": "Adobe Creative Cloud"
    }
]
```

### /application/\<id\> (GET)

Endpoint used to retreive details of a single application.

No JSON body is required for GET but requires the application ID in the path, a bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Expeceted result is the values for application id,  name, description, whether the application is active, and a list of licenses associated with the applciation, and their details, eg:

``` JSON
{
    "description": "Microsoft M365 platform",
    "id": 1,
    "isActive": true,
    "licenses": [
        {
            "application_id": 1,
            "description": "Microsoft M365 F3 license",
            "id": 1,
            "is_position_level_restricted": false,
            "monthly_cost": "9.95",
            "name": "M365-F3",
            "total_purchased": 10
        },
        {
            "application_id": 1,
            "description": "Microsoft M365 E3 license",
            "id": 2,
            "is_position_level_restricted": false,
            "monthly_cost": "25.95",
            "name": "M365-E3",
            "total_purchased": 50
        },
        {
            "application_id": 1,
            "description": "Microsoft M365 E5 license",
            "id": 3,
            "is_position_level_restricted": true,
            "monthly_cost": "34.95",
            "name": "M365-E5",
            "total_purchased": 15
        }
    ],
    "name": "Microsoft M365"
}
```

Where no application of that id is found, the API will return an error message stating the same:

``` JSON
{
    "error": "Application not found with id 8"
}
```

### /application/new (POST)

Endpoint used to add a new application to the CRUD database.

A bearer token from authentication access, and that the user satisfy the `@authorise_as_admin` requirements.

The request body requires:

- `name` of the application
- `description` of the application (optional)
- `isActive` boolean to indicate if the application is active or not (default value is True).

An example body of the JSON POST request is:

``` JSON
{
    "name": "Trello",
    "description": "A kanban application",
    "isActive": true
}
```

Successful posting of new application will return a response with a dump of the application attributes, including the application ID and an empty list of licneses. Licenses are added to applications through another endpoint. Eg:

``` JSON
{
    "description": "A kanban application",
    "id": 4,
    "isActive": true,
    "licenses": [],
    "name": "Trello"
}
```

Where any non-nullable fields have no value (in this case, name), the API will respond with an error message advising the missing field:

``` JSON
{
    "error": "Application name is required"
}
```

### /application/\<id\> (PUT/PATCH)

Endpoint used to edit an application's data in the CRUD database.

A bearer token from authentication access, and that the user satisfy the `@authorise_as_admin` requirements.

The JSON only requires details to be updates, and can include:

- `name` of the application
- `description` of the application
- `isActive` boolean

Successfuly putting/patching will return a dump of the edited applciation. For example:

Putting a request to edit the name of application with ID  of 6:

``` JSON
{
    "name": "Twello"
}
```

Receives a response from the API of:

``` JSON
{
    "description": "A kanban application",
    "id": 6,
    "isActive": true,
    "licenses": [],
    "name": "Twello"
}
```

### /application/\<id\> (DELETE)

Endpoint used to delete an application's data in the CRUD database.

A bearer token from authentication access, and that the user satisfy the `@authorise_as_admin` requirements.

This endpoint does not require body in the request, however, the endpoint validates the application exists and has no licnese types associated with it.

If the application ID does not exist, the API returns an error message:

```JSON
{
    "error": "Application not found with id 6."
}
```

If the application has license types associated with it, the API returns an error message advising the same, and gives advice on how to resolve:

``` JSON
{
    "error": "Cannot delete application 'Microsoft M365' with id 1 as license types have been associated with the application. Please remove the license types first."
}
```

Successful deletion of the application from the database, returns a message advising the application ID and name:

``` JSON
{
    "message": "Application 'Twello' with id 6 deleted successfully."
}
```

### /license (GET)

No JSON body is required for GET but requires bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Expected result is a list of: license details, including license name, description, id, monthly cost, total licenses purchased and application name, eg:

``` JSON
[
    {
        "application": {
            "name": "Salesforce"
        },
        "description": "Standard Salesforce license for Sales and Service Teams",
        "id": 5,
        "monthly_cost": "44.95",
        "name": "Sales-Force-Standard",
        "total_purchased": 15
    },
    {
        "application": {
            "name": "Microsoft M365"
        },
        "description": "Microsoft M365 F3 license",
        "id": 1,
        "monthly_cost": "9.95",
        "name": "M365-F3",
        "total_purchased": 10
    }
]

```

### /license/\<id\> (GET)

Endpoint used to retreive details of a single license type.

No JSON body is required for GET but requires the license ID in the path, a bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Expected result is a list of: license details, including license name, description, id, monthly cost, total licenses purchased and application name, eg:

``` JSON
{
    "application": {
        "name": "Microsoft M365"
    },
    "description": "Microsoft M365 F3 license",
    "id": 1,
    "monthly_cost": "9.95",
    "name": "M365-F3",
    "total_purchased": 10
}
```

Where no license of that id is found, the API will return an error message stating the same:

``` JSON
{
    "error": "License with id 7 not found."
}
```

### /license/\<id\> (DELETE)

Endpoint used to delete single license type.

No JSON body is required for GET but requires the license ID in the path, a bearer token from authentication access, and that the user satisfy the `@authorise_as_admin` requirements.

If the application ID does not exist, the API returns an error message:

``` JSON
{
    "error": "License not found with id 7."
}
```

If the license id has users associated with it, the API returns an error message advising the same, eg:

``` JSON
{
    "error": "Cannot delete license 'Adobe-Creative-Cloud' with id 4 as it currently allcoated to at least one user."
}
```

Successful deletion of the license from the database, returns a message advising the application ID and name:

``` JSON
{
    "message": "License id: 2 with name: M365-E3 deleted successfully."
}
```

### /license/new (POST)

Endpoint used to add a new license type to the CRUD database.

A bearer token from authentication access, and that the user satisfy the `@authorise_as_admin` requirements.

The request body requires:

- `name` of the license
- `description` of the license
- `monthly_cost` numeric, decimal value to capture the license fee. Include numbers only, and to two decimal places.
- `total_purchased` for the number of licenses purchased
- `application` to add the application id

An example body of the JSON POST request is:

``` JSON
{
    "name": "Adobe-trial-license",
    "description": "trial licnese for Adobe",
    "application_id": 2,
    "monthly_cost": 4.95,
    "total_purchased": 1
}
```

Successful submission will return the license and application details:

``` JSON
{
    "application": {
        "name": "Adobe Creative Cloud"
    },
    "application_id": 2,
    "description": "standard license for Adobe",
    "id": 6,
    "monthly_cost": "4.95",
    "name": "Twello-license",
    "total_purchased": 1
}
```

If the specified application ID does not exist, the API will return an error advising the same:

``` JSON
{
    "error": "Application not found with id 6"
}
```

### /allocation/ (GET)

Endpoint used to retreive a list of all license allocations between license types and users.

No JSON body is required for GET but requires bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Expected result is a list of: allocation id, license id, and enough information to identify the user, including user is, user email, user name, and user employment end date, which is used in a later endpoint.

Successful request will return details for all allocations, similar to the below snippet:

``` JSON
[
    {
        "id": 7,
        "license_id": 1,
        "user_email": "ncuser2@email.com",
        "user_employment_end_date": null,
        "user_id": 4,
        "user_name": "NonCRUD User2"
    },
    {
        "id": 6,
        "license_id": 1,
        "user_email": "ncuser1@email.com",
        "user_employment_end_date": "2022-10-23",
        "user_id": 3,
        "user_name": "NonCRUD User1"
    }
]
```

### /allocation/user/\<id\> (GET)

Endpoint used to retreive all licenses allocated to the user specified with the ID in the path.

No JSON body is required for GET but requires bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Expected result is a list of the user name, id, and total cost to the business for all licenses consumed by the user, along with a list breaking down each license ID, name and monthly cost, eg:

``` JSON
{
    "licenses": [
        {
            "license_id": 3,
            "license_name": "M365-E5",
            "monthly_cost": "34.95"
        },
        {
            "license_id": 4,
            "license_name": "Adobe-Creative-Cloud",
            "monthly_cost": "78.95"
        },
        {
            "license_id": 5,
            "license_name": "Sales-Force-Standard",
            "monthly_cost": "44.95"
        }
    ],
    "total_monthly_cost": "158.85",
    "user_id": 1,
    "user_name": "Admin User"
}
```

Where the user id does not exist, the API will return an error message advising this:

``` JSON
{
    "error": "No license allocations found for user with id 9"
}
```

### /allocation/license/\<id\> (GET)

Endpoint used to retreive all licenses allocated to the user specified with the ID in the path.

No JSON body is required for GET but requires bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Expected result are details of the license relating to the ID provided, and a list of users' details who have the license allcoated to them. The result also includes the total monthly cost of allocated licenses, eg:

``` JSON
{
    "license_id": 3,
    "license_name": "M365-E5",
    "total_monthly_cost": "69.90",
    "users": [
        {
            "monthly_cost": "34.95",
            "user_id": 1,
            "user_name": "Admin User"
        },
        {
            "monthly_cost": "34.95",
            "user_id": 2,
            "user_name": "CRUD User"
        }
    ]
}
```

Where no license is found with the given ID, the API returns an error message:

``` JSON
{
    "error": "No license allocations found for licence type with id 1"
}
```

### /allocation/\<id\> (DELETE)

Endpoint to delete the allocation of a license type to a user.

No JSON body is required for GET but requires bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Successful deletion of an allocation will return a confirmation message, including the allocation id, license id and user id:

``` JSON
{
    "message": "Allocation with id 7 for license id 1 for user id 4 deleted successfully ."
}
```

Where the allocation id does not exist, the API will return an error message advising this:

``` JSON
{
    "error": "Allocation not found with id 11."
}
```

### /allocation/new (POST)

Endpoint to create a new assocaition between a license type and a user.

No JSON body is required for GET but requires bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

The request body requires:

- `name` of the license
- `description` of the license
- `monthly_cost` numeric, decimal value to capture the license fee. Include numbers only, and to two decimal places.
- `total_purchased` for the number of licenses purchased
- `application` to add the application id

An example body of the JSON POST request is:

``` JSON
{
    "license_id": 2,
    "user_id": 4
}
```

Successful post request will return a dump of the added allocation, including additional user details to allow easier confirmation of the transaction:

``` JSON

{
    "id": 12,
    "license_id": 2,
    "user_email": "ncuser2@email.com",
    "user_employment_end_date": null,
    "user_id": 4,
    "user_name": "NonCRUD User2"
}
```

If license and user pairings already exist, the API will return an error stating this:

``` JSON
{
    "error": "License ID 2 has already been assigned to User ID 4."
}
```

If license or user IDs used do not exist, the API will respond with error messages advising:

``` JSON
{
    "error": "User with ID 9 not found."
}
```

or:

``` JSON
{
    "error": "License with ID 22 not found."
}
```

### /allocation/expired (GET)

Endpoint used to retreive all licenses allocated to user whose employment_end date is no null and is less than today, indicating the person's employment has terminated in the past.

No JSON body is required for GET but requires bearer token from authentication access, and that the user satisfy the `@authorise_as_access` requirements.

Where license allocation to terminated users exists, expected results include the allocation ID, license details, including id and name, total monthly cost, and user details, including user id and name, the date the user terminated, and the monthly cost consumed by the user for the license.

For example:

``` JSON
{
    "expired_allocations": [
        {
            "licenses": [
                {
                    "allocation_id": 9,
                    "employment_end_date": "2022-10-23",
                    "license_id": 4,
                    "license_name": "Adobe-Creative-Cloud",
                    "monthly_cost": "78.95"
                },
                {
                    "allocation_id": 8,
                    "employment_end_date": "2022-10-23",
                    "license_id": 3,
                    "license_name": "M365-E5",
                    "monthly_cost": "34.95"
                },
                {
                    "allocation_id": 6,
                    "employment_end_date": "2022-10-23",
                    "license_id": 1,
                    "license_name": "M365-F3",
                    "monthly_cost": "9.95"
                }
            ],
            "user_id": 3,
            "user_name": "NonCRUD User1"
        }
    ],
    "total_monthly_cost": "123.85"
}
```

Where no licenses are allocated to termianted users, the API returns that as a message:

``` JSON
{
    "message": "No expired license allocations found."
}
```

## R6 An ERD for your app

![Application ERD](./docs/img/SaaS-LIcense-CRUD-v1.png)

The database design consists of four tables, with normalised data. Data requiring calculation has this completed in the model and retruned to the client via the controller, so as not to store calculated data within the table.

There is no duplication of data on the table.

For further detail on how the models and tables relate to each other, please see the following sections.

## R7 Detail any third party services that your app will use

### bcrypt

bcrypt is a password hashing function, derived from the blowfish cypher [7.1] and is deployed in this application to prevent passwords being transmitted in plain text. This adds security to the application by reducing the opportunity for a bad actor to attempt access to the application through intercepting the plaintext password, or through bruteforce password cracking.

The function repeatedly encrypts the provided password to a hash, and transmits this from the client to the application's backend, which compares it to the has stored in the database.

[7.1](https://en.wikipedia.org/wiki/Bcrypt)

### Flask

The micro web framework unpon which allows CRUD applications to be built and operate within Python, allowing the controllers and models to be constructed, which are essential to this application.

### Flask-DotEnv

Flask-DotEnv allows for the creation of a .flaskenv file, which defines parameters required for the Flask environment. In this case, the Flask server port is defined, along with dubug option and the definition of which python file should be treated as the main application file.

### python-dotenv

This extension is used to create the environment for the application, and abstracts the parameters used for the database URL and JSON Web Token secret key, keeping these secure. These attributes are stored in the .env file. A .envsample file is provided to allow users to identify required attributes and provide their own.

### Marshmallow

Provides the schemas used by the models to validate input, serialises objects to primative types, for JSON requests and HTTP APIs, and deserialises input into application-level objects for use within the schema.

### SQLAlchemy

The Python library which creates the ORM for this application, and generates the SQL queries required for the application's interation with the database.

### flask-marshmallow

This provides the integration between Flask and Marshmallow, and in the application creates schemas as subclasses of the schemas automatically generated by Marshmallow.

### flask-jwt-extended

This simple extension for JSON Web Tokens (JWT) handles authentication of a user, through the use of bearer tokens, and handles the secure transmission of data between server and client.

On authentication, the server sends a token to the client, which is then used by the client to validate its authentication to perform the requests is generates. The JWT is transmitted with each request that requires it.

### flask-sqlalchemy

This extension integrates Flask and SQLAlchemy to simplify operation of the two extensions. In this application, it is used largely to define models as classes, seen as `class ClassName(db.Model)`. This in turn allows the use of `db.Xxx` methods to be used through the application.

### psycopg2

psycopg2 allows python to interact with the SQL database directly, by creating an API between the application and the database.


## R8 Describe your projects models in terms of the relationships they have with each other

Four models are created in this application:

1. User model, which houses information related to users within an organisation;
2. Application model, which contains information about the applications being used by the orgasnisation;
3. License Model, which holds the verious available licenses for the applciations, that can be allocated to users;
4. Allocation model, which records the allocation of a license to a user.

### User Model

The Primary Key of the User model (id) forms a Foreign Key in the Allocation model, and changes in this model backpopulate the "user" variable in the Allocation schema. A user deletion will result in the cascading deletion of license allocations to the user.

``` python
class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_crud_access = db.Column(db.Boolean, nullable=False, default=False)
    is_crud_admin = db.Column(db.Boolean, nullable=False, default=False)
    employment_start_date = db.Column(db.Date, nullable=False)
    employment_end_date = db.Column(db.Date, nullable=True) # TODO back populate LicenseAllocation table

    # at model level    
    allocation = db.relationship('Allocation', back_populates='user', cascade='all, delete')
```

### Application Model

The Primary Key of the Application model (id) forms a Foreign Key in the Licenses model, and changes in this model backpopulate the "application" variable in the License model. An application deletion will result in the cascading deletion of the license type, however safeguards have been introduced to prevent the removal of an application if licenses have been associated with it.

``` python
class Application(db.Model):
    __tablename__='applications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    isActive = db.Column(db.Boolean, default=True)

    # at the model level
    licenses = db.relationship('License', back_populates='application', cascade='all, delete')
```

### License Model

The Primary Key of the License model (id) forms a Foreign Key in the Allocation model, and changes in this model backpopulate the "license" variable in the Allocation model. A license being deleted will result in the cascading deletion of the allocations using this data.

The License model contains an application_id variable, with Foreign Key constraints from the Application model.

``` python
class License(db.Model):
    __tablename__='licenses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    monthly_cost = db.Column(db.Numeric(precision=6, scale=2), nullable=False)
    total_purchased = db.Column(db.Integer)
    # FK
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)

    # at model level
    application = db.relationship('Application', back_populates='licenses')
    allocation = db.relationship('Allocation', back_populates='license', cascade='all, delete')

```

### Allocation Model

The Allocation model has two Froeign Key constraints from the Primary Keys of User and License models.

``` python
class Allocation(db.Model):
    __tablename__= 'allocations'

    id = db.Column(db.Integer, primary_key=True)
    # FK
    license_id = db.Column(db.Integer, db.ForeignKey('licenses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   
    # model level
    license = db.relationship('License', back_populates='allocation', cascade='all, delete')
    user = db.relationship('User', back_populates='allocation')
```

### Other relationships between the data

User id, allocated licenses and license cost are used to calculate the monthly cost of a user's licensing to the business, which is provided through the /allocation/user/\<id\> endpoint.

User id, user employment end date, allocated licenses, and license cost are used to provide license recovery and cost information for users whose last working date has passed, allowing for easy identification of licenses that can be deallocated, along with the costs saved by doing so.

Allocated licenses, license cost, and application data is used in the /allocation/license/\<id\> endpoint to calculate the ongoing monthly cost of ongoing allocated licenses types.

## R9 Discuss the database relations to be implemented in your application

### Users table

The Primary Key of the users table (id) forms a Foreign Key contstraint in the allocations table (user_id), with a respective no-or-one-to-many relationship, where one user can be allocated between zero and multiple licenses.

The data stored in this table include:

- id - the employee's ID (Primary Key, unique and not nullable), with unique constraint and used as foreign key constraint in table allocations
- name - the employee's name (not nullable)
- email - the employee's email address, (not nullable) with a unique key constraint
- password - saved in the table as hash (not nullable)
- is_crud_access - a boolean value to indicate whether the user has access to this application (not nullable and default value of False). Used for the `@validate_as_access` decorator
- is_crud_admin - a boolean value to indicate whether the user has elevated access within this application (not nullable and default value of False). Used for the `@validate_as_admin` decorator
- employment_start_date - Date value in the format of yyyy-mm-dd, indicating the employee's start date (not nullable)
- employe_end_date - Date value in the format of yyyy-mm-dd, indicating the employee's end date (nullable)

### Applications Table

The applications table holds simple information about the applications used by the organisation. The Primary Key of the applications table (id) forms a Foreign Key in the licenses table, with a no-or-one-to-many relationship, where one application can have between zero and multiple licenses. A good example of this is provided in the seed data, where the Microsoft M365 platform has multiple license types available, with different access and costs.

Data stored in this table include:

- id - the application ID (Primary Key, unique and not nullable), used as foreign key constraint in the table licenses
- name - application name (not nullable)
- description - application description (nullable)
- isActive - Boolean value to indicate whether the application is actively being used by the organisation (not nullable, default value of True). An application can be marked False prior to be deleted, should the organisation need to keep a record prior to deletion.

### Licenses Table

The licenses table holds information about the licenses available for the applications. The Primary Key of the licenses table (id) forms a secondary key in the allocations table. This forms a no-or-one-to-many relationship between applications and licenses (with zero-to-one application to zero-to-many licenses), and the same with the allocations table (with zero-to-one license to zero-to-many allocations).

Data stored in this table include:

- id - the license ID (Primary Key, unique and non nullable), used as foreign key constraint in the allocations table
- name - the name of the license (not nullable)
- description - a description of the license (nullable)
- monthly_cost - a numberic field with precision of 6 and scale of 2, used for the monthly cost of the each license unit (not nullable)
- total purchased - integer (nullable) for the number of licenses held
- application_id - foreign key constraint from applications table

### Allocations Table

This model solves the many-to-many relationship between users and licenses, as users can have licenses for multiple applications, and license types can be allcoated to multiple users.

Some integrity checking takes place in this model to prevent the same user/license pairings from occurring, so that a user cannot have the same license allocated multiple times.

A future enhancement here would be further limitations, preventing licenses from the same application being allocated to the same user.

Data stored in this table include:

- id - the allocation ID (Primary Key, unique and not nullable)
- license_id - foreign key constraint from licenses table
- user_id - foreign key constraint from users table

## R10 Describe the way tasks are allocated and tracked in your project

Tasks are defined sequentially, then separated into those required for the application and those required to satsify the rubric. These are added to a Trello board, with a separate tracking column for the rubric.

![](./docs/img/R10-1.jpg)

The rubric tasks will be monitored and checked off as completed.

For the other tasks, these are defined, sequenced and added to the Trello board. For this assignment, I created the categories of:

- Backlog, where all non-rubric tasks are initially added. As the project developed, new tasks were identified and added to the backlog.
- Current Sprint, where the tasks being worked on presently were moved to. The intention was to run stricter sprints for this assignment, however life events, work and some health issues interfered with this plan, so this column became more of a "current attention" column.
- Next Up, was the holding column for activities that required my attention next, or had some relevance to the current sprint, but were not being actively worked on at the time. This, at times, included prompts, reminders or enhancements.
- On hold, holds any activity that is unexpectedly delayed due to a dependency, or a reprioritisation. This is a temporary holding space until the future prioritisation of that task is determined.
- Room for improvement holds tasks that have been worked on or delivered but are not operating satisfactorily. Tasks held here are either reprioritised back intot he sprint for correction, moved to on hold, where an immediate solution is not possible, or added to the junk drawer, if being discarded.
- Junk drawer holds tasks that will not be implemented in this iteration of the application. They are either not required, or it is not possible to implement in the time available, and can be revisited in a future iteration of the application.

![](./docs/img/R10-2.jpg)

The full Trello board can be viewed here: https://trello.com/b/g2Opst0X

Buoyed from successes with understanding class content of the Trello clone API, the initial approach had been to try to build all routes and functionality of each model and associated controller before moving on to the next. I quickly identified that an improvement here would be a redivide the tasks into features, crossing multiple models and controllers, and iterate the building of the application one feature at a time.

Thankfully as this was early in the development process, it was easy to recategorise and reprioritise the required tasks.