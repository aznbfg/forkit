#!/usr/bin/python3

"""
Webserver to ForkIt!
"""

from urllib.parse import parse_qs
import configargparse
from flask import Flask, redirect, request
import requests
import yaml


app = Flask(__name__)
CLIENT_ID = None
CLIENT_SECRET = None


@app.route("/")
def hello():
    """Index Page with greeting"""
    body = "<h1>Welcome to Fork It!</h1>"
    body += "<h2>Fork It! will fork this github repo into your github account.</h2>"
    body += "<h2>Click <a href='/startfork'> here to forkit!</a></h2>"
    body += "<img src='https://upload.wikimedia.org/wikipedia/en/6/6e/Forky_waving.png'>"
    return body


@app.route("/startfork")
def startfork():
    """Begins fork process, sends oauth request"""
    redirect_url = 'https://github.com/login/oauth/authorize?client_id=' + \
                   f'{CLIENT_ID}&scope=repo'
    return redirect(redirect_url)


@app.route("/callback")
def callback():
    """Callback for oauth request"""
    code = request.args.get("code")
    auth_request = requests.post("https://github.com/login/oauth/access_token",
                                 data={"client_id": CLIENT_ID,
                                       "client_secret": CLIENT_SECRET,
                                       "code": code})
    auth_content = parse_qs(auth_request.content)
    auth_token = auth_content.get(b'access_token')
    if auth_token is None:
        return "Invalid request, contact michael.mileusnich@gmail.com", 500
    auth_token = auth_token[0].decode('utf-8')
    return redirect(f"/fork?auth_token={auth_token}")


@app.route("/fork")
def fork():
    """Last step of the fork process"""
    auth_token = request.args.get("auth_token")
    repo = "forkit"
    url = f'https://api.github.com/repos/justmike2000/{repo}/forks'
    fork_req = requests.post(url,
                             headers={'Authorization': f'token {auth_token}',
                                      'Content-Type': 'application/json'})
    if fork_req.status_code >= 200 and fork_req.status_code < 300:
        return "Forked!  Check your github!"
    print(fork_req.__dict__)
    return "Unknown error, contact michael.mileusnich@gmail.com"


if  __name__ in ["__main__", "uwsgi_file_app"]:
    cma = configargparse.ArgParser()
    cma.add('-c', '--config', required=False,
            default='default_settings.yaml',
            help='config file path')
    options = cma.parse_args()
    yaml_config = yaml.load(open(options.config).read())
    CLIENT_ID = yaml_config.get("github").get("client_id")
    CLIENT_SECRET = yaml_config.get("github").get("client_secret")
    print(CLIENT_ID)

    if __name__ == "__main__":
        app.run()
