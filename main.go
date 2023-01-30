package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"strconv"
	"syscall"

	"github.com/gorilla/mux"
)

type HostConfig struct {
	Name     string
	Host     string
	User     string
	Port     string
	Services string
}

var hostsData []HostConfig

func init() {
	jsonFile, err := os.Open("./cfg/hosts.json")

	if err != nil {
		log.Fatal("Cannot open hosts file : " + err.Error())
	}

	defer jsonFile.Close()

	fileBytes, err := ioutil.ReadAll(jsonFile)

	if err != nil {
		log.Fatal("Cannot read hosts file : " + err.Error())
	}

	err = json.Unmarshal(fileBytes, &hostsData)

	if err != nil {
		log.Fatal("Cannot parse hosts file : " + err.Error())
	}
}

func remoteBash(hostName string, bashCode string) (error, *exec.Cmd) {
	cmd := exec.Command("ssh", hostName, "bash")
	var b bytes.Buffer
	b.Write([]byte(bashCode))
	cmd.Stdin = &b
	err := cmd.Run()

	return err, cmd
}

func main() {

	if len(os.Args) == 2 && os.Args[1] == "--adapt-hosts-json" {
		if len(hostsData) == 0 {
			os.Exit(1)
		}

		for _, host := range hostsData {
			fmt.Printf("Host %s\n", host.Name)
			fmt.Printf("\tHostName %s\n", host.Host)
			fmt.Printf("\tUser %s\n", host.User)
			fmt.Printf("\tPort %s\n\n", host.Port)
		}

		return
	}

	bind := "[::]"
	if len(os.Getenv("BIND")) > 0 {
		bind = os.Getenv("BIND")
	}

	port := "7878"
	if len(os.Getenv("PORT")) > 0 {
		if value, err := strconv.Atoi(os.Getenv("PORT")); err != nil && value > 0 {
			log.Fatal("Invalid environment variable: PORT")
		}
		port = os.Getenv("PORT")
	}

	if len(os.Getenv("SECRET_KEY")) == 0 {
		log.Fatal("Invalid environment variable: SECRET_KEY")
	}

	sslCert := os.Getenv("SSL_CERT")
	sslKey := os.Getenv("SSL_KEY")

	router := mux.NewRouter()

	router.HandleFunc("/{host_name}/{service_name}/{action_name}", func(w http.ResponseWriter, r *http.Request) {
		valid_auth := r.Header.Get("key") == os.Getenv("SECRET_KEY")
		if !valid_auth {
			w.Header().Add("Content-Type", "application/json; charset=utf-8")
			w.WriteHeader(http.StatusUnauthorized)
			w.Write([]byte("{\"returncode\": 401, \"stderr\": \"Unauthorized\", \"stdout\": \"\"}"))
			return
		}

		params := mux.Vars(r)

		for _, v := range params {
			for c := range v {
				if c == '!' || c == '@' || c == '#' || c == '$' || c == '%' ||
					c == '^' || c == '&' || c == '*' || c == '(' || c == ')' ||
					c == '+' || c == '?' || c == '=' || c == ',' || c == '<' ||
					c == '>' || c == '/' || c == ';' || c == ':' {
					w.Header().Add("Content-Type", "application/json; charset=utf-8")
					w.WriteHeader(http.StatusBadRequest)
					w.Write([]byte("{\"returncode\": 400, \"stderr\": \"Bad request\", \"stdout\": \"\"}"))
					return
				}
			}
		}

		w.Header().Add("Content-Type", "text/plain; charset=utf-8")
		w.Write([]byte("HostName = " + params["host_name"] + "\n" +
			"ServiceName = " + params["service_name"] + "\n" +
			"ActionName = " + params["action_name"]))
	}).Methods("GET")

	cancelChan := make(chan os.Signal, 1)
	// catch SIGETRM or SIGINTERRUPT
	signal.Notify(cancelChan, syscall.SIGTERM, syscall.SIGINT)
	go func() {
		sslEnabled := len(sslCert) > 0 && len(sslKey) > 0
		protocolStr := "http"
		if sslEnabled {
			protocolStr = "https"
		}
		listenAddr := bind + ":" + port

		log.Printf("mypli will listen on %v://%v:%v\n", protocolStr, bind, port)
		if sslEnabled {
			log.Fatal(http.ListenAndServeTLS(listenAddr, sslCert, sslKey, router))
		} else {
			log.Fatal(http.ListenAndServe(listenAddr, router))
		}
	}()
	sig := <-cancelChan
	log.Printf("Caught signal %v\n", sig)
}
