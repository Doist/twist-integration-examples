const express = require('express');
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  }),
);

app.post('/appear', (req, res) => {
  const body = req.body;
  const roomName = body.command_argument;

  const appearUrl = `📹 [Join my meeting at appear.in!](https://appear.in/${roomName})`;

  res.send(appearUrl);
});

app.listen(process.env.PORT || 3000, () =>
  console.log(`Server listening on port ${process.env.PORT || 3000}`),
);
