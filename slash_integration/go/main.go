package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type reply struct {
	Content string `json:"content"`
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

func appearHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, fmt.Sprintf("Method %s is not allowed.", r.Method), http.StatusMethodNotAllowed)
		return
	}

	if err := r.ParseForm(); err != nil {
		http.Error(w, err.Error(), http.StatusUnprocessableEntity)
		return
	}

	eventType := r.FormValue("event_type")
	switch eventType {
	case "ping":
		setResponse(w, reply{Content: "pong"})
	default:
		arg := r.FormValue("command_argument")
		url := fmt.Sprintf("https://appear.in/%s", arg)
		setResponse(w, reply{Content: url})
	}
}

func main() {
	http.HandleFunc("/appear", appearHandler)
	log.Println("Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)")
	log.Fatal(http.ListenAndServe(":5000", nil))
}
