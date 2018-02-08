# Compare Vision API's

This is a simple webapp for showing how various image classification API's perform on specific tasks or categories of tasks. Currently setup to run on Google App Engine (GAE)
Some dependencies not installed, so prior to running or deploying, add a the necessary pyton packages using pip:

`pip install -r requirements.txt -t lib`


## Note on HTTPS while using dev_appserver.py
The GAE development server hosts your app at localhost and serves requests over HTTP. This causes issues for testing 3rd party API calls. To solve this, use NGINX to run a reverse proxy. [This guide](https://ericbidelman.tumblr.com/post/150410248401/using-http2-for-app-engine-local-development) was hepful.

