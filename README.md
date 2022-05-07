# FICO Hacking Calendar
## What is this?
A calendar file you can import to Google Calendar or Calendar that sets up a recurring event on the last weekday of each month, which is typically before the billing cycle closes and your credit card finalizes your billing statement.

*Note that this will only work if your billing cycle does not end before the month is up. To my knowledge, it is not possible to set a recurring calendar event that occurs on the last weekday before the nth day of a month.*
## What's the purpose of this anyways?
To maximize the utilization section of your credit score, it is best to practice the $2/$3 rule (TL;DR: Have a little usage as possible while still being registered as having some usage. $2 is the sweet spot for most credit cards, but some like Discover will count $2 as having no overall usage in the billing cycle, so we use $3 for such cards).

> Your billing cycles might look like this: 
> 
> Days 1-28: Use card normally
> 
> Day 29: Pay off entire balance minus $3 
> 
> Day 30: End of statement, statement balance will be $3 
> 
> Day 31: Pay off $3 statement balance, go back to Day 1 and start over.
> 
> [Franholio](https://www.reddit.com/r/churning/comments/c7u1uv/comment/esixe7t/?utm_source=share&utm_medium=web2x&context=3) via Reddit

## How to use the `.ical` file
You should only use this if your billing cycles across all your cards ends on the last day of the month. 
This calendar file, once imported into your calendar, will set up a reminder that falls on **the last *weekday* of each month**.
## How to use the Python script
If the `.ical` isn't useful for you, this option is for you. I personally use this because my credit cards end their cycles on different dates. 

Note that before using the script, please set up your billing cycles and cards in the `BILLING_CYCLES` dictionary in `reminder.py`. In addition, fill in your email details, as the default values will not work. 

I scheduled my Python (3.8) script to run as a cron job using Google Cloud Platform. You can set this up on a local machine without GCP, but your machine will need to be running when the cron job is scheduled (unless you use anacron). 

The frequency fo the cron job should be `0 9 * * *`, which will run the script daily at 9AM of whichever time zone you select in the GCP configuration. Alternatively, you can use `0 9 * * 1-5` to run this only on weekdays, which is what I have selected. Then, you'll only receive emails on weekdays.

#### GCP Setup Pt.0 (Setting Up a Free Tier Account)
Follow [the documentation](https://cloud.google.com/free) and create a free tier GCP account.
Then, create a GCP project. Any name will do. I just named mine "credit card reminder" or something along those lines. 
#### GCP Setup Pt.1 (Cloud Functions)
Go into the GCP Console and make sure you're using the project you just created by looking on the top left banner next to the Google Cloud Platform logo/text. Next, create a Cloud Function. 

<u>Basics</u>
1. Choose the first gen environment 
2. You can give the function any name
3. For the region just select whichever region is closest to your location (or not, it won't make a noticeable difference for this project).

<u>Trigger</u>
1. Use `Cloud Pub/Sub` for the trigger type
2. Create a generic topic to use. I left all 3 options unchecked (schema,message retention duration, customer managed encryption key). Whether or not you select the retry on failure option is up to you. I personally selected it.

<u>Adding environment variables</u>
1.  Activate a plan on  [GCP marketplace](https://console.cloud.google.com/marketplace/details/sendgrid-app/sendgrid-email)  ( I use free plan, 12K mails/month)
2.  [Create an api key in sendgrid](https://app.sendgrid.com/settings/api_keys)
3.  Validate your sendgrid account email (use the email that you received)
4. Expand the "Runtime, build, connection and security" section and click "Add Variable". Name should be "SENDGRID_API_KEY" and Value should be your SendGrid API Key.

<u>Code Source</u>
1. Use `Python 3.8` and have the entry point be `send_email`. 
2. Update [`BILLING_CYCLES`](https://github.com/azc242/fico-hacking-calendar/blob/main/reminder.py#L22) and the [sender/recipient email addresses](https://github.com/azc242/fico-hacking-calendar/blob/main/reminder.py#L66) (the `to_emails` and `from_email` fields. 
3. Paste the `reminder.py` file into the `main.py` section.
4. In the `requirements.txt`, add `sendgrid` into it. 
 
#### GCP Setup Pt.2 (Cloud Schedule)
<u>Define The Schedule</u>
1. Go to the Cloud Scheduler console and select "Create Job" and give the job any name, description, and timezone.
2.  The region should be what region your function is in, and set the frequency to `0 9 * * *`, which will run the script daily at 9AM of whichever time zone you select in the GCP configuration. Alternatively, you can use `0 9 * * 1-5` to run this only on weekdays, which is what I have selected. Then, you'll only receive emails on weekdays.

<u>Configure the Execution</u>
Use a Pub/Sub type and use whichever topic you created earlier. The message can be anything arbitrary as long as it's not empty. We won't be using this field.

<u>Configure optional settings</u>
Set retries to `1`, and use the defaults for everything else.

#### Etc.

Note that this script currently sends an email each day as a sanity check that it runs properly. However, you can disable this simply by indenting the code block after `if  days_until_next_action == 0:` so that it is a part of the `if` statement. Then, it will only send when action is required (AKA when it is the last weekday day before your credit card provider calculates your statement).