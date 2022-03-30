#howdy Mau
import sys
import getopt
import urllib.parse
import json
import http
import base64
import http.client
base_url="https://api.github.com/repos/"

def github_request(method, url,github_token, headers=None, data="", params=None):
    """Execute a request to the GitHUB API, handling redirect"""
    if not headers:
        headers = {}
    headers.update({
        "User-Agent": "Agent 007",
        "Authorization": "Bearer " + github_token,
    })

    url_parsed = urllib.parse.urlparse(url)
    url_path = url_parsed.path
    if params:
        url_path += "?" + urllib.parse.urlencode(params)

    data = data and json.dumps(data)

    conn = http.client.HTTPSConnection(url_parsed.hostname)
    conn.request(method, url_path, body=data, headers=headers)
    response = conn.getresponse()
    print(response.status)
    if response.status == 302:
        return github_request(method, response.headers["Location"])
        
    if response.status >= 400:
        headers.pop('Authorization', None)


    return response, json.loads(response.read().decode())
    

def check_to_github(repository, github_token, branch):
    # Get last commit SHA of a branch
    resp, jeez = github_request("GET", f"{base_url}{repository}/git/{branch}",github_token)
    last_commit_sha = jeez["object"]["sha"]
    print("Last commit SHA: " + last_commit_sha)
    resp, jeez = github_request(
        "POST",
        f"{base_url}{repository}/git/check-runs",github_token,
        data={
            "name": "Lint Annotations",
            "head_sha": last_commit_sha,
            "conclusion":'failure',
            "output":[{
                    "title":"lint Annotations",
                    "summary":"failure lint validation"
            }]
        },
    )
if __name__ == "__main__":
    check_to_github("mauricioobgo/runners-test","the personnal token","refs/heads/git-api")