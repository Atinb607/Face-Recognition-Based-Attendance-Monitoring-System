############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import threading

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'bhardwajatin607@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="#1e2a38")
    
    # Update style for dark theme
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='#1e2a38',fg='#ffffff',font=('Helvetica', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="#ffffff", bg="#2c3e50", relief='solid',font=('Helvetica', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    
    lbl5 = tk.Label(master, text='   Enter New Password', bg='#1e2a38', fg='#ffffff', font=('Helvetica', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="#ffffff", bg="#2c3e50", relief='solid', font=('Helvetica', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    
    lbl6 = tk.Label(master, text='Confirm New Password', bg='#1e2a38', fg='#ffffff', font=('Helvetica', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="#ffffff", bg="#2c3e50", relief='solid', font=('Helvetica', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    
    cancel=tk.Button(master,text="Cancel", command=master.destroy, fg="#ffffff", bg="#e74c3c", height=1,width=25, activebackground="#c0392b", font=('Helvetica', 10, ' bold '))
    cancel.place(x=200, y=120)
    
    save1 = tk.Button(master, text="Save", command=save_pass, fg="#ffffff", bg="#3498db", height=1, width=25, activebackground="#2980b9", font=('Helvetica', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

# New functions for email notification system
def load_email_config():
    """Load email configuration from a JSON file"""
    assure_path_exists("EmailConfig/")
    config_file = "EmailConfig/email_config.json"
    
    if not os.path.exists(config_file):
        # Create default config if it doesn't exist
        default_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "your_email@gmail.com",
            "sender_password": "your_app_password",  # Use app password for Gmail
            "admin_email": "admin@example.com",
            "send_to_student": True,
            "send_to_admin": True,
            "student_email_domain": "student.example.com"
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        # Show message to configure email settings
        mess._show(title='Email Configuration', 
                  message='Please configure your email settings in the EmailConfig/email_config.json file')
        return default_config
    
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        mess._show(title='Error', message=f'Error loading email configuration: {str(e)}')
        return None

def configure_email():
    """Open a dialog to configure email settings"""
    global email_settings
    
    email_settings = load_email_config()
    
    email_config = tk.Toplevel()
    email_config.geometry("500x400")
    email_config.resizable(False, False)
    email_config.title("Email Configuration")
    email_config.configure(background="#1e2a38")
    
    # SMTP Server
    lbl_smtp = tk.Label(email_config, text="SMTP Server:", bg='#1e2a38', fg='#ffffff',
                       font=('Helvetica', 12, 'bold'))
    lbl_smtp.place(x=20, y=20)
    
    smtp_var = tk.StringVar(value=email_settings.get("smtp_server", ""))
    entry_smtp = tk.Entry(email_config, textvariable=smtp_var, width=30, fg="#ffffff", 
                         bg="#2c3e50", font=('Helvetica', 12, 'bold'))
    entry_smtp.place(x=200, y=20)
    
    # SMTP Port
    lbl_port = tk.Label(email_config, text="SMTP Port:", bg='#1e2a38', fg='#ffffff',
                       font=('Helvetica', 12, 'bold'))
    lbl_port.place(x=20, y=60)
    
    port_var = tk.StringVar(value=str(email_settings.get("smtp_port", "")))
    entry_port = tk.Entry(email_config, textvariable=port_var, width=30, fg="#ffffff", 
                         bg="#2c3e50", font=('Helvetica', 12, 'bold'))
    entry_port.place(x=200, y=60)
    
    # Sender Email
    lbl_sender = tk.Label(email_config, text="Sender Email:", bg='#1e2a38', fg='#ffffff',
                         font=('Helvetica', 12, 'bold'))
    lbl_sender.place(x=20, y=100)
    
    sender_var = tk.StringVar(value=email_settings.get("sender_email", ""))
    entry_sender = tk.Entry(email_config, textvariable=sender_var, width=30, fg="#ffffff", 
                           bg="#2c3e50", font=('Helvetica', 12, 'bold'))
    entry_sender.place(x=200, y=100)
    
    # Password
    lbl_pass = tk.Label(email_config, text="Password:", bg='#1e2a38', fg='#ffffff',
                       font=('Helvetica', 12, 'bold'))
    lbl_pass.place(x=20, y=140)
    
    pass_var = tk.StringVar(value=email_settings.get("sender_password", ""))
    entry_pass = tk.Entry(email_config, textvariable=pass_var, width=30, fg="#ffffff", 
                         bg="#2c3e50", font=('Helvetica', 12, 'bold'), show="*")
    entry_pass.place(x=200, y=140)
    
    # Admin Email
    lbl_admin = tk.Label(email_config, text="Admin Email:", bg='#1e2a38', fg='#ffffff',
                        font=('Helvetica', 12, 'bold'))
    lbl_admin.place(x=20, y=180)
    
    admin_var = tk.StringVar(value=email_settings.get("admin_email", ""))
    entry_admin = tk.Entry(email_config, textvariable=admin_var, width=30, fg="#ffffff", 
                          bg="#2c3e50", font=('Helvetica', 12, 'bold'))
    entry_admin.place(x=200, y=180)
    
    # Student Email Domain
    lbl_domain = tk.Label(email_config, text="Student Email Domain:", bg='#1e2a38', fg='#ffffff',
                         font=('Helvetica', 12, 'bold'))
    lbl_domain.place(x=20, y=220)
    
    domain_var = tk.StringVar(value=email_settings.get("student_email_domain", ""))
    entry_domain = tk.Entry(email_config, textvariable=domain_var, width=30, fg="#ffffff", 
                           bg="#2c3e50", font=('Helvetica', 12, 'bold'))
    entry_domain.place(x=200, y=220)
    
    # Checkboxes
    send_student_var = tk.BooleanVar(value=email_settings.get("send_to_student", True))
    check_student = tk.Checkbutton(email_config, text="Send to Students", 
                                  variable=send_student_var, bg='#1e2a38', 
                                  fg='#ffffff', selectcolor="#2c3e50", 
                                  activebackground="#1e2a38", activeforeground="#ffffff",
                                  font=('Helvetica', 12, 'bold'))
    check_student.place(x=20, y=260)
    
    send_admin_var = tk.BooleanVar(value=email_settings.get("send_to_admin", True))
    check_admin = tk.Checkbutton(email_config, text="Send to Admin", 
                                variable=send_admin_var, bg='#1e2a38', 
                                fg='#ffffff', selectcolor="#2c3e50", 
                                activebackground="#1e2a38", activeforeground="#ffffff",
                                font=('Helvetica', 12, 'bold'))
    check_admin.place(x=250, y=260)
    
    def save_config():
        try:
            new_config = {
                "smtp_server": smtp_var.get(),
                "smtp_port": int(port_var.get()),
                "sender_email": sender_var.get(),
                "sender_password": pass_var.get(),
                "admin_email": admin_var.get(),
                "send_to_student": send_student_var.get(),
                "send_to_admin": send_admin_var.get(),
                "student_email_domain": domain_var.get()
            }
            
            with open("EmailConfig/email_config.json", 'w') as f:
                json.dump(new_config, f, indent=4)
                
            global email_settings
            email_settings = new_config
            
            mess._show(title='Success', message='Email configuration saved successfully!')
            email_config.destroy()
            
        except Exception as e:
            mess._show(title='Error', message=f'Error saving configuration: {str(e)}')
    
    # Save Button
    save_btn = tk.Button(email_config, text="Save Configuration", command=save_config, 
                        fg="#ffffff", bg="#3498db", width=20, height=1, 
                        activebackground="#2980b9", font=('Helvetica', 12, 'bold'))
    save_btn.place(x=150, y=320)
    
    # Test Button
    def test_email():
        try:
            send_test_email(smtp_var.get(), int(port_var.get()), sender_var.get(), 
                           pass_var.get(), admin_var.get())
            mess._show(title='Success', message='Test email sent successfully!')
        except Exception as e:
            mess._show(title='Error', message=f'Error sending test email: {str(e)}')
    
    test_btn = tk.Button(email_config, text="Test Email", command=test_email, 
                        fg="#ffffff", bg="#2ecc71", width=10, height=1, 
                        activebackground="#27ae60", font=('Helvetica', 12, 'bold'))
    test_btn.place(x=370, y=320)
    
    email_config.mainloop()

def send_test_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email):
    """Send a test email to verify configuration"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Test Email from Attendance System"
    
    body = """
    <html>
    <body>
        <h2>Test Email</h2>
        <p>This is a test email from the Face Recognition Attendance System.</p>
        <p>If you received this email, your email configuration is working correctly.</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def send_attendance_email(student_id, student_name, date, time):
    """Send email notification about attendance"""
    try:
        # Load email configuration
        config = email_settings if 'email_settings' in globals() else load_email_config()
        if not config:
            return
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['Subject'] = f"Attendance Recorded on {date}"
        
        # Email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #f9f9f9; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h2 style="color: #3498db; border-bottom: 1px solid #ddd; padding-bottom: 10px;">Attendance Confirmation</h2>
                <p>Hello <b>{student_name}</b>,</p>
                <p>Your attendance has been successfully recorded with the following details:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                    <tr style="background-color: #3498db; color: white;">
                        <th style="padding: 10px; text-align: left;">Student ID</th>
                        <th style="padding: 10px; text-align: left;">Date</th>
                        <th style="padding: 10px; text-align: left;">Time</th>
                    </tr>
                    <tr style="background-color: #f2f2f2;">
                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{student_id}</td>
                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{date}</td>
                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">{time}</td>
                    </tr>
                </table>
                <p>Thank you for using our Face Recognition Attendance System.</p>
                <p style="font-size: 0.8em; margin-top: 40px; color: #777; text-align: center;">
                    This is an automated message. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send to student if enabled
        if config.get('send_to_student', True):
            student_email = f"{student_id}@{config['student_email_domain']}"
            student_msg = msg.copy()
            student_msg['To'] = student_email
            
            try:
                with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                    server.starttls()
                    server.login(config['sender_email'], config['sender_password'])
                    server.send_message(student_msg)
                    print(f"Email sent to student: {student_email}")
            except Exception as e:
                print(f"Error sending email to student: {str(e)}")
        
        # Send to admin if enabled
        if config.get('send_to_admin', True):
            admin_msg = msg.copy()
            admin_msg['To'] = config['admin_email']
            admin_msg['Subject'] = f"Attendance Alert: {student_name} ({student_id}) on {date}"
            
            try:
                with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                    server.starttls()
                    server.login(config['sender_email'], config['sender_password'])
                    server.send_message(admin_msg)
                    print(f"Email sent to admin: {config['admin_email']}")
            except Exception as e:
                print(f"Error sending email to admin: {str(e)}")
                
    except Exception as e:
        print(f"Error in sending email: {str(e)}")

###########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    df = pd.read_csv("StudentDetails/StudentDetails.csv") if os.path.isfile("StudentDetails/StudentDetails.csv") else pd.DataFrame()

    recognized_students = set()

    face_detected_time = None
    last_id = None

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        if len(faces) == 0:
            face_detected_time = None
            last_id = None
        for (x, y, w, h) in faces:
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                ts = time.time()
                current_time = datetime.datetime.fromtimestamp(ts)
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                if len(aa) == 0 or len(ID) == 0:
                    continue  # skip unknowns
                ID = str(ID[0])
                Name = str(aa[0])
                student_key = f"{ID}_{current_time.strftime('%d-%m-%Y')}"

                if student_key not in recognized_students:
                    if last_id != ID:
                        face_detected_time = current_time
                        last_id = ID
                    else:
                        duration = (current_time - face_detected_time).total_seconds()
                        if duration >= 3:  # held for 3 seconds
                            date = current_time.strftime('%d-%m-%Y')
                            timeStamp = current_time.strftime('%H:%M:%S')
                            attendance = [str(ID), '', Name, '', str(date), '', str(timeStamp)]

                            # Save attendance
                            filename = f"Attendance/Attendance_{date}.csv"
                            file_exists = os.path.isfile(filename)
                            with open(filename, 'a+', newline='') as f:
                                writer = csv.writer(f)
                                if not file_exists:
                                    writer.writerow(col_names)
                                writer.writerow(attendance)

                            # Show in UI
                            tv.insert('', 0, text=ID, values=(Name, date, timeStamp))

                            # Send email
                            email_thread = threading.Thread(
                                target=send_attendance_email,
                                args=(ID, Name, date, timeStamp)
                            )
                            email_thread.daemon = True
                            email_thread.start()

                            recognized_students.add(student_key)

                            # Close automatically
                            cam.release()
                            cv2.destroyAllWindows()
                            return
            else:
                last_id = None
                face_detected_time = None
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(im, Name if conf < 50 else "Unknown", (x, y - 10), font, 0.9, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) == 27:  # just in case someone wants to abort with ESC
            break

    cam.release()
    cv2.destroyAllWindows()


######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

# Define dark blue color scheme
DARK_MAIN = "#151b26"           # Dark blue/black for main background
PANEL_BG = "#1e2a38"            # Slightly lighter dark blue for panels
ACCENT_BLUE = "#3498db"         # Bright blue for important buttons
TEXT_COLOR = "#ecf0f1"          # Light grey/white for text
ACCENT_ORANGE = "#e74c3c"       # Red/orange for exit/clear buttons
HIGHLIGHT_GREEN = "#2ecc71"     # Green for confirmation/success
SECONDARY_BG = "#2c3e50"        # Medium dark blue for secondary elements
HEADER_BG = "#34495e"           # Dark blue for headers

# Load email configuration at startup
email_settings = load_email_config()

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background=DARK_MAIN)

# Create a style for ttk widgets
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", 
                background=SECONDARY_BG, 
                foreground=TEXT_COLOR, 
                fieldbackground=SECONDARY_BG,
                font=('Helvetica', 10))
style.configure("Treeview.Heading", 
                background=HEADER_BG, 
                foreground=TEXT_COLOR,
                font=('Helvetica', 11, 'bold'))
style.map('Treeview', background=[('selected', ACCENT_BLUE)])

frame1 = tk.Frame(window, bg=PANEL_BG)
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg=PANEL_BG)
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance Monitoring System", 
                   fg=TEXT_COLOR, bg=DARK_MAIN, width=55, height=1, font=('Helvetica', 29, 'bold'))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg=HEADER_BG)
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg=HEADER_BG)
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text=day+"-"+mont[month]+"-"+year+"  |  ", fg=ACCENT_BLUE, bg=DARK_MAIN, width=55, height=1, font=('Helvetica', 22, 'bold'))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg=ACCENT_BLUE, bg=DARK_MAIN, width=55, height=1, font=('Helvetica', 22, 'bold'))
clock.pack(fill='both', expand=1)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", 
                fg=TEXT_COLOR, bg=HEADER_BG, font=('Helvetica', 17, 'bold'))
