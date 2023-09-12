The Bloom Hospital website represents the culmination of my work as part of CS50's final project. Where CS50 is a course offered by Harvard University (Introduction To Computer Science)
#### Video Demo:  <https://youtu.be/D3IffWSjHME>
#### Description:
To register a member you just click on register and fill in the details and then click register
Then you are automatically redirected to login where you input the username and password.
To register a staff member you have to manually type /secret at the end of the URL to make sure not everyone has the the
ability to register as a staff member.
In the main page of the patient you have multiple options.
Donate is the first option where there is a donate button inside that makes sure that you want to donate.
Donate gets the data of the patient using his id stored in the session
And then the patient is redirected to the main page where he can see that he donated blood X times
If the patient want to see the staff members of the hospital, he can simply press Staff lookup and he will get a table
that displays all the staff members and their specializations.
Find a donor makes the patient look for a person who signed for blood donation before that has a certain blood type
entered by the user. A table of all the donors with their contact details is displayed.
Lookup schedule allows the patient to lookup the schedule of the a staff member where if the staff member is free at
a certain time slot, the patient could reserve it.
Reserve allows the patient to choose a time slot of a doctor and reserve it(if free).
If a successful reservation was made then in the main page the user is show the reservation as a table with the doctor's
name and the time slot.
Now, lets go the main page of a staff member where he is shown his schedule(the time slots that the patients resrved)
he has the ability to free a certain time slot or the entire schedule by simply pressing the free schedule button right
bellow his schedule.
He also has the ability to upload a test result where he can select the patient and then type into the results field the
result of the test.
When the patient logs into his account again, the patient will be shown the test result that the doctor uploaded
in his main page.



The static folder contains alot of images that were used in the web application as well as 2 style sheets where the
diffrence is that one contains a standard back ground and the other needs manual implementation


HTMLS:
layout.html: it is the main template where most other htmls inherit. It implements the bootstrap and the stylesheet and
certain buttons like donate, reserve etc... if the user is logged in and if the user is logged out they aren't displayed.
Also the register and login button if the user isn't logged in.

layout2.html is the same as layout.html however it implements a diffrent style sheet


index.html extends layout2.html and it has the title of home page.
Firstly it describes the use of the /secret in the URL to register a staff member.
Secondly it says how many times the user has donated blood by simply counting the number if entries in the the database in
the blood_donations table where the user has made.
Thirdly it displays the reservations that the user has with doctors and the time slot that he reserved
The last section is the test result where it is uploaded by the doctor using the upload result but more on that later.

donate.html contains a form just asking the user to submit it to make sure that he is fully aware that he will be donating
blood. The details about the donation are extracted from the database later on using the user's id

donor.html contains a form where it asks the user to input a blood type in order to find a donor with the matching blood type.
it has the blood types passed in as parameters in order to be able to display them as a drop down menu

donored.html displays the blood donations with the matching blood type that a user asked for
previously.It takes a query with the matching blood types and displays information about the donors.

error.html is an error template where it takes the cases where the user has done something wrong, it displays an error
message instead of the program crashing. The message is passed in as a parameter

free.html is a form used to ask the doctor whether he wants to free a certain time slot or his whole schedule.
He can choose using a drop down menu then clicking free where it will remove the data of the reservations from the database.

login.html is a form where the user is asked to input his username and password and press login to login

lookedup.html displays all staff members' name and specialization in a table by looping over them.

lookedup2.html displays a staff member's name and his each of the time slots whether he is free or busy at this time slot.
If the result is set to 1, that means that he is busy. Otherwise if it was set to 0, that means that he is free at this time slot.

lookup.html contains a form that has a drop down menu where you can select a doctor by his name to see his availability late one.
then it has the lookup button that is clicked after a doctor is chosen.

register.html is a form that asks the user to input his personal details like name, phone, email, address and so on,
also it promts the user to enter his username, password and password confirmation so that this data is used later on to login.
Also the data is stored in the database.

reserve.html is a form that asks the patient to choose a doctor and then choose a time slot and if that time slot if free for
the chosen doctor, then it is reserved for him later on

staff_error.html is the same as error.html however, it extends staff layout.html.
it gets a message as a parameter and displays it insead of terminating the application.

staff_index.html is the main page for the staff members where it displays their schedule and allows them to free it using the
free schedule button. Also it allows a staff member to upload a test result.

staff_layout.html is the main template where all other staff related templates extend. it contains the bootstrap and the stylesheet

staff_register.html is the template that is displayed when the user types /secret in the URL. It is the same as register.html however,
it has an extra input field called specialization to allow a staff member to input his specialization.
It stores the data in the database as a staff member,

thanks.html is a template that thanks the user for something. For example donating blood.


