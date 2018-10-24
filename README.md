# Intel health

- Checks an org's monitored Intel apps
- Notifies via Slack with URL's of any app that has a release more than `day_limit` days old and no current report
- Automatically requests a re run of the app (~40% success rate?)
- If an app has gone a certain number of days (set by `ticket_limit`) will then send an email to support to create a ticket.

Current DOCKERFILE has bash but probably does not need to.

API_TOKEN - the token for the account you are monitoring
TEAM - the account team that needs to be notified
SLACK_WEBHOOK - the slack url to push messages
REQUEST_TOKEN - internal token for requesting fresh analysis
EMAIL_KEY - Key to send e-mails
SLACK_CHANNEL - where to send messages
