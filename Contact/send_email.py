from flask import Flask, request
from decouple import config
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def send_email():
    name = request.form['name']
    sender_email = request.form['email']
    message = request.form['message']

    email = EmailMessage()
    email['Subject'] = f"New message from {name}"
    email['From'] = sender_email
    email['To'] = config("EMAIL_HOST_USER")  # Send to your Gmail address
    email.set_content(message)

    try:
        with smtplib.SMTP(config('EMAIL_HOST'), config('EMAIL_PORT')) as smtp:
            smtp.starttls()
            smtp.login(config("EMAIL_HOST_USER"), config("EMAIL_HOST_PASSWORD"))
            smtp.send_message(email)
        return 'Email sent successfully'
    except Exception as e:
        return f'Failed to send email: {str(e)}'

if __name__ == "__main__":
    print('Email host is', config('EMAIL_HOST'))
    app.run(debug=True)

