#!/bin/bash
# This script checks if it is the right time to send an email reminder to your email.
# It sends an email if it is the last weekday on or before the specified day of the month, REMINDER_DATE.
# your email here
TO="azc242@nyu.edu"
# defaults to remind on the last weekday on or before the 3rd of each month
# valid range: [1,31]
reminder_date=3

days_in_month=$(cal $(date +"%m %Y") | awk 'NF {DAYS = $NF}; END {print DAYS}')
echo "$days_in_month"
echo "$reminder_date"
if [ "$reminder_date" -ge 0 ] && [ "$reminder_date" -le 31 ]; then
    echo "INFO: Valid reminder date."
else
    echo "ERROR: Invalid reminder date."
fi

if [ "$reminder_date" -gt "$days_in_month" ]; then
    reminder_date=$days_in_month
    echo "Days in month: $days_in_month"
fi