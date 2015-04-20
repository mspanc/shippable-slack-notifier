import httplib, json, argparse, sys, os, subprocess

def get_data_from_git(format_string, commit):
  return subprocess.check_output(['git', 'log', '-1', '--format=format:%s' % format_string, commit])

def get_author(commit):
  return get_data_from_git('%an <%ae>', commit)

def get_date(commit):
  return get_data_from_git('%aD', commit)

def get_title(commit):
  return get_data_from_git('%s', commit)

def get_full_message(commit):
  return get_data_from_git('%b', commit)

def post_message(connection, url, success):
  headers = {'Content-Type': 'application/json'}
  build_url = os.environ['BUILD_URL']
  build_number = os.environ['BUILD_NUMBER']
  branch = os.environ['BRANCH']
  commit = os.environ['COMMIT']
  project = os.environ['REPO_NAME']

  status_text = 'succeeded' if success else 'failed'
  color = 'good' if success else 'danger'
  emoji = ':ok_hand:' if success else ':fire:'
  text = '<%s|Build #%s> %s for project %s on branch %s' % (build_url, build_number, status_text, project, branch)

  message = {
    'username': 'Shippable',
    'fallback': text,
    'pretext': text,
    'icon_emoji': emoji,
    'color': color,
    'fields': [
      {
        'title': get_author(commit),
        'value': get_date(commit)
      },
      {
        'title': get_title(commit),
        'value': get_full_message(commit)
      }
    ]
  }

  connection.request('POST', url, json.dumps(message), headers)
  response = connection.getresponse()
  print response.read().decode()

def main():
  parser = argparse.ArgumentParser(description='Slack notifier for Shippable.')
  parser.add_argument('--slack-url', help='URL for Slack webhook (e.g. /services/ABCDEFGH/IJKLMNOP/12312312312312312321)', required = True)
  parser.add_argument('--message', help='Type of message to send', required = True, choices = [ "success", "failure" ])
  parser.print_help()

  args = parser.parse_args(sys.argv[1:])

  connection = httplib.HTTPSConnection('hooks.slack.com')
  post_message(connection, args.slack_url, args.message == "success")

if __name__ == '__main__':
  main()
