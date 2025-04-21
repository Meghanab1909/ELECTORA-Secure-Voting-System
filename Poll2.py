from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import  Tk, Canvas
from PIL import Image, ImageTk
from tkinter import PhotoImage
import socket
import pickle
import os
import csv
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
from datetime import date
import ssl
import threading

root = Tk()
root.geometry("1150x764")
root.title("Poll Admin")

no_of_candidates = StringVar()

images = ["♞ - KJP",
          "✪ - SAP",
          "✏ - PVP",
          "☎ - CCP",
          "❇ - PSP",
          "π - PPP",
          "ↂ - TFP",
          "≙ - ERM"]

image_vars = []
names = []

poll_time = "17:00"

def display_glossary():
  def remove():
    label.destroy()
    button.destroy()
    
  image = PhotoImage(file = "grid.png")
  
  label = Label(root, image = image, height = 190, width = 300)
  label.image = image
  label.place(x = 848, y = 30)

  button = Button(root, text = "⛝", command = remove, bg = "white")
  button.place(x = 1127, y = 30)

def end_poll(WINNER):
  if(WINNER is None or WINNER == [] or len(WINNER) == 0):
    message.showinfo("No winners","No winners have emerged from the poll. The poll administrator is advised to take appropriate steps to inform the voters accordingly.")
  else:
    if(len(WINNER) == 1):
      winner = WINNER[0]
    else:
      winner = WINNER

    text = f"""\
    This is to officially declare that {winner} has secured the highest number of votes and is hereby announced as the elected winner of the poll.
    We extend our sincere appreciation to all voters for their active participation and commitment to upholding democratic values.
    For records and verification, this result has been digitally signed and time-stamped by the Electoral Committee.
    © 2025 Electora Voting Authority. All rights reserved.
    """

    html = f"""
        <!DOCTYPE html>
        <html>
          <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background: none;">
            <div style="background-color: #ffffff; border-radius: 25px; width: 600px; margin: 40px auto; padding: 40px; box-shadow: 0 6px 25px rgba(0,0,0,0.15);">
              <div align="center" style="margin-bottom: 20px;">
                <img style="width: 150px; height: 150px; font-size: 150px" src="cid:LOGO" alt = "🛡️"/>
              </div>
              <div align="center" style="color: #0a3d62; font-size: 28px; font-weight: bold;">Electora Voting Authority</div>
              <div align="center" style="color: #34495e; font-size: 14px; margin-bottom: 20px;">Verified • Trusted • Safe</div>
              <hr style="border: none; height: 3px; background-color: #0a3d62; margin: 20px 0; border-radius: 5px;" />
              <div style="color: #2c3e50; font-size: 17px; line-height: 1.7;">
                <p>This is to officially declare that <strong>{winner}</strong> has secured the highest number of votes and is hereby announced as the elected winner of the poll.</p>
                <p style="color: #3498db; font-weight: bold;">We extend our sincere appreciation to all voters for their active participation and commitment to upholding democratic values.</p>
                <p style="color: #3498db; font-size: 15px; margin-top: 25px;">For records and verification, this result has been digitally signed and time-stamped by the Electoral Committee.</p>
                <p style="text-align: center; font-size: 12px; color: #555; margin-top: 30px; border-top: 1px solid #ccc; padding-top: 10px;">
                  © 2025 Electora Voting Authority. All rights reserved.
                </p>
              </div>
            </div>
          </body>
        </html>
        """
    
    def send_emails():
      connect = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "412356",
        database = "secure_vote_db"
      )

      if(connect.is_connected()):
        cursor = connect.cursor()
      
      cursor.execute("SELECT email FROM voters")
      emails = cursor.fetchall()
      print(emails)

      sender = "electora.securevote@gmail.com"
      subject = "Poll Results - "+str(date.today())
      smtp_server = "smtp.gmail.com"
      smtp_port = 587 
      password = "jhhe ehco wamv zqax"

      try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
          server.starttls()
          server.login(sender, password)

          for (receiver,) in emails:
            if "example.com" not in receiver:
              msg = MIMEMultipart("alternative")
              msg["From"] = sender
              msg["To"] = receiver
              msg["Subject"] = subject
              
              msg.attach(MIMEText(text, "plain"))
              msg.attach(MIMEText(html, "html"))

              with open('LOGO.png', 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<LOGO>')
                msg.attach(img)

              server.sendmail(sender, receiver, msg.as_string())
              
        root.after(0, lambda: messagebox.showinfo("✅","Results have been successfully sent via all Voter's Registered Emails"))
      except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", e))

    messagebox.showinfo("Sending","Sending the poll results to the Voters. This may take a moment.\n\nNote: Please do not close this window until you receive a confirmation message stating that all emails have been successfully sent. This process involves heavy network operations and may take some time. Temporary freezing or unresponsiveness is expected and does not indicate an error.")
    root.update() #Process any pending UI operations before sending emails
    threading.Thread(target = send_emails).start()

  try:
    server_host = "MSB"
    server_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    ssl_client_socket = context.wrap_socket(client_socket, server_hostname = server_host)
    ssl_client_socket.connect((server_host, server_port))
    message = {"poll_status":"ended"}
    ssl_client_socket.send(pickle.dumps(message))
    ssl_client_socket.close()
  except Exception as e:
    messagebox.showerror("Error sending Poll Status to Server",e)

def display_live_stats():
  global stats_window, canvas, anext

  stats_window = Toplevel(root)
  stats_window.title("Poll Live Stats")
  stats_window.geometry('1150x764')

  fig, ax = plt.subplots(figsize=(11, 6))
  canvas = FigureCanvasTkAgg(fig, master=stats_window)
  canvas.get_tk_widget().pack(pady=20)

  connect = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "412356",
    database = "secure_vote_db"
  )

  if(connect.is_connected()):
    cursor = connect.cursor()
  
  cursor.execute("SELECT DISTINCT RIGHT(symbol, 3) from poll_info")
  all_parties = [row[0] for row in cursor.fetchall()]
  
  def refresh_graph():
        ax.clear()

        with open("vote_results.csv", "r") as file:
            reader = csv.reader(file)
            voted_parties = [row[0] for row in reader if row]

        # Count and draw updated stats
        vote_count = Counter(voted_parties) 
        
        votes = [vote_count.get(i, 0) for i in all_parties] 
        
        ax.bar(all_parties, votes, color="skyblue", width = 0.4)
        ax.set_xlabel("Party")
        ax.set_ylabel("Votes")
        ax.set_title("Live Election Vote Stats")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        canvas.draw()
        stats_window.after(2000, refresh_graph)

        if vote_count:
          max_votes = max(vote_count.values())
          winners = [name for name, count in vote_count.items() if count == max_votes]
        else:
          winners = []

        current_time = time.strftime("%H:%M")

        if(current_time < poll_time):
          cursor.close()
          connect.close()
          end_poll_button = Button(stats_window, text = "End Poll", font = ("Tahoma", 15), command = lambda: end_poll(winners))
          end_poll_button.place(x = 1060, y = 0)
        elif(current_time == poll_time):
          messagebox.showinfo("Time Up","The Poll has ended. Sending Results to Voters")
          end_poll(winners)
          stats_window.destroy()
        
  refresh_graph()
    
