# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask
import os
from google.cloud import datastore

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

dataclient = datastore.Client()


@app.route('/')
def hello():
    addVisitor()
    """Return a friendly HTTP greeting."""
    return 'Hello World! Daniel Strauch 300206805'

@app.route('/version')
def versA():
    addVisitor()
    return 'This is app version B!'

@app.route('/instance')
def getid():
    addVisitor()
    instanceid = os.getenv('GAE_INSTANCE')
    return str(instanceid)

@app.route('/version-id')
def getversionid():
    addVisitor()
    versionid = os.getenv('GAE_VERSION')
    return str(versionid)

def addVisitor():
    ent = dataclient.key('data', 'visitor')
    total = dataclient.get(key=ent)
    if total:
        total['total'] += 1
        dataclient.put(total)
    else:
        total = datastore.Entity(key=ent)
        total['total'] = 0
        dataclient.put(total)

@app.route('/visitors')
def getVisitor():
    addVisitor()
    ent = dataclient.key('data', 'visitor')
    total = dataclient.get(key=ent)
    if total:
        return 'Total visitors: '+ str(total['total'])
    else:
        return 'Visitor Broken!'

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
