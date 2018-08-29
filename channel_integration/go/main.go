package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

const (
	twistURL = "https://twistapp.com/api/v2/integration_incoming/post_data?install_id=71554&install_token=71554_b818c7fe1fee02a567cf87471cd8c287"
)

type reply struct {
	Content string `json:"content"`
}

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

func setResponse(w http.ResponseWriter, r reply) {
	js, err := json.Marshal(r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(js)
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

	tr, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Printf(err.Error())
		return
	}
	log.Printf("\n%#v", string(tr))
}

func main() {
	http.HandleFunc("/issues", issuesHandler)
	log.Println("Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)")
	log.Fatal(http.ListenAndServe(":5000", nil))
}
