const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const TWIST_URL =
  'https://twistapp.com/api/v2/integration_incoming/post_data?install_id=1234&install_token=01234_56a7b89c012345678de9012f345678ab';

app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  }),
);

app.post('/issue', (req, res) => {
  const body = req.body;
  const githubId = req.get('X-GitHub-Delivery')

  if (!githubId) {
    const eventType = body.event_type;
    if (eventType && eventType === 'ping') {
      return res.json({ 'content': 'pong' })
    }
  }
  else {
    const repoName = body.repository.name;
    const issueName = body.issue.title;
    const issueNumber = body.issue.number;
    const issueBody = body.issue.body;
    const issueLink = body.issue.html_url;

    const title = `${repoName} - #${issueNumber} ${issueName}`;
    const content = `**Body**: \n${issueBody}\n\n**Link**:\n[GitHub Issue](${issueLink})`;

    const twistData = { title, content };

    axios.post(TWIST_URL, twistData).catch(err => console.error(err));

    res.send(twistData);
  }
});

app.listen(process.env.PORT || 5000, () =>
  console.log(`Server listening on port ${process.env.PORT || 5000}`),
);
