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

const handleMessage = body => {
    switch (body.event_type) {
      case `ping`:
        return { content: `pong` };
      case `thread`:
        return `Thanks for notifying me of this thread!`;
      case `comment`:
        return `Interesting you should mention that. I was thinking the same thing!`;
        break;
      case `message`:
        return `Hello, ${body.user_name}! I hope you're having a great day.`;
      default:
        return { content: `` };
    }
  };
  
  app.post('/bot', (req, res) => {
    const body = req.body;
  
    const response = handleMessage(body);
  
    res.send(response);
  });

app.listen(process.env.PORT || 3000, () =>
  console.log(`Server listening on port ${process.env.PORT || 3000}`),
);