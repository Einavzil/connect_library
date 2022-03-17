# Library Database
A python program that connects to the library database. 

To run the program, you should run it through the command line or IDE.
Make sure to create a user by running the following code in the MySQL command prompt or workbench:

´´´CREATE USER 'Maria'@'localhost'
IDENTIFIED BY 'password'
;´´´

´´´GRANT SELECT, UPDATE, INSERT, DELETE, EXECUTE ON *.* TO 'maria'@'localhost'
;´´´

It is also important to install the python conenctor to mysql.
You can do so by creating a virtual environment in the git bash:

´´´make venv´´´

Activate the virtual environment, and install the MySQL connector by the following command:

´´´pip install mysql-connector-python´´´

Or by installing the whole requirements file (Code analysis included):

´´´make install´´