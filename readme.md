# Dev Documentation
The Robotarium project was created using the minimalist Flask framework, i.e. Python. As DBMS, we opted for PostgreSQL.

## Prerequisites
python installed 
PostgreSQL installed
Arduino board recognition drivers installed on the machine

## Installation process
All the modules used to create this application are referenced in the "requirement.txt" file.

Once you've created your virtual environment, you can run the command : <br/>
 `pip install -r requirement.txt` to install the modules. <br/>
 Once this has been done, you can run : <br/>
 `pip freeze` to see if the modules have been correctly installed.

Next, you need to install Arduino CLI by following the instructions on :
https://arduino.github.io/arduino-cli/0.35/installation/ 
Once downloaded, you need to move the "arduino-cli.exe" executable into the project folder like this:

Once you've done all this, you can move on to the PostgreSQL DBMS. 
Create a **flaskapp** database 
Return to your virtual environment and enter the following commands: <br/> 
` $env:FLASK_APP="server.py" ` <br/>
`flask db init` <br/>
`flask db migrate` <br/>
`flask db upgrade` <br/>
Finally, you can run the application by doing : <br/>
`flask run --host=0.0.0.0`