head2.grid(row=0, column=0)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", 
                fg=TEXT_COLOR, bg=HEADER_BG, font=('Helvetica', 17, 'bold'))
head1.place(x=0, y=0)

lbl = tk.Label(frame2, text="Enter ID", width=20, height=1, fg=TEXT_COLOR, bg=PANEL_BG, font=('Helvetica', 17, 'bold'))
lbl.place(x=80, y=55)

txt = tk.Entry(frame2, width=32, fg=TEXT_COLOR, bg=SECONDARY_BG, font=('Helvetica', 15, 'bold'))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name", width=20, fg=TEXT_COLOR, bg=PANEL_BG, font=('Helvetica', 17, 'bold'))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2, width=32, fg=TEXT_COLOR, bg=SECONDARY_BG, font=('Helvetica', 15, 'bold'))
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile", bg=PANEL_BG, fg=TEXT_COLOR, width=39, height=1, font=('Helvetica', 15, 'bold'))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="", bg=PANEL_BG, fg=TEXT_COLOR, width=39, height=1, font=('Helvetica', 16, 'bold'))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance", width=20, fg=TEXT_COLOR, bg=PANEL_BG, height=1, font=('Helvetica', 17, 'bold'))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window, relief='ridge', bg=DARK_MAIN, fg=TEXT_COLOR)
filemenu = tk.Menu(menubar, tearoff=0, bg=SECONDARY_BG, fg=TEXT_COLOR)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Email Settings', command=configure_email)  # Add email settings menu item
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('Helvetica', 12, 'bold'), menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv = ttk.Treeview(frame1, height=13, columns=('name', 'date', 'time'))
tv.column('#0', width=82)
tv.column('name', width=130)
tv.column('date', width=133)
tv.column('time', width=133)
tv.grid(row=2, column=0, padx=(0,0), pady=(150,0), columnspan=4)
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')

