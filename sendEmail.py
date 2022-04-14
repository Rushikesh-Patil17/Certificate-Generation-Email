import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

fromaddr = "test@gmail.com"

data = pd.read_csv("test.csv")
names = data['Name'].tolist()
emails = data['Attendee Email'].tolist()

for i in range(len(names)):
	toaddr = emails[i].lower()

	# instance of MIMEMultipart
	msg = MIMEMultipart()

	# storing the senders email address
	msg['From'] = fromaddr

	# storing the receivers email address
	msg['To'] = toaddr

	# storing the subject
	msg['Subject'] = "COEP FLOSSMeet'22 Participation Certificate"
	name = names[i].title()

	# string to store the body of the mail
	body = f"Hi👋, {name}, please find attached your COEP FLOSSMeet'22 Participation Certificate!\nLet us know your experiences on our social media handles or via email. Kudos👏🙌"

	# attach the body with the msg instance
	msg.attach(MIMEText(body, 'plain'))

	# open the file to be sent
	filename = f"FLOSSMeet22 {name.upper()}.pdf"
	attachment = open(f"./pdfs/FLOSSMeet22 {name.upper()}.pdf", "rb")

	# instance of MIMEBase and named as p
	p = MIMEBase('application', 'octet-stream')

	# To change the payload into encoded form
	p.set_payload((attachment).read())

	# encode into base64
	encoders.encode_base64(p)

	p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

	# attach the instance 'p' to instance 'msg'
	msg.attach(p)

	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)

	# start TLS for security
	s.starttls()

	# Authentication
	s.login(fromaddr, "password")

	# Converts the Multipart msg into a string
	text = msg.as_string()

	# sending the mail
	s.sendmail(fromaddr, toaddr, text)

	print(f"Email: {toaddr}")
	print(f"File: {filename}")
	# terminating the session
	s.quit()
	print(f"Sent {i+1} of {len(names)}")
