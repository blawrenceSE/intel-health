# Intel health

Checks an org's monitored Intel apps, then notifies via Slack with URL's of any app that has a release more than ~2 days old and no current report.

Current slack webhook goes to SE test Slack team.

`docker build .`
`docker run -d -e PYTHONUNBUFFERED=0 --name <client or name>`

Build and run the Docker container. Once running, you must set and export environment variables:

API_TOKEN - the token for the account you are monitoring
TEAM - the account team that needs to be notified
SLACK_WEBHOOK - the slack url to push messages
REQUEST_TOKEN - internal token for requesting fresh analysis
EMAIL_KEY - Key to send e-mails
SLACK_CHANNEL - where to send messages

