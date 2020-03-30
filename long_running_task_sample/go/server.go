package main

import (
	"fmt"
	"log"
	"net/http"
	"net/url"
	"strconv"
	"strings"
	"time"
)

func main() {
	http.HandleFunc("/bot", botHandler)
	log.Fatal(http.ListenAndServe(":5000", nil))
}

func botHandler(w http.ResponseWriter, r *http.Request) {
	// Because the Twist API will only send this data via POST,
	// we can discard any calls to this endpoint that aren't POST
	if r.Method != "POST" {
		http.Error(w, "This is POST only", http.StatusBadRequest)
		return
	}

	if err := r.ParseForm(); err != nil {
		log.Print("ParseForm() error: ", err)
		http.Error(w, "Error reading form parts", http.StatusBadRequest)
		return
	}

	eventType := r.FormValue("event_type")

	// It's good practice with Twist integrations to support being
	// pinged, it's a good way to test that your integration is
	// successfully talking to Twist. This ping is done from the bot
	// section of the integration's configuration
	if eventType == "ping" {
		w.Write([]byte("pong"))
		return
	}

	go func() {
		processBotConversation(r.PostForm)
	}()

	// This tells the server we've received the message ok
	// Optionally, you can also respond with some message text, this
	// text would then be displayed as a message to the user who sent
	// it. This message could be to say that the bot is handling their
	// request
	w.Header().Set("Content-Type", "text/plain")
	w.WriteHeader(http.StatusAccepted)
}

func processBotConversation(r url.Values) {
	callbackURL := r.Get("url_callback")
	urlTTL := r.Get("url_ttl")

	if urlHasTimedOut(urlTTL) {
		return
	}

	var message = createMessageResponse(r)

	err := sendReply(callbackURL, message)
	if err != nil {
		log.Print("Error sending reply: %v", err)
	}
}

func createMessageResponse(r url.Values) string {
	content := strings.ToUpper(r.Get("content"))
	log.Print("Content: %s\n", content)
	var message = "I didn't understand that, please type 'help' to see how to use this bot"

	if strings.HasPrefix(content, "HELLO") ||
		strings.HasPrefix(content, "HI") {
		userName := r.Get("user_name")
		message = fmt.Sprintf("Hello, %s", userName)

		// This is here to purely demonstrate that a bot's response could take a while, thus
		// why this sample is showing how to use the url_callback approach.
		time.Sleep(11 * time.Second)
	} else if content == "HELP" {
		message = "This sample allows you to say 'hi' or 'hello' to the bot"
	}

	return message
}

func sendReply(callbackURL, message string) error {
	data := url.Values{
		"content": {message},
	}

	response, err := http.DefaultClient.PostForm(callbackURL, data)

	if err == nil {
		defer response.Body.Close()
	}

	return err
}

func urlHasTimedOut(urlTTL string) bool {
	if ttl, err := strconv.ParseInt(urlTTL, 10, 64); err == nil {
		var now = time.Now()
		expiryTime := time.Unix(ttl, 0)

		return now.After(expiryTime)
	}

	return true
}
