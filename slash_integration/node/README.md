# Slash Integration with Node and Express

## Prerequisites
You'll need to ensure that [Node.js](https://node.js) is installed on your machine and you can download the latest LTS/Current version or by using [Homebrew](https://brew.sh)/[Chocolatey](https://chocolatey.org).

We'll also be using ngrok (https://ngrok.com/) for this project. You can elect to install this via `npm` or by other methods.

## New Project
Start off by creating a new Node.js and Express application.

To create a new Node project, run the following in your terminal:

```bash
# Create a new directory
$ mkdir appear-in-slash

# Change directory
$ cd appear-in-slash

# Initiate a new Node project
$ npm init -y

# Create a server.js file
$ touch server.js

# Install the required dependencies
$ npm install express body-parser --save
```

## Server Setup

We can then set up a listen server with Express:

```javascript
const express = require('express');
const bodyParser = require('body-parser');

const app = express();

// Parse POST requests with JSON or URLEncoded
app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  }),
);

app.listen(process.env.PORT || 3000, () =>
  console.log(`Server listening on port ${process.env.PORT || 3000}`),
)
```
### Nodemon
At this point, we can run our Node application using `nodemon`. This means any changes to our JavaScript will restart our Node server, allowing for a much smoother development experience:

```bash
# Install nodemon globally
$ npm install nodemon -g

# Run our server with nodemon.
$ nodemon server.js
```

Next, we'll define a new route that our webhook will point at:

```javascript
app.post('/appear', (req, res) => {
  console.log(req)
});
```

We'll need to expose our application and create an integration based on user events. This means we'll need to use `ngrok` and create an integration over at [Twist](https://twistapp.com).

# Twist Integration
## Create a New Integration

Navigate to https://twistapp.com and select 'Add Integrations' from the top-right drop down menu. Next, select 'Build' from the navigation menu and then 'Add New Integration'.

We can then add an integration name and description:

**Integration name**

appear.in


**Description**

Allows a user to create a new appear.in room with a slash command.

**Integration type**

Slash command integration

This allows us to create a new Integration that can listen for slashes when installed. Click 'Create my integration' to continue.

On the integration overview screen we can create a **Slash command** that can be used to invoke this integration. As our example involves [appear.in](https://appear.in), we can give this the command of `/appear`.

## Exposing a URL
We now have an application on Twist but no exposed URL, for this we'll use `ngrok`. There are numerous ways to install `ngrok`, but perhaps the easiest for Node environments is via `npm`.

### Install `ngrok` globally

```
$ npm install ngrok -g
```

Using a new terminal window (with our server running) run the following command:

```$ ngrok http 3000```

This starts a HTTP tunnel on based on our Node application that's running on port `3000`.

Copy the forwarding URL from your terminal, this will be different each time the `ngrok` command is ran. We can then place this inside of our Twist Integration under the 'Outgoing webhook URL' inside of the Webhook section.

Ensure you use the HTTPS link and add the `/appear` route, for example, `https://53325f4d.ngrok.io/appear`.

# Installing the Integration

At this point it'd be a good idea to install the integration onto our own account for testing. It still doesn't do anything *as we have yet to actually write it*, but as any changes we make locally will now be reflected to our integration with `ngrok`.

To install the integration, select Installation 🚀 and then 'Install integration' on your own account.

We can then head to a channel to test our integration by typing `/appear`. You should then be able to see both the logged request from `Node` and the POST request via `ngrok` in the respective terminal windows.

We can do what we want with this information, but as we're looking to create a new room with a slash command (such as `/appear paul`) we need access to the `command_argument` from the `req.body`.

Here's an example of what you can expect:
```javascript
{ 
  user_id: '12345',
  workspace_id: '1234',
  channel_id: '12345',
  comment_id: '12345',
  content: '/appear paul',
  thread_id: '12345',
  command: '/appear',
  thread_title: 'hi',
  command_argument: 'paul',
  user_name: 'Paul H.',
  verify_token: '012_a3b4c56789de0123f456a7b',
  channel_name: 'appear.in Integration Testing Channel',
  event_type: 'comment'
}
```

We can then capture the `roomName` by accessing the `req.body.command_argument`. This should allow us to subsequently create a new room and send it back to the Twist client.

```javascript
app.post('/appear', (req, res) => {
  console.log(req);
  const body = req.body;
  const roomName = body.command_argument;

  const appearUrl = `📹 [Join my meeting at appear.in!](https://appear.in/${roomName})`;

  res.send(appearUrl);
});
```

If we now type `/appear my-room-name` the message will be overwritten with a link for people to join and chat!