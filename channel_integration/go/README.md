# GitHub Issues - Channel Integration with Go

We can use Twist to create a new channel integration that interfaces with GitHub webhooks. The outcome we should expect from this example is:

> When a new GitHub issue is created, it should post a relevant Twist thread to a channel that contains information about the issue.

## Prerequisites
To get it up and running you have to [install go](https://golang.org/), no external packages are needed.

We'll also be using [ngrok](https://ngrok.com/) for this project. You can download the binary from [the website](https://ngrok.com/), `npm` or another method of your choosing.

## New Project

For this example, just create a file named `main.go`.

We can then set up a listen server with `net\http`:

```go
func main() {
	log.Println("Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)")
	log.Fatal(http.ListenAndServe(":5000", nil))
}
```

Next, we'll define a new route that our webhook will point at:

```go
func issuesHandler(w http.ResponseWriter, r *http.Request) {
  # TODO
}

func main() {
	http.HandleFunc("/issues", issuesHandler)
	...
}
```

Our application wants to listen for user events on GitHub (such as making a new issue) and then perform an action on Twist. This means we'll need to use `ngrok` to _expose_ our application and plug this into the integration over at [Twist](https://twistapp.com).

As you might have already guessed - we'll need to create the Twist integration next!

# Twist Integration
## Create a New Integration

Navigate to https://twistapp.com and select 'Add Integrations' from the top-right drop down menu. Next, select 'Build' from the navigation menu and then 'Add New Integration'.

We can then add an integration name and description:

**Integration name**

GitHub Issues


**Description**

Create a new Twist thread whenever there is a new GitHub issue.

**Integration type**

Channel integration

This allows us to create a new integration that can listen for GitHub issues when installed. Click 'Create my integration' to continue. Next, head over to the 'Webhooks' section and paste in the URL we get from `ngrok` later in this tutorial.

## Installing the Integration

We can install our integration by navigating to Installation 🚀 and subsequently installing this onto a particular channel _or_ by sharing the URL with someone else.

## Exposing a URL
We now have an application on Twist but no exposed URL, for this we'll use `ngrok`. If you haven't got `ngrok` already, get it from [https://ngrok.com](https://ngrok.com)

Using a new terminal window (with our server running) run the following command:

```$ ngrok http 5000```

This starts a HTTP tunnel on based on our Node application that's running on port `5000`.

_Why this port? It's the one we started our HTTP server to listen on:_

```go
  http.ListenAndServe(":5000", nil)
```

Copy the forwarding URL from your terminal, _with the free version of `ngrok`, this will be different each time the `ngrok` command is ran_. We can then place this inside of our Twist Integration under the 'Outgoing webhook URL' inside of the webhook section.

Ensure you use the HTTPS link and add the `/issue` route, for example, `https://53325f4d.ngrok.io/issue`.

## GitHub Webhooks

We can set up GitHub webhooks by navigating to our GitHub repository -> Settings -> Webhooks and then selecting 'Add webhook'.

Similar to our Twist integration, we'll add the URL from `ngrok` here as the Payload URL: https://53325f4d.ngrok.io/issue. For content type, select `application/json` and then we can simply add a word of our choosing within the secret box.

We're then asked _Which events would you like to trigger this webhook?_ As we're simply looking for Issues only, select `Let me select individual events` and then tick `Issues`. To finish this, select _Add webhook_ you'll be able to see this in the dashboard.

# Integration
Everything is now in place to handle webhooks from GitHub. Let's modify our Go application to handle this.

Firstly, we'll need to determine whether the incoming POST request is _from GitHub_, for this example, we've elected to do a simple check for the delivery ID from within the headers. Also, when debugging we may get an `event_type` payload with the value of `ping`, so we'll firstly check for this and respond with `pong`:

```go
type reply struct {
	Content string `json:"content"`
}

func issuesHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, fmt.Sprintf("Method %s is not allowed.", r.Method), http.StatusMethodNotAllowed)
		return
	}

	gh := r.Header.Get("X-Github-Delivery")
	if gh == "" {
		handlePing(w, r)
		return
  }
}

func handlePing(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, err.Error(), http.StatusUnprocessableEntity)
		return
	}

	eventType := r.FormValue("event_type")
	if eventType == "ping" {
		setResponse(w, reply{Content: "pong"})
	}
}
```

If we now create an issue inside of the repository, we can then navigate back to our webhook and see `Recent Deliveries`. You'll be able to select a request that was made due to the open issue and see both the request and response data. You can see the entire payload from within this view and more importantly, **redeliver** the request and this means we don't have to keep creating issues each time we want to test our webhook.

## Posting Twist Threads

Everything is in place to post Twist threads based off GitHub issues. Inside of our the overview of your newly installed integration, copy the **Post content manually** URL and add it to the application for future use:

```Go
twistURL = "https://twistapp.com/api/v2/integration_incoming/post_data?install_id=1234&install_token=01234_56a7b89c012345678de9012f345678ab"
```

We can now create a new Twist thread whenever the issue comes in from the GitHub repository. We'll need to create a payload to send to Twist that contains information such as the `title` and post `content`, next, the payload can be sent using the `twist_url` that we created a moment ago:

```Go
type twistData struct {
	Title   string `json:"title"`
	Content string `json:"content"`
}

type issue struct {
	Action string `json:"action"`
	Issue  struct {
		HTMLURL string `json:"html_url"`
		Number  int    `json:"number"`
		Title   string `json:"title"`
		Body    string `json:"body"`
	} `json:"issue"`
	Repository struct {
		Name string `json:"name"`
	} `json:"repository"`
}

func issuesHandler(w http.ResponseWriter, r *http.Request) {
	...
	var data issue
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		http.Error(w, err.Error(), http.StatusUnprocessableEntity)
		return
	}

	title := fmt.Sprintf("%s - #%d %s", data.Repository.Name, data.Issue.Number, data.Issue.Title)
	content := fmt.Sprintf("**Body:** \n%s\n\n**Link**:\n [GitHub Issue](%s)", data.Issue.Body, data.Issue.HTMLURL)

	payload, err := json.Marshal(twistData{title, content})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	resp, err := http.Post(twistURL, "application/json", bytes.NewBuffer(payload))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
```

If we check our channel, you should see that the Twist thread mirrors the GitHub issue! 😄