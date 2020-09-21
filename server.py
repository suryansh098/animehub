from flask import Flask, render_template, url_for, request, redirect
import csv
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
	with open('database.txt', mode='a') as database:
		email = data["email"]
		subject = data["subject"]
		message = data["message"]
		file = database.write(f'\n{email}, {subject}, {message}')

def write_to_csv(data):
	with open('database.csv', mode='a', newline='') as database2:
		email = data["email"]
		subject = data["subject"]
		message = data["message"]
		csv_writer = csv.writer(database2, delimiter=",", quotechar='"',quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([email, subject, message])

def thanks_giving(mail):
	email = EmailMessage()
	email['from'] = 'Animehub'
	email['to'] = mail
	email['subject'] = 'Thanks Giving !'
	email.set_content('Thank you for review mate! I hope you liked the website, stay connected for future updates.\n\nTeam Animehub')
	try:
		with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
			smtp.ehlo()
			smtp.starttls()
			smtp.login('your_email', 'your_password')
			smtp.send_message(email)
			print('All Good')
	except Exception as e:
		print(e)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
	if request.method == 'POST':
		data = request.form.to_dict()
		print(data)
		write_to_csv(data)
		thanks_giving(data["email"])
		return redirect('/thank_you.html')
	else:
		return 'something went wrong'

if __name__ == "__main__":
	app.run()