upload.html is a form that asks a doctor to choose a patient from a drop dowm menu and promt him to enter the test result.


application.py contains some libraries being implemented in requirements.txt
then it turns the file into a flask application


it configures a session so that the user remains signed in unless signed out

it has two lists to store the blood types and the available time slots


it  uses the database of hospital.db

at the route "/" if the user is a staff member then he should be redirected to /staff
otherwise, it gets the number of times the user donated blood and the reservations he
made and description written by the doctor and passes them to index.html to be displayed

the route "/thanks" just returns the template thanks.html to thank a user


the route "/donor":
if the user is a staff member then he is redirected to /staff
if the request method is post then it gets all the matches with the chosen blood type and
passes them to donored.html to be displayed.
else if it is a get then a the form contained in donor.html is displayef and the blood types
are passed in as parameters

the route "/reserve":
if post,tries to figure out which time slot was chosen to be resererved and accordingly check
its availability and update the database if it was available and reserve it.
if the method was get, it queries to get all the doctors list and passes them to reserve.html
in order for the user to choose a doctor using a drop down menu


the route "/donate":
if the user is a staff member then he is redirected to /staff
if the method was post then it gets the blood_type and other personal details from the database
using the ID of the user stored in the session and then insert it into the blood dontations table
in the database
if method was get, it returns the template donate.html and passes the blood types as a parameter

the route "/upload":
if the user is not a staff member then an error is returned
if method is get it return the template upload.html and the patients are passed in as a parameter
if method is post it gets the patient name and the description and then updates the database to set
the description to the one the doctor wrote

the route "/free"
if the user is not a staff member then an error is returned
if the method is get, the template free.html is returned.
if the method is post, it checks the time slot choosen or if all time slots are choosen to be freed
and then updates the database to free these time slots for the doctor using his session id
he is redirected to the main page afterwards

the route "/staff"
it gets all the reservaions that the doctor has and sends it to staff index.html to be displayed

the route "/login"
removes the user that is currently signed in (if any).
Then if the method is get then it returns login.html
if the request was post then it checks whether the input username and password match anything in the
database and if so the user is signed in, otherwise an error appears
the function checkpassword hash is used to check the input password with the hashed password stored in
the database.
then lastly it stores the user id in the session
If the user is a staff member, he is redirected to /staff
else if he is a normal patient then he is redirected to /


the route "/logout":
clears the session from logged in user and redirects the user to /login


the route "/staff_lookup"
gets all the staff members and passes them to lookedup.html to be displayed


the route "/register"
if the method is post, it gets the data that the user input in the form and checks
that the username is not already taken and that the password and password confimation match
and then it hashes the password and stores the data in the database
then redirects the user to /login
if method is get then it returns register.html passing in the blood types so that the form
is displayed for the user

the route "/lookup"
if the user is a staf member, he is redirected to /staff
if the method ths post, the schedule doctor chosen in the form will be queried and then passed to
lookedup2.html to be displayed.
if the method is get, then then the staff members are passed to lookup.html


the route "/secret"
if the method is post then the data input in the form is inserted to the database as a staff member this time
also a schedule is created for the new member in the database
if the method is get then the session is cleared to removed currently signed users from the session nd the
staff_register.html is returned with blood types passed in as a parameter.


hospital.db contains four tables, blood_donations, patients, reservations and timeslots

the table blood_donations has the following fields
name: to store the name of the donor
username: to store the username of the donor
phone: to store phone number of the donor
gender: to store the gender of the donor
blood_type: to store the blood type of the donor

the table patients stores the data of all the members staff and non staff
it has the following fields:
ID: so that it is a unique identifier
name: to store the name of the user
gender: to store the gender of the user
DOB: to store the date of birth of the user
phone: to store phone number of the user
email: to store the email address of the user
address: to store the address of the user
description: to carry the test results of the user
username: to carry the username of the user
password: to carry the password of the user
staff: to indicate whether the uesr is a staff member or not
specialization: to store the specialization of a staff member
blood_type: to store the blood type of the user

the table reservations has the fields:
patient_name: stores the patient name
patient_username: stores the patient username
doctor_name: store the doctor name
doctor_username: store the doctor username
time_slot: the time slot where the reservation is made


the table time_slots has the fields:
name: to store the name of the doctor
username: to store the username of the doctor
time_slot1: to store the availiability of timeslot 1 of the doctor
time_slot2: to store the availiability of timeslot 2 of the doctor
time_slot3: to store the availiability of timeslot 3 of the doctor
time_slot4: to store the availiability of timeslot 4 of the doctor
time_slot5: to store the availiability of timeslot 5 of the doctor


this was all done by Ali Mostafa Zeinelabdeen Ali Mohamed
Cairo, Egypt
