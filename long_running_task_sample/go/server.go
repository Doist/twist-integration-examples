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
	fmt.Println("botHandler")
	// Because the Twist API will only send this data via POST,
	// we can discard any calls to this endpoint that aren't POST
	if r.Method != "POST" {
		http.Error(w, "This is POST only", http.StatusBadRequest)
		return
	}

	if err := r.ParseForm(); err != nil {
		fmt.Fprintf(w, "ParseForm() error: %v", err)
		http.Error(w, "Error reading form parts", http.StatusBadRequest)
		return
	}

	eventType := r.FormValue("event_type")

	// It's good practice with Twist integrations to support being
	// pinged, it's a good way to test that your integration is
	// successfully talking to twist. This ping is done from the bot
	// section of the integration's configuration
	if eventType == "ping" {
		w.Write([]byte("pong"))
		return
	}

	go func() {
		processBotConversation(r.PostForm)
	}()

	w.Header().Set("Content-Type", "text/plain")
	w.WriteHeader(http.StatusAccepted)

	fmt.Println("Response header written")
}

func processBotConversation(r url.Values) {
	fmt.Printf("processBotConversation, messageID: %s\n", r.Get("message_id"))
	callbackURL := r.Get("url_callback")
	urlTTL := r.Get("url_ttl")

	if urlHasTimedOut(urlTTL) {
		return
	}

	var message = createMessageResponse(r)

	err := sendReply(callbackURL, message)
	if err != nil {
		fmt.Printf("Error sending reply: %v", err)
	}
}

func createMessageResponse(r url.Values) string {
	fmt.Println("createMessageResponse")
	content := strings.ToUpper(r.Get("content"))
	fmt.Printf("Content: %s\n", content)
	var message = "I didn't understand that, please type 'help' to see how to use this bot"

	if strings.HasPrefix(content, "HELLO") ||
		strings.HasPrefix(content, "HI") {
		userName := r.Get("user_name")
		message = fmt.Sprintf("Hello, %s", userName)

		time.Sleep(11 * time.Second)
	} else if content == "HELP" {
		message = "This sample allows you to say 'hi' or 'hello' to the bot"
	}

	return message
}

func sendReply(callbackURL, message string) error {
	fmt.Println("sendReply")
	data := url.Values{
		"content": {message},
	}

	_, err := http.DefaultClient.PostForm(callbackURL, data)
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