###################### SCROLLBAR ################################

scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.grid(row=2, column=4, padx=(0,100), pady=(150,0), sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear, fg=TEXT_COLOR, bg=ACCENT_ORANGE, width=11, 
                        activebackground=SECONDARY_BG, font=('Helvetica', 11, 'bold'))
clearButton.place(x=335, y=86)

clearButton2 = tk.Button(frame2, text="Clear", command=clear2, fg=TEXT_COLOR, bg=ACCENT_ORANGE, width=11, 
                        activebackground=SECONDARY_BG, font=('Helvetica', 11, 'bold'))
clearButton2.place(x=335, y=172)    

takeImg = tk.Button(frame2, text="Take Images", command=TakeImages, fg=TEXT_COLOR, bg=ACCENT_BLUE, width=34, height=1, 
                    activebackground=SECONDARY_BG, font=('Helvetica', 15, 'bold'))
takeImg.place(x=30, y=300)

trainImg = tk.Button(frame2, text="Save Profile", command=psw, fg=TEXT_COLOR, bg=ACCENT_BLUE, width=34, height=1, 
                    activebackground=SECONDARY_BG, font=('Helvetica', 15, 'bold'))
trainImg.place(x=30, y=380)

trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages, fg=TEXT_COLOR, bg=HIGHLIGHT_GREEN, width=35, height=1, 
                    activebackground=SECONDARY_BG, font=('Helvetica', 15, 'bold'))
trackImg.place(x=30, y=50)

quitWindow = tk.Button(frame1, text="Quit", command=window.destroy, fg=TEXT_COLOR, bg=ACCENT_ORANGE, width=35, height=1, 
                      activebackground=SECONDARY_BG, font=('Helvetica', 15, 'bold'))
quitWindow.place(x=30, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()