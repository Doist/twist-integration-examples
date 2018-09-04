Appear.in with Go
====================

This is a simple implementation of a slash integration to create a link
to [appear.in](https://appear.in) when the slash command is called with an
argument.

Usage
-----

`/slash username`

Will change the text to `https://appear.in/username`

Implementation
--------------

It uses Go to implement a simple server to listen to the requests.

To get it up and running you have to [install go](https://golang.org/) and run the server, no external packages are needed:

    go run main.go

It should run the server and display some debugging information like this:

    2018/08/28 23:19:30 Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

Testing the integration 
-----------------------

We recommend to use [ngrok](https://ngrok.com) to tunnel external requests to
your own local server. It already provides HTTPS for your integration out of the
box. Please read [their documentation](https://ngrok.com/docs) to know how to
install and configure it.

When installed, run it pointing to the port your server is running:

    ngrok http 5000

It will give you the https address to use as your **Outgoing webhook URL** (you
can create it [here](https://twistapp.com/integrations/build)).
