package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"mime/multipart"
	"net/http"
	"net/url"
	"os"
	"strings"

	"github.com/google/uuid"
	"golang.org/x/oauth2"
)

const (
	conversationID = "<<enter your conversation ID here>>"
	threadID       = "<<enter your thread ID here>>"

	attachmentEndpoint             = "https://api.twist.com/api/v3/attachments/upload"
	addConversationMessageEndpoint = "https://api.twist.com/api/v3/conversation_messages/add"
	addCommentThreadEndpoint       = "https://api.twist.com/api/v3/comments/add"
)

var (
	// This access token will need to have "attachments:write, and either/both
	// messages:write,comments:write" (depending on your usage) scopes
	accessToken = os.Getenv("twist_token")
	bearerToken = "Bearer " + accessToken
	httpClient  *http.Client
)

func main() {
	if accessToken == "" {
		fmt.Println("Invalid access token")
		return
	}

	httpClient = oauth2.NewClient(context.Background(), oauth2.StaticTokenSource(&oauth2.Token{
		AccessToken: accessToken,
		TokenType:   "Bearer",
	}))

	if err := uploadAttachmentToThread("Hello from Go"); err != nil {
		fmt.Println(err.Error)
	}
}

func uploadAttachment() (string, error) {
	var fileName = "image.jpg"
	var attachmentID = uuid.New().String()

	// Read the file contents and do *something* with it
	file, readFileError := os.Open(fileName)
	if readFileError != nil {
		return "", fmt.Errorf("Error reading file: %q", readFileError.Error)
	}
	defer file.Close()

	data := map[string]string{
		"attachment_id": attachmentID,
		"file_name":     fileName,
	}

	// Prepare the file for uploading
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	part, err := writer.CreateFormFile("file", fileName)

	if err != nil {
		return "", fmt.Errorf("Error adding file to request")
	}

	io.Copy(part, file)

	for key, val := range data {
		_ = writer.WriteField(key, val)
	}

	writer.Close()

	request, requestError := http.NewRequest("POST", attachmentEndpoint, body)
	if requestError != nil {
		return "", fmt.Errorf("Error creating request: %q", requestError.Error)
	}

	request.Header.Add("Content-Type", writer.FormDataContentType())

	// Upload the file
	response, err := httpClient.Do(request)

	if err != nil {
		fmt.Println("Error uploading attachment: ", err)
		return "", err
	}

	jsonBytes, readError := ioutil.ReadAll(response.Body)

	if readError != nil {
		return "", fmt.Errorf("Error reading body: %q", readError.Error)
	}

	jsonString := string(jsonBytes)

	// Check to see if the API has sent back any errors
	if strings.Contains(jsonString, "error_string") {
		var data map[string]interface{}
		jsonError := json.Unmarshal(jsonBytes, &data)
		fmt.Printf("Error uploading attachment: %q \n", data["error_string"])
		return "", jsonError
	}

	// Return the JSON here as this will be needed
	// when adding the attachment to the message
	return jsonString, nil
}

func uploadAttachmentToConversation(message string) error {
	data := url.Values{
		"conversation_id": {conversationID},
	}

	return sendMessage(data, message, addConversationMessageEndpoint)
}

func uploadAttachmentToThread(message string) error {
	data := url.Values{
		"thread_id": {threadID},
	}

	return sendMessage(data, message, addCommentThreadEndpoint)
}

func sendMessage(
	data url.Values,
	message string,
	apiEndpoint string) error {

	attachment, err := uploadAttachment()

	if err != nil {
		return fmt.Errorf("Error from upload")
	}

	fmt.Println("Sending message '" + message + "'")

	data.Set("content", message)
	data.Set("attachments", "["+attachment+"]")

	response, responseError := httpClient.PostForm(apiEndpoint, data)

	if responseError != nil {
		return fmt.Errorf("Error posting to conversation: %q", responseError.Error)
	}

	_, readerError := io.Copy(os.Stdout, response.Body)
	fmt.Println("")

	return readerError
}
