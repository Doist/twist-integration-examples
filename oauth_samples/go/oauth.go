package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"github.com/google/uuid"
	"golang.org/x/oauth2"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"strings"
)

const (
	authorizeURL string = "https://twist.com/oauth/authorize"
	tokenURL     string = "https://twist.com/oauth/access_token"

	// callback url specified when the application was defined
	// eg. https://dev.twist.test:4567/v3/
	callbackURL string = "<<enter the callback url for your application>>"

	// e.g. https://api.twist.com/api/v3/workspaces/get
	apiURL string = "<<enter the scopes your application requires>>"

	// client (application) credentials - located at https://twist.com/integrations/build, then go to your integration
	clientID     string = "<<client id>>"
	clientSecret string = "<<client secret>>"
)

var (
	state  string
	scopes string
)

func init() {
	// Should be a comma separated list, see https://developer.twist.com/v3/#scopes for a full list
	// user:read,workspaces:read
	scopes = "<<enter the scopes your application requires>>"

	// state, should be unique
	state = uuid.New().String()
}

func main() {
	requestAuthorization()
}

func requestAuthorization() {
	reader := bufio.NewReader(os.Stdin)

	// Step 1 - simulate a request from a browser on the authorize_url -
	// will return an authorization code after the user is prompted for credentials.
	authURL := authorizeURL + "?response_type=code&client_id=" + clientID + "&redirect_uri=" + url.QueryEscape(callbackURL) +
		"&scope=" + url.QueryEscape(scopes) + "&state=" + url.QueryEscape(state)
	fmt.Println("Go to the following url on a browser and enter the code from the returned url")
	fmt.Println(authURL)
	fmt.Printf("-> ")

	// Read the authorization code
	text, _ := reader.ReadString('\n')

	requestToken(strings.TrimSuffix(text, "\n"))
}

func requestToken(code string) {
	fmt.Println("Requesting access token")

	// Step 2, 3 - turn the authorization code into a access token, etc
	token := exchangeForToken(code)

	if token == "" {
		fmt.Println("Invalid token response")
		return
	}

	// We can now use the access_token as much as we want to access protected resources.
	makeAPICall(token)
}

func makeAPICall(token string) {

	var hc = http.Client{}
	var bearer = "Bearer " + token

	request, _ := http.NewRequest("GET", apiURL, nil)

	request.Header.Add("Authorization", bearer)
	apiResp, _ := hc.Do(request)

	defer apiResp.Body.Close()

	jsonBytes, _ := ioutil.ReadAll(apiResp.Body)

	fmt.Println(string(jsonBytes))
}

func exchangeForToken(code string) string {
	authData := url.Values{
		"grant_type":    {"authorization_code"},
		"code":          {code},
		"redirect_uri":  {callbackURL},
		"client_id":     {clientID},
		"client_secret": {clientSecret},
	}

	authResp, err := http.PostForm(tokenURL, authData)

	if authResp == nil {
		fmt.Println("error: ", err)
		return ""
	}

	fmt.Println("Access token requested")

	var result *oauth2.Token

	body, _ := ioutil.ReadAll(authResp.Body)

	json.Unmarshal(body, &result)

	return result.AccessToken
}
