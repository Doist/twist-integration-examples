package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"strconv"

	"golang.org/x/oauth2"
)

const (
	addConversationMessageEndpoint = "https://api.twist.com/api/v3/conversation_messages/add"
	addCommentThreadEndpoint       = "https://api.twist.com/api/v3/comments/add"
)

var (
	// This access token will need to have either/both
	// messages:write,comments:write" (depending on your usage) scopes
	accessToken = os.Getenv("TWIST_TOKEN")
	httpClient  *http.Client
)

func main() {
	conversation := flag.Int("conversation", 0, "Conversation ID for the file to be uploaded to")
	thread := flag.Int("thread", 0, "Thread ID for the file to be uploaded to")
	message := flag.String("message", "", "The message to go with the button")
	action := flag.String("action", "", "The type of action you want, this can be open_url, prefill_message or send_reply")
	url := flag.String("url", "", "The url to open when the button is clicked")
	buttonMessage := flag.String("buttonmessage", "", "The text to be prefilled/sent when the button is clicked")
	buttonText := flag.String("buttontext", "", "The text to appear on the button")
	flag.Parse()

	if accessToken == "" {
		log.Fatal("Invalid access token")
	}

	httpClient = oauth2.NewClient(context.Background(), oauth2.StaticTokenSource(&oauth2.Token{
		AccessToken: accessToken,
		TokenType:   "Bearer",
	}))

	conversationID := *conversation
	threadID := *thread

	if conversationID == 0 && threadID == 0 {
		log.Fatal("Please supply either a conversation ID or a thread ID")
	}

	messageStr := *message
	actionStr := *action
	urlStr := *url
	buttonMessageStr := *buttonMessage
	buttonTextStr := *buttonText

	button, err := createButton(actionStr, buttonTextStr, urlStr, buttonMessageStr)

	if err != nil {
		log.Fatal(err)
	}

	if button == nil {
		log.Fatal("Something went wrong with the button creation")
	}

	if threadID != 0 {
		if err := addButtonToThread(messageStr, button, threadID); err != nil {
			log.Fatal(err)
		}
	} else if conversationID != 0 {
		if err := addButtonToConversation(messageStr, button, conversationID); err != nil {
			log.Fatal(err)
		}
	}
}

func addButtonToConversation(message string, button *Button, conversationID int) error {
	data := url.Values{
		"conversation_id": {strconv.Itoa(conversationID)},
	}

	return sendMessage(data, message, button, addConversationMessageEndpoint)
}

func addButtonToThread(message string, button *Button, threadID int) error {
	data := url.Values{
		"thread_id": {strconv.Itoa(threadID)},
	}

	return sendMessage(data, message, button, addCommentThreadEndpoint)
}

func sendMessage(data url.Values, message string, button *Button, apiEndpoint string) error {
	fmt.Printf("Sending message '%q'\n", message)

	actionJSON, err := json.Marshal(button)
	if err != nil {
		return fmt.Errorf("Error converting button to JSON: %v", err)
	}

	data.Set("content", message)
	data.Set("actions", "["+string(actionJSON)+"]")

	fmt.Println(data)

	response, err := httpClient.PostForm(apiEndpoint, data)

	if err != nil {
		return fmt.Errorf("Error posting message: %v", err)
	}

	_, err = io.Copy(os.Stdout, response.Body)
	fmt.Println("")

	return err
}

func createButton(action string, buttonText string, url string, message string) (*Button, error) {
	if action != "open_url" && action != "prefill_message" && action != "send_reply" {
		return nil, fmt.Errorf("You have not passed a valid action: %v", action)
	}

	var button = Button{
		Action:     action,
		ButtonText: buttonText,
		ButtonType: "action",
	}

	if action == "open_url" {
		if url == "" {
			return nil, fmt.Errorf("URL should be set when using 'open_url'")
		}

		button.URL = url
	} else {
		if message == "" {
			return nil, fmt.Errorf("Message cannot be empty")
		}

		button.Message = message
	}

	return &button, nil
}

// Button is the object for the action button
type Button struct {
	Action     string `json:"action"`
	URL        string `json:"url"`
	ButtonText string `json:"button_text"`
	Message    string `json:"message"`
	ButtonType string `json:"type"`
}
