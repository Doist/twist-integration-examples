package main

import (
	// "encoding/json"
	"fmt"
	"github.com/google/uuid"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
)

const (
	workspaceID    = 70829
	conversationID = 494996
	threadID       = 1389541

	attachmentEndpoint             string = "https://api.twist.com/api/v3/attachments/upload"
	addConversationMessageEndpoint string = "https://api.twist.com/api/v3/conversation_messages/add"
	addCommentThreadEndpoint       string = "https://api.twist.com/api/v3/comments/add"
)

var (
	bearerToken string
	accessToken string
)

func init() {
	accessToken = os.Getenv("twist_token")
	bearerToken = "Bearer " + accessToken
}

func main() {

}

func uploadAttachment() string {
	var fileName = "image.jpg"
	var attachmentID = uuid.New().String()

	f, _ := ioutil.ReadFile(fileName)
	// Read the file contents and do *something* with it

	data := url.Values{
		"attachment_id": {attachmentID},
		"file_name":     {fileName},
		"file":          {f},
	}

	response, err := http.PostForm(attachmentEndpoint, data)

	if err != nil {
		fmt.Println("Error uploading attachment: ", err)
		return ""
	}

	json, _ := ioutil.ReadAll(response.Body)

	// Return the JSON here as this will be needed
	// when adding the attachment to the message
	return string(json)
}

func uploadAttachmentToConversation(message string) {
	attachment := uploadAttachment()

	if attachment == "" {
		return
	}

	fmt.Println("Sending message '" + message + "'")

	data := url.Values{
		"conversation_id": {string(conversationID)},
		"content":         {message},
		"attachments":     {attachment},
	}

	response, _ := http.PostForm(addConversationMessageEndpoint, data)

	json, _ := ioutil.ReadAll(response.Body)

	fmt.Println(string(json))
}