def send_to_server(poll_data):
  SERVER_HOSTNAME = "MSB"
  SERVER_PORT = 12345
  
  try:
    SERVER_IP = socket.gethostbyname(SERVER_HOSTNAME)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    ssl_client_socket = context.wrap_socket(client_socket, server_hostname=SERVER_HOSTNAME)
    ssl_client_socket.connect((SERVER_IP, SERVER_PORT))

    data = pickle.dumps(poll_data)
    ssl_client_socket.sendall(data)
    ssl_client_socket.close()

    messagebox.showinfo("Success", "Poll submitted Successfully")
    
    current_time = time.strftime("%H:%M")
    if(current_time < poll_time):
      display_live_stats()
      root.withdraw()
    else:
      messagebox.showinfo("Time Exceeded","The live stats can only be viewed until 5:00pm IST\n\nNote: To retain poll information, please do not shut down or close the server. Doing so will result in the loss of all poll data.")
  except Exception as e:
    messagebox.showerror("Failed", f"Failed to connect to Server: {e}")

def submitpoll():
  for i in names:
    if(i == '' or i.get() == ''):
      messagebox.askretrycancel("Error","Please fill the all the fields to submit poll")
      break

  for i in image_vars:
    if(i == '' or i.get() == ''):
      messagebox.askretrycancel("Error","Please select symbol(s) to submit poll")
      break
  
  name_values = [i.get() for i in names]
  image_values = [i.get() for i in image_vars]
  
  if(len(set(name_values)) != len(name_values)):
    messagebox.askretrycancel("Name Error","Duplicate entries are not allowed. To retry, refresh the page")
    return
  
  if(len(set(image_values)) != len(image_values)):
    messagebox.askretrycancel("Symbol Error","Duplicate entries are not allowed. To retry, refresh the page")
    return

  poll_data = []

  for i in range(len(names)):
    if(names[i].get() == "" or image_vars[i].get() == ""):
      messagebox.askretrycancel("Error", "Please fill all fields to submit poll")
      return

    poll_data.append({"name": names[i].get(), "symbol": image_vars[i].get()})

  agreement = messagebox.askyesno("Terms and Conditions",
        "By using the Electora Secure Vote platform, the poll administrator agrees to adhere strictly to all ethical and legal guidelines governing fair voting practices. The administrator is solely responsible for:\n1. The integrity and security of the polls they create and manage.\n2. Ensuring that no unauthorized or malicious activity (e.g., tampering with votes, voter impersonation, or data misuse) that occurs under their supervision.\nIn the event of any detected or reported malicious activity, including but not limited to vote manipulation, unauthorized access, or violation of user privacy, the poll administrator shall be held fully accountable.\nElectora Secure Vote shall not be liable for any consequences resulting from the misuse of administrative privileges.\n\nClick Yes to accept the Terms and Conditions and proceed"
        )
  if agreement:
    send_to_server(poll_data)
  else:
    messagebox.showinfo("Declined", "You must accept the terms to proceed.")

