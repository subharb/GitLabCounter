import requests

r = requests.get("https://git.augmentedworkforce.com/api/v3/projects/17/issues?state=closed")
r.encoding = 'ISO-8859-1'

curl --header "PRIVATE-TOKEN: Uz6PgmkmEiZ3yHvWX8D9" 