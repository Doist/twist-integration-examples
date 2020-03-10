package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"

	"github.com/google/uuid"
	"golang.org/x/oauth2"
)

const (
	authorizeURL = "https://twist.com/oauth/authorize"
	tokenURL     = "https://twist.com/oauth/access_token"

	// callback url specified when the application was defined
	// eg. https://dev.twist.test:4567/v3/
	callbackURL = "<<enter the callback url for your application>>"

	// e.g. https://api.twist.com/api/v3/workspaces/get
	apiURL = "<<enter the url of the api endpoint you wish to access>>"
)

var (
	// Should be a comma separated list, see https://developer.twist.com/v3/#scopes for a full list
	// user:read,workspaces:read
	scopes = "<<enter the scopes your application requires>>"
	state  = uuid.New().String()

	// client (application) credentials - located at https://twist.com/integrations/build, then go to your integration
	clientID     = os.Getenv("TWIST_CLIENT_ID")
	clientSecret = os.Getenv("TWIST_CLIENT_SECRET")
)

func main() {
	if err := requestAuthorization(); err != nil {
		log.Fatal(err)
	}
}

func requestAuthorization() error {
	reader := bufio.NewReader(os.Stdin)

	// Step 1 - simulate a request from a browser on the authorize_url -
	// will return an authorization code after the user is prompted for credentials.
	vals := make(url.Values)
	vals.Set("response_type", "code")
	vals.Set("client_id", clientID)
	vals.Set("redirect_url", callbackURL)
	vals.Set("scope", scopes)
	vals.Set("state", state)

	fmt.Println("Go to the following url on a browser and enter the code from the returned url")
	fmt.Println(authorizeURL + "?" + vals.Encode())
	fmt.Printf("-> ")

	// Read the authorization code
	text, err := reader.ReadString('\n')

	if err != nil {
		return fmt.Errorf("Erorr reading the code you entered")
	}

	err = requestToken(strings.TrimSuffix(text, "\n"))

	return err
}

func requestToken(code string) error {
	fmt.Println("Requesting access token")

	// Step 2, 3 - turn the authorization code into a access token, etc
	token, err := exchangeForToken(code)

	if err != nil {
		return fmt.Errorf("Invalid token response: %v", err)
	}

	// We can now use the access_token as much as we want to access protected resources.
	return makeAPICall(token)
}

func makeAPICall(token string) error {
	request, err := http.NewRequest("GET", apiURL, nil)

	if err != nil {
		return fmt.Errorf("Error creating request")
	}

	request.Header.Add("Authorization", "Bearer "+token)
	apiResp, err := http.DefaultClient.Do(request)

	if err != nil {
		return fmt.Errorf("Error making Authorization request")
	}

	defer apiResp.Body.Close()

	if apiResp.StatusCode != http.StatusOK {
		return fmt.Errorf("Unexpected respose %q", apiResp.Status)
	}

	if ct := apiResp.Header.Get("Content-Type"); ct != "application/json" {
		return fmt.Errorf("Unsupported content-type: %q", ct)
	}

	_, err = io.Copy(os.Stdout, apiResp.Body)
	return err
}

func exchangeForToken(code string) (string, error) {
	authData := url.Values{
		"grant_type":    {"authorization_code"},
		"code":          {code},
		"redirect_uri":  {callbackURL},
		"client_id":     {clientID},
		"client_secret": {clientSecret},
	}

	authResp, err := http.PostForm(tokenURL, authData)

	if err != nil {
		return "", fmt.Errorf("error: %v", err)
	}

	if authResp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("unexpected status: %q", authResp.Status)
	}

	fmt.Println("Access token requested")

	var result oauth2.Token

	body, err := ioutil.ReadAll(authResp.Body)

	if err != nil {
		return "", fmt.Errorf("Error reading the API call response")
	}

	err = json.Unmarshal(body, &result)

	return result.AccessToken, err
}
