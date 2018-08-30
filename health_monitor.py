import requests, json, time, os, sys, sendgrid
from day_diff import day_check
from time import sleep
from sendgrid.helpers.mail import Email,Content,Mail

monitored_url = "https://intel-api.nowsecure.com/app/monitor?limit=1000000"
request_url = "https://intel-api.nowsecure.com/app/request"
intel_url = "https://intel.nowsecure.com/app/"


api_token = os.environ['API_TOKEN']
request_token = os.environ['REQUEST_TOKEN']
team = os.environ['TEAM']
slack_url = os.environ['SLACK_WEBHOOK']
email_token = os.environ['EMAIL_KEY']
slack_channel = os.environ['SLACK_CHANNEL']

day_limit = 2
ticket_limit = 14
support_email = "blawrence+support@nowsecure.com"
header = {"Authorization": "Bearer " + api_token}
request_header = {"Authorization": "Bearer " + request_token}





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
            request_analysis = requests.post(request_url, headers=request_header, data={"name":app['package_name'], "platform": app['platform_id']} )
            if request_analysis.status_code > 201:
                send_slack_message({
                    "channel": slack_channel,
                    "text":"Error requesting new analysis of " + app['package_name'],
                    "attachments": [
                        {
                            "text": request_analysis.text
                        }
                    ],
                })
            if day_check(app['latest_release_date']) > ticket_limit:
                send_ticket = True
                if os.path.isfile('./requests.json'):
                    with open("./requests.json", "r") as json_file:  
                        json_data = json.load(json_file)
                        json_file.close()
                else:
                    json_data = []
                for app_archive in json_data:
                    if app_archive['package_name'] == app['package_name'] and app_archive["latest_published_version"] == app["latest_published_version"] and app['platform_id'] == app_archive['platform_id']:
                        send_ticket = False
                        break
                if send_ticket:
                    send_support_ticket(app['package_name'], app["platform_id"], app["latest_published_version"],app['title'])
                    json_data.append({"package_name": app["package_name"], "platform_id": app["platform_id"], "latest_published_version": app["latest_published_version"]})
                    with open("./requests.json","w+") as json_file:
                            json.dump(json_data,json_file)
                       

        x+=1
    if problems:
        slack_data = {
            "channel": slack_channel,
            "text":"Attention " + team + " Team: There are apps in Intel which have new versions that have not gotten a new assessment for over 48 hours. New analysis has been requested automatically for all apps.",
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": "ff0000",
                    "pretext": "Analysis has been requested automatically for these apps:",
                    "text": problems
                }
            ],
            "footer": "<!date^" + str(int(time.time())) + "^{date} at {time}|Error reading date>"
        }
        send_slack_message(slack_data)
       
def send_support_ticket(app_package, app_platform, app_version, app_title):
    sg = sendgrid.SendGridAPIClient(apikey=email_token)
    from_email = Email("noreply@nowsecure.com")
    to_email = Email(support_email)
    subject = "Intel App in need of attention for client " + team
    content = Content("text/plain", "Hello Support team, the app " + app_title + " (" + app_package + "), version: " + str(app_version) + "for " + app_platform + " is being monitored by " + team + " and has released a new version over two weeks ago that still does not have a complete report. This is an automated ticket for us to look into and take appropriate action for that app/client. Please note that repeat analysis has likely been requested for this app multiple times already. Thanks!")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("Response to sending email regarding + " + app_package + " was " + response.status_code)
    #print(response.body)
    

def send_slack_message(message):
    r4 = requests.post(slack_url, json=message)
    if r4.status_code != 200:
        print "Error sending message! " + r4.text
    else:
        print "Message sent successfully"


while True:
    monitored_pull()
    sleep(86400*2)

