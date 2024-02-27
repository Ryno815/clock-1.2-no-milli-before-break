from flask import Flask, request, redirect,session
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


app = Flask(__name__)
app.secret_key = 'HEHEHEHAHEHEHEHA'



def generate_verification_code():
  return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def send_verification_email(email, verification_code):
    # Email configurations
    sender_email = 'gikisclock@gmail.com'  # Update with your email address
    sender_password = 'pctadtawbvdmqfxr'  # Update with your email password
    smtp_server = 'smtp.gmail.com'  # Update with your SMTP server address
    smtp_port = 587  # Update with your SMTP port number

    # Create a message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'Account Verification Code'

    # Create the body of the email
    body = f'Your verification code is: {verification_code}. Do not share this code with anyone, especially Vraj.'

    # Attach the body to the message object
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


@app.route('/')
def index():
  if 'logged_in' in session:
    f=open("private.html","r")
    page=f.read()
    f.close()
    return page
  else:
    return redirect('/public')
 

@app.route('/public')
def public():
  f=open("index.html","r")
  page=f.read()
  f.close()
  return page

  
@app.route("/nope")
def nope():
  f=open ("nope.html","r")
  page=f.read()
  f.close()
  return page

@app.route("/success")
def success():
  f=open ("success.html","r")
  page=f.read()
  f.close()
  return page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open("nothing.txt", "r") as file:
          users_data = file.readlines()

        for user_data in users_data:
            user_info = user_data.strip().split(',')
            if username == user_info[0] and password == user_info[1]:
                session['logged_in'] = True
                session['username']=username
                return redirect('/')

        return redirect('/public')

    else:
      return redirect('/public')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

   
@app.route('/create')
def create():
  f=open("create.html","r")
  page=f.read()
  f.close()
  return page

@app.route('/submit_account', methods=['POST'])
def submit_account():
    username = request.form['username']
    email=request.form['email']
    password = request.form['password']

    with open("nothing.txt", "r") as file:
        users_data = file.readlines()

        for user_data in users_data:
            user_info = user_data.strip().split(',')
            if username == user_info[0] or email == user_info[2]:
              f=open("existing.html","r")
              page=f.read()
              f.close()
              return page
            

    verification_code = generate_verification_code()
    session['verification_code'] = verification_code
    session['username']=username
    session['email']=email
    session['password']=password
    send_verification_email(email, verification_code)
    print(f"Email sent to {email}")
   

    # Process the submitted data (e.g., store it in a database)
    f=open("verify.html","r")
    page=f.read()
    f.close()
    return page



@app.route('/verify_code', methods=['POST'])
def verify_code():
    
    generated_code = session.get('verification_code')
    username = session.get('username')
    email = session.get('email')
    password = session.get('password')

    print (f"Code for {email} is {session['verification_code']}")

   
    generated_code = session.get('verification_code')

    submitted_code = request.form.get('verification_code')
    if generated_code != submitted_code:
        
        new_user_data = f"{username},{password},{email},NOPE\n"
        with open("nothing.txt", "a") as file:
            file.write(new_user_data)
        return redirect('/nope')
    
        
    new_user_data = f"{username},{password},{email},SUCCESS\n"
    with open("nothing.txt", "a") as file:
      file.write(new_user_data)

    profiles_dir = os.path.join(os.getcwd(), 'profiles')
    profile_filename = os.path.join(profiles_dir, f"{username}.txt")
    with open(profile_filename, "w") as file:
        file.write(f"Username: {username}\n")
        file.write(f"Password: {password}\n")
        file.write(f"Email: {email}\n")

    return redirect ('/success')




@app.route('/create_preset', methods=['POST'])
def create_preset():
    # Get the current font and color being used
    current_font = request.form.get('current_font')
    current_color = request.form.get('current_color')


    username = session.get('username')  

    if username:
        # Construct the path to the user's profile data file
        profile_filename = os.path.join(os.getcwd(), 'profiles', f"{username}.txt")

        # Write the current font and color to the user's profile data file
        with open(profile_filename, "a") as file:
            file.write(f"Font: {current_font} Color: {current_color}\n")


    # Redirect back to the homepage
    return redirect('/')


app.run(host='0.0.0.0', port=81)

