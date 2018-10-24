# Intel health

Checks an org's monitored Intel apps, then notifies via Slack with URL's of any app that has a release more than ~2 days old and no current report.

Current DOCKERFILE has bash but probably does not need to.

API_TOKEN - the token for the account you are monitoring
TEAM - the account team that needs to be notified
SLACK_WEBHOOK - the slack url to push messages
REQUEST_TOKEN - internal token for requesting fresh analysis
EMAIL_KEY - Key to send e-mails
SLACK_CHANNEL - where to send messages
