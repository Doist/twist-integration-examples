# Long Running Task Python Sample

This is a code sample demonstrating how to perform a long running task when dealing with bots in Twist.

To run this sample we will need to setup and configure a few things:
- [ngrok](https://ngrok.com/) to forward the Twist calls to your local server
- An integration on Twist
- A Flask server to run the server code

## Setup ngrok

In order for your integration to work, Twist needs to know where to send the command/bot data, and for this, you will need a running web server. Whilst you're developing your integration, you may not have a dedicated web server setup for this, and you just want to point to your local machine, this is where [ngrok](https://ngrok.com/) comes in as it can forward the call to your local server. Head to the [ngrok download page](https://ngrok.com/download) to get that installed.

Once installed, you can simply call
```
ngrok http 5000
```

This will start a session that points to port 5000.
![](../images/ngrok.jpg)

Make a note of the second forwarding URL (in the example, https://4ecc43da.ngrok.io) as we will need this in the next step.

## Setup your integration

To create your integration, go to https://twist.com/integrations/build and click the `Add a new integration` button.

Once you've given it a name and a description, press `Create my integration`; for this sample we will mainly look at Bots. If you go to the Bot section, enter the details of your bot like below

![](../images/bot_config.jpg)

It's here you need that ngrok URL from earlier, enter that into the Request URL with `/bot` at the end as that's the endpoint we are using in the code. Your integration may be different.

Once all that is done and saved, click on `Installation`, make sure you are in the right Twist workspace, and click `Install integration`.

## Setup Flask to run as server

Before your integration will work, you need to have a server up and running. 

We're using Flask in this example, but you can use any other setup you're more familiar with. 

Make sure you have Flask installed
```
pip install flask
```

Once you're in the `server.py` directory, it's a simple case of running
```
FLASK_APP=server.py flask run
```

With that complete, you can now go to a conversation with the bot and type something like "hello bot" and it will reply to you.
![](../images/bot_chat.jpg)