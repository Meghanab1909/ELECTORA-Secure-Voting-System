## Project Overview
Electora is a Secure Voting System implemented in Python Tkinter using Socket Programming. This project uses TCP socket as TCP prioritizes reliability over speed of transmission. 

## Files of this Repository
<table>
  <tr>
    <th>Poll1.py</th>
    <td>
      This python file is responsible to receiving the poll admin details. The poll admin details are stored in a table in mySQL. Only after authenticating the poll admin, Poll2.py shall open. 
      <br><br>
      <b>Features of Poll1.py</b>
      <ol>
        <li>Receives poll admin details</li>
        <li>Checks SQL database to verify and authenticate</li>
        <li>Necessary validations are present</li>
      </ol>
    </td>
  </tr>
    <tr>
      <th>Poll2.py</th>
      <td>
      This python file is responsible for making the poll, sending the poll info to the server and live stats. In addition to this, there is also a poll time feature. By default the poll time is set to 5:00pm (but it can be modified).
      <br><br>
      <b>Features of Poll2.py</b>
      <ol>
        <li>Recives the poll details</li>
        <li>Submits the poll info to server</li>
        <li>Displays live stats</li>
        <li>End Poll Option, to end the poll prior to the set poll time</li>
        <li>Keeps track of poll time. If poll time is exceeded then the poll is terminated automatically with the results being sent to registered voters.</li>
        <li>Necessary validations are present</li>
      </ol>
      </td>
    </tr>
  <tr>
    <th>Server.py</th>
    <td>
      This python file is the Server file of this project. It is the integral part of the project responsible for many functions. 
      <br><br>
      <b>Features of Server.py</b>
      <ol>
        <li>Receives poll data and writes into SQL database</li>
        <li>Checks voter details. If the voter details are found, the OTPs are sent via phone number (using twilio) and email (using SMTP) for authentication.</li>
        <li>If the authenticated, the server sends the poll info to the voter</li>
        <li>Receives the votes of the voters, sets the voter id status to voted (updates in SQL database) and stores it in a csv file. The csv file aides the live stats of Poll2.py.</li>
        <li>Keeps track of poll time. If the time is exceeded OR end poll button is pressed, it terminates all the functions indicating the poll is terminated. </li>
        <li>Necessary validations are present</li>
      </ol>
    </td>
  </tr>
  <tr>
    <th>Voter.py</th>
    <td>
      This python file is the voter file where the voters can get authenticated and vote for the candidate of their choice. 
      <br><br>
      <b>Features of voter.py</b>
      <ol>
        <li>Receives the login details of voters and sends to server</li>
        <li>If voter found, the OTPs are sent for authentication.</li>
        <li>Once authenticated, the voter can see the poll info sent by server</li>
        <li>Vote is submitted</li>
        <li>Necessary validations are present</li>
      </ol>
    </td>
  </tr>
</table>

## Prequisites
1. Python
2. Tkinter
3. MySQL (Create the database and necessary tables)
4. SMTP (Recommended to create an email specific to this project)
5. Twilio (Create a twilio account, video reference: https://www.youtube.com/watch?v=-fqGGqXHQ2E&pp=ygUGdHdpbGlv)
6. OpenSSL
7. Numpy and Matplotlib

## Before Running the Project
1. Download the project files in this repository
2. Generate csr, crt and key files. Check the code and do the necessary additions. The parts where the additions are to be made are highlighted.

## Run the project<br>
(Please run the project in the following sequence)
1. Server.py
2. Poll1.py (On the poll admin getting authenticated, Poll2.py shall open)
3. _Once the poll is made_, Voter.py

*Note: To get a better understanding of the project, kindly watch the screen recording of the project (project.mp4) uploaded in the repository. If the video is not being displayed/loaded on github please download it*

## Project Contributors _(In Alphabetical Order)_
1. Meghana Saisri Bisa - github username: Meghanab1909

2. Mitha M K

