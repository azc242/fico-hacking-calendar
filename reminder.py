import calendar
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

'''
Sends notification reminder to your email on the last business day before your
credit card billing cycle(s) is up.
Note that the sender email MUST be a gmail address.

If you do not use Gmail, change the following line:
server = smtplib.SMTP("smtp.gmail.com", 587)
Find out the appropriate values for your email service with a quick Google search.

You'll also need to allow less secure apps for Gmail or your email service if authentication fails
https://myaccount.google.com/lesssecureapps
'''

def send_email():
    msg = MIMEMultipart()
    fromaddr = 'YOUR EMAIL HERE'
    password = 'fromaddr EMAIL PASSWORD HERE'
    msg['From'] = fromaddr
    msg['To'] = 'YOUR EMAIL HERE'
    msg['Subject'] = "Daily credit card cycle check"

    today = datetime.now()
    cur_year = today.year
    cur_month = today.month

    days_in_month = calendar.monthrange(cur_year, cur_month)[1]

    # Set this to the FIRST day of your each billing cycle.
    BILLING_CYCLES = {
    'Discover IT': 4,
    'Chase Freedom': 1
    # Add modify or add more cards in this format 'Name': first day of billing cycle
    # Above, my Discover IT card has its first day of the cycle on the 3th of each
    # month, and my Chase Freedom's last day of each cycle falls on the first day.
    }

    # Returns datetime object of the last working day of a credit card cycle.
    def find_last_working_day_of_cycle(cycle_first_day):
        last_working_day = datetime(cur_year, cur_month, cycle_first_day, 00, 00, 00) - timedelta(days = 1)
        while last_working_day.weekday() > 4:
            last_working_day = last_working_day - timedelta(days = 1)
            print("test")
        return last_working_day

    email = "Notice(s):<br/><br/><p>"
    action_needed = False
    for card in BILLING_CYCLES:
        if today == find_last_working_day_of_cycle(BILLING_CYCLES[card]):
            email += "Your <b>{credit_card}</b> credit card's billing cycle is ending tomorrow<br><br>".format(credit_card = card)
            action_needed = True
        else:
            email += "Your <b>{credit_card}</b> credit card's billing cycle will end on day {end_date} of each month.<br><br>".format(credit_card = card, end_date = BILLING_CYCLES[card])
    email += "</p>"

    if action_needed:
        msg['Subject'] = '[ACTION REQUIRED] Credit card cycle check'

    msg.attach(MIMEText(email, 'html'))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, [msg['To']], text)
    server.close()

    print("Email sent successfully!")

send_email()