def reset():
  messagebox.showinfo("Reset","Please wait while the page is reloaded")
  os.startfile("Poll2.py")
  root.destroy()


def display():
  global name_entry, combobox, submit_poll, refresh_button

  n_fetch = int(no_of_candidates.get())

  for i in range(n_fetch):
    Label(root, text = f"{i+1}. Name:", font = ("Tahoma", 11), bg = "white" ).place(x = 275, y = 395 + i * 30) 

    name_var = StringVar()
    name_entry = Entry(root, textvariable = name_var, font = ("Tahoma", 11), width = 25, bg = "white smoke").place(x = 355, y = 395 + i * 30)
    names.append(name_var)
    
    Label(root, text = "Symbol:", font = ("Tahoma", 11), bg = "white").place(x = 575, y = 395 + i * 30)

    image_var = StringVar()
    combobox = ttk.Combobox(root, textvariable = image_var, values = images, state = "readonly", width = 24, font = ("Calibri", 12))
    combobox.place(x = 655, y = 395 + i * 30)
    image_vars.append(image_var)

    y = 395 + i * 30

  submit_poll = Button(root, text = "Submit Poll", font = ("Tahoma", 12), command = submitpoll)
  submit_poll.place(x = 515, y = y + 40)

  reset_button = Button(root, text = " ↻ ", font = ("Calibri", 8), command = reset)
  reset_button.place(x = 868, y = 363)

canvas = Canvas(root, width=1150, height=764)
canvas.pack(fill = "both", expand = True)

image = Image.open("BACKGROUND-Poll2.png")
photo = ImageTk.PhotoImage(image)

canvas.create_image(0, 0, anchor = "nw", image=photo)

Label(root, text = "POLL MAKER", font = ("Tahoma", 16), bg = "white").place(x = 515, y = 300)
Label(root, text = "Enter the following details of the poll", font = ("Tahoma", 10), bg = "white").place(x = 465, y = 330)

Label(root, text = "Select the number of candidates/parties:", font = ("Tahoma", 12), bg = "white").place(x = 270, y = 360)
number = ttk.Combobox(root, width = 27, textvariable = no_of_candidates, font = ("Tahoma", 12))
number['values'] = ('2', '3', '4', '5', '6', '7')
number.place(x = 570, y = 363)
number.current()

select_button = Button(root, text = "✅", font = ("Calibri", 8), command = display).place(x = 840, y = 363)

symbols = Button(root, text = "Symbols Glossary", font = ("Tahoma", 10), command = display_glossary).place(x = 1037, y = 0)

root.mainloop()
