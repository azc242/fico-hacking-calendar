import calendar
from datetime import datetime, timedelta
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from python_http_client import exceptions

"""
Sends notification reminder to your email on the last business day before your
credit card billing cycle(s) is up.
"""


def send_email(event, context):
    today = datetime.now()
    cur_year = today.year
    cur_month = today.month

    days_in_month = calendar.monthrange(cur_year, cur_month)[1]

    # Set this to the FIRST day of your each billing cycle.
    BILLING_CYCLES = {
        "Discover IT": 6,
        "Chase Freedom": 1
        # Add modify or add more cards in this format 'Name': first day of billing cycle
        # Above, my Discover IT card has its first day of the cycle on the 6th of each
        # month, and my Chase Freedom's first day of each cycle falls on the first day.
    }

    def find_cycle_end_date(cycle_first_day):
        last_day = datetime(
            cur_year, cur_month, cycle_first_day, 00, 00, 00
        ) - timedelta(days=1)
        if last_day < today:
            last_day = datetime(
                cur_year, cur_month + 1, cycle_first_day, 00, 00, 00
            ) - timedelta(days=1)
        return last_day

    # Returns datetime object of the last working day of a credit card cycle.
    def find_last_working_day_of_cycle(cycle_first_day):
        last_working_day = find_cycle_end_date(cycle_first_day)
        while last_working_day.weekday() > 4:
            last_working_day = last_working_day - timedelta(days=1)
        return last_working_day

    email = "<h3>Notice(s):</h3><br/><p>"
    days_until_next_action = 32
    for card in BILLING_CYCLES:
        last_working_day_of_cycle = find_last_working_day_of_cycle(BILLING_CYCLES[card])
        last_day_of_cycle = find_cycle_end_date(BILLING_CYCLES[card])
        print(f"last day of working cycle for {card} is {last_working_day_of_cycle}")
        days_until_next_action = min(
            days_until_next_action, (last_working_day_of_cycle - today).days
        )
        if today == last_working_day_of_cycle:
            email += f"Your <b>{card}</b> credit card's billing cycle is ending tomorrow, {calendar.month_name[last_working_day_of_cycle.month]} {last_working_day_of_cycle.day}.<br><br><b>Pay off the card now to reduce utilization in your monthly statement.</b>"
        else:
            email += f"Your <b>{card}</b> credit card's billing cycle will end on {calendar.month_name[last_day_of_cycle.month]} {last_day_of_cycle.day}.<br>The last weekday before that is on {calendar.month_name[last_working_day_of_cycle.month]} {last_working_day_of_cycle.day}, or in <b>{(last_working_day_of_cycle - today).days}</b> days.<br><br>"
    email += "</p>"

    print(f"Days until next action is required: {days_until_next_action}")

    email_subject = f"{days_until_next_action} Days Until Next Billing Cycle Ends"
    if days_until_next_action == 0:  # implies that a billing cycle ends today
        email_subject = "[ACTION REQUIRED] Credit card cycle check"

    # You will need to set up your SendGrid API Key
    sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
    message = Mail(
        to_emails="YOUR EMAIL",
        from_email=Email("YOUR EMAIL", "YOUR NAME"),
        subject=email_subject,
        html_content=email,
    )
    # message.add_bcc("YOUR ALT EMAIL HERE") # Optional, note that this cannot be the same as your to_emails email

    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        # Expected 202 Accepted

    except exceptions.BadRequestsError as e:
        print(e.body)
        exit()

    except exceptions.HTTPError as e:
        print(e.body)
        exit()
