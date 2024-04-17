# multichat.backend

Requirements:
- python version 3 (python command should work from your terminal/cmd)
- pip (pip command should work from your terminal/cmd)
- mysql server should be installed and running on your system in the background
(you can check if its running by going to task manager -> services tab)
- mysqlworkbench program
- dbeaver program

Steps:

1. clone the project
2. open mysqlworkbench, open the localhost instance, then click on an icon which when highlighted says (create new schema). Then in the loaded window, type "multichat_dev" in the input and click apply. Click apply again and you can close mysqlworkbench.
3. In the project folder go to the subfolder "multichat" and then open the settings.py file. Go to line 75 which looks like this: 'PASSWORD': '', and in the '' type your sql password. If your password is blank than ignore this step. Also in case your username is not "root", also update the line 77 with the correct username.
4. From your terminal/cmd type python manage.py makemigrations
5. Run python manage.py migrate
6. Run python manage.py runserver
7. Open Dbeaver program
8. Create a connection to our database. Open the table messaging_service and add the rows with the info about every messenger (I will send you a pic on discord with correct info)