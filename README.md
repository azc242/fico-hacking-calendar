# FICO Hacking Calendar
### What is this?
A calendar file you can import to Google Calendar or Calendar that sets up a recurring event on the last weekday of each month, which is typically before the billing cycle closes and your credit card finalizes your billing statement.

*Note that this will only work if your billing cycle does not end before the month is up. To my knowledge, it is not possible to set a recurring calendar event that occurs on the last weekday before the nth day of a month.*
### What's the purpose of this anyways?
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

### How to use the script
I scheduled my Python (3.8) script to run as a cron job using Google Cloud Platform. You can check out a good guide on how to set this all up [for free here using GCP](https://towardsdatascience.com/how-to-schedule-a-python-script-on-google-cloud-721e331a9590). The frequency fo the cron job should be `0 9 * * *`, which will run the script daily at 9AM of whichever time zone you select in the GCP configuration.
Note that this script currently sends an email each day as a sanity check that it runs properly. However, you can disable this simply by indenting the code block containing so that it is a part of the preceding `if` statement. Then, it will only send when action is required (AKA when it is the last weekdat day before your credit card provider calculates your statement).
```
msg.attach(MIMEText(email, 'html'))
server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(fromaddr, 'YOUR EMAIL PASSWORD HERE')
text = msg.as_string()
server.sendmail(fromaddr, [msg['To']], text)
server.close()
```

Note that before using the script, please set up your billing cycles and cards in the `BILLING_CYCLES` dictionary in `reminder.py`. In addition, fill in your email details, as the default values will not work. 