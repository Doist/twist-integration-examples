package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"mime/multipart"
	"net/http"
	"net/url"
	"os"

	"github.com/google/uuid"
	"golang.org/x/oauth2"
)

const (
	conversationID = "<<enter your conversation ID here>>"
	threadID       = "<<enter your thread ID here>>"
	fileName       = "../images/image.jpg"

	attachmentEndpoint             = "https://api.twist.com/api/v3/attachments/upload"
	addConversationMessageEndpoint = "https://api.twist.com/api/v3/conversation_messages/add"
	addCommentThreadEndpoint       = "https://api.twist.com/api/v3/comments/add"
)

var (
	// This access token will need to have "attachments:write, and either/both
	// messages:write,comments:write" (depending on your usage) scopes
	accessToken = os.Getenv("TWIST_TOKEN")
	httpClient  *http.Client
)

func main() {
	if accessToken == "" {
		log.Fatal("Invalid access token")
	}

	httpClient = oauth2.NewClient(context.Background(), oauth2.StaticTokenSource(&oauth2.Token{
		AccessToken: accessToken,
		TokenType:   "Bearer",
	}))

	if err := uploadAttachmentToThread("Hello from Go", fileName); err != nil {
		log.Fatal(err)
	}
}

func uploadAttachment(fileName string) (json.RawMessage, error) {
	var attachmentID = uuid.New().String()

	// Read the file contents and do *something* with it
	file, err := os.Open(fileName)
	if err != nil {
		return nil, fmt.Errorf("Error reading file: %v", err)
	}
	defer file.Close()

	data := map[string]string{
		"attachment_id": attachmentID,
		"file_name":     fileName,
	}

	// Prepare the file for uploading
	// NOTE: This will buffer the file into memory, if you try and do this
	// with a large file, you may run into resource issues.
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	part, err := writer.CreateFormFile("file", fileName)

	if err != nil {
		return nil, fmt.Errorf("Error adding file to request: %v", err)
	}

	_, err = io.Copy(part, file)

	if err != nil {
		return nil, fmt.Errorf("Error reading file: %v", err)
	}

	for key, val := range data {
		_ = writer.WriteField(key, val)
	}

	writer.Close()

	request, err := http.NewRequest(http.MethodPost, attachmentEndpoint, body)
	if err != nil {
		return nil, fmt.Errorf("Error creating request: %v", err)
	}

	request.Header.Add("Content-Type", writer.FormDataContentType())

	// Upload the file
	response, err := httpClient.Do(request)

	if err != nil {
		return nil, err
	}

	defer response.Body.Close()

	// make sure we have an expected response code
	if response.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status: %q", response.Status)
	}

	// make sure response has valid content-type
	if ct := response.Header.Get("Content-Type"); ct != "application/json" {
		return nil, fmt.Errorf("unsupported content-type: %q", ct)
	}

	jsonBytes, err := ioutil.ReadAll(io.LimitReader(response.Body, 1*1024*1024))

	if err != nil {
		return nil, fmt.Errorf("Error reading body: %v", err)
	}

	var jsonBody json.RawMessage
	if err := json.Unmarshal(jsonBytes, &jsonBody); err != nil {
		return nil, fmt.Errorf("response body json decode: %v", err)
	}

	// Check to make sure the API hasn't sent back any errors
	tmp := struct {
		ErrorText string `json:"error_string"`
	}{}
	if err := json.Unmarshal(jsonBytes, &tmp); err != nil {
		return nil, err
	}

	if tmp.ErrorText != "" {
		return nil, fmt.Errorf("upload attachment error from API: %q", tmp.ErrorText)
	}

	// Return the JSON here as this will be needed
	// when adding the attachment to the message
	return jsonBody, nil
}

func uploadAttachmentToConversation(message string, fileName string) error {
	data := url.Values{
		"conversation_id": {conversationID},
	}

	return sendMessage(data, fileName, message, addConversationMessageEndpoint)
}

func uploadAttachmentToThread(message string, fileName string) error {
	data := url.Values{
		"thread_id": {threadID},
	}

	return sendMessage(data, fileName, message, addCommentThreadEndpoint)
}

func sendMessage(data url.Values, fileName string, message string, apiEndpoint string) error {
	attachment, err := uploadAttachment(fileName)

	if err != nil {
		return fmt.Errorf("Error from upload: %v", err)
	}

	fmt.Printf("Sending message '%q'", message)

	data.Set("content", message)
	data.Set("attachments", "["+string(attachment)+"]")

	response, err := httpClient.PostForm(apiEndpoint, data)

	if err != nil {
		return fmt.Errorf("Error posting to conversation: %v", err)
	}

	_, err = io.Copy(os.Stdout, response.Body)
	fmt.Println("")

	return err
}
