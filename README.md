# Slack notifier for Shippable

Simple Slack notifier for Shippable.

# Usage

* Setup a Slack channel
* Go to http://YOUR_ORG_NAME.slack.com/admin, sign in
* Click *Add* button near "Incoming WebHooks" integration listed in the "All services" tab
* Select desired channel for notifications, confirm
* Copy `/services/ABCDEFGH/IJKLMNOP/12312312312312312321` part of *Webhook URL* information
* Enable your project in Shippable
* Go to the org dashboard or individual dashboard page from where you have enabled your project and click on ENCRYPT ENV VARIABLE button on the top right corner of the page. ([More info...](http://docs.shippable.com/en/latest/config.html#secure-env-variables))
* Enter the following into the text field: `SLACK_URL=/services/ABCDEFGH/IJKLMNOP/12312312312312312321` where `/services/ABCDEFGH/IJKLMNOP/12312312312312312321` was obtained before, click *Encrypt*
* Copy the encrypted variable code that will appear 
* Paste it into your `shippable.yml` in your *env* section
* Add the following code to your `shippable.yml`:
    
```
after_failure:
  - sudo apt-get install wget -y; wget -O /tmp/notify.py http://mspanc.github.io/shippable-slack-notifier/notify.py; python /tmp/notify.py --slack-url $SLACK_URL --message failure
after_success:
  - sudo apt-get install wget -y; wget -O /tmp/notify.py http://mspanc.github.io/shippable-slack-notifier/notify.py; python /tmp/notify.py --slack-url $SLACK_URL --message success
```

# License

MIT

# Authors

Marcin Lewandowski
