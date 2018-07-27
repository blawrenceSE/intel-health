import requests, json, time, os, sys
from day_diff import day_check
from time import sleep

monitored_url = "https://intel-api.nowsecure.com/app/monitor?limit=1000000"
api_token = os.environ['API_TOKEN']
team = os.environ['TEAM']
day_limit = 2
header = {"Authorization": "Bearer " + api_token}
intel_url = "https://intel.nowsecure.com/app/"
slack_url = os.environ['SLACK_WEBHOOK']
slack_channel = "#general"


def monitored_pull():
    r = requests.get(monitored_url, headers=header)
    monitored_apps = json.loads(r.text)
    x = 0
    #problems = []
    problems = ""
    for app in monitored_apps:
        if app['latest_published_version'] != app['latest_report_release_version'] and day_check(app['latest_release_date']) > day_limit:
            app_url = intel_url + app['platform_id'] + "/" + app['package_name'] + "/"
            sys.stdout.write('Found problem app: ' + app_url + '\n')
            problems = problems + app_url + "\n"
        x+=1
    if problems:
        slack_data = {
            "channel": slack_channel,
            "text":"Attention " + team + " Team: There are apps in Intel which have new versions that have not gotten a new assessment for over 48 hours.",
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": "ff0000",
                    "pretext": "These are the apps that are out of date and should probably be investigated:",
                    "text": problems
                }
            ],
            "footer": "<!date^" + str(int(time.time())) + "^{date} at {time}|Error reading date>"
        }
        send_slack_message(slack_data)
       

def send_slack_message(message):
    r4 = requests.post(slack_url, json=message)
    if r4.status_code != 200:
        print "Error sending message! " + r4.text
    else:
        print "Message sent successfully"


while True:
    monitored_pull()
    sleep(86400*2)

