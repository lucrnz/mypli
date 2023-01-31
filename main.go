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
	"strings"
	"syscall"

	"github.com/gorilla/mux"
	"gopkg.in/yaml.v3"
)

type HostConfig struct {
	Name     string
	Host     string
	User     string
	Port     string
	Services string
}

type ExecutedCommand struct {
	Stdout  []byte
	Stderr  []byte
	Command *exec.Cmd
}

type APIResult struct {
	ReturnCode int    `json:"returncode"`
	Stderr     string `json:"stderr"`
	Stdout     string `json:"stdout"`
}

var hostsData []HostConfig

func getErrorBytes(code int, message string) []byte {
	apiResult := APIResult{}
	apiResult.ReturnCode = code
	apiResult.Stderr = message
	apiResult.Stdout = ""
	apiResultBytes, err := json.Marshal(apiResult)

	if err != nil {
		log.Fatalf("error: %v", err)
	}

	return apiResultBytes
}

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

func remoteBash(hostName string, bashCode string) (ExecutedCommand, error) {
	cmd := exec.Command("ssh", hostName, "bash")
	var b bytes.Buffer
	b.Write([]byte(bashCode))
	cmd.Stdin = &b

	var stdout bytes.Buffer
	var stderr bytes.Buffer

	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()
	result := ExecutedCommand{}
	result.Stderr = stderr.Bytes()
	result.Stdout = stdout.Bytes()
	result.Command = cmd

	return err, result
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
			w.Write(getErrorBytes(http.StatusUnauthorized, "Unauthorized"))
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
					w.Write(getErrorBytes(http.StatusBadRequest, "Bad request"))
					return
				}
			}
		}

		var hostConfig *HostConfig

		for _, v := range hostsData {
			if v.Name == params["host_name"] {
				hostConfig = &v
				break
			}
		}

		if hostConfig == nil {
			w.Header().Add("Content-Type", "application/json; charset=utf-8")
			w.WriteHeader(http.StatusBadRequest)
			w.Write(getErrorBytes(http.StatusBadRequest, "Bad request"))
			return
		}

		cmd, err := remoteBash(params["host_name"], "cat "+hostConfig.Services+"/"+params["service_name"]+"/mypli.yml")

		if err != nil {
			w.Header().Add("Content-Type", "application/json; charset=utf-8")
			w.WriteHeader(http.StatusInternalServerError)
			w.Write(getErrorBytes(http.StatusInternalServerError, "Internal server error"))
			log.Printf("error: %s\n", err.Error())
			return
		}

		var commands map[string][]string

		if err := yaml.Unmarshal(cmd.Stdout, &commands); err != nil {
			if err != nil {
				w.Header().Add("Content-Type", "application/json; charset=utf-8")
				w.WriteHeader(http.StatusInternalServerError)
				w.Write(getErrorBytes(http.StatusInternalServerError, "Internal server error"))
				log.Printf("error: %s\n", err.Error())
				return
			}
		}

		actionArray, actionFound := commands[params["action_name"]]

		if !actionFound {
			w.Header().Add("Content-Type", "application/json; charset=utf-8")
			w.WriteHeader(http.StatusInternalServerError)
			w.Write(getErrorBytes(http.StatusInternalServerError, "Internal server error"))
			log.Printf("error: Action not found")
		}

		cmd, err = remoteBash(params["host_name"], "cd "+hostConfig.Services+"/"+params["service_name"]+" || exit 1\n"+strings.Join(actionArray, " && "))

		if err != nil && !strings.HasPrefix(err.Error(), "exit status") {
			w.Header().Add("Content-Type", "application/json; charset=utf-8")
			w.Write(getErrorBytes(http.StatusInternalServerError, "Internal server error"))
			log.Printf("error: %v", err)
		}

		w.Header().Add("Content-Type", "application/json; charset=utf-8")
		rc := cmd.Command.ProcessState.ExitCode()

		if rc == 0 {
			w.WriteHeader(http.StatusOK)
		} else {
			w.WriteHeader(http.StatusInternalServerError)
		}

		apiResult := APIResult{}
		apiResult.ReturnCode = rc
		apiResult.Stdout = string(cmd.Stdout)
		apiResult.Stderr = string(cmd.Stderr)
		apiResultBytes, _ := json.Marshal(apiResult)
		w.WriteHeader(http.StatusOK)
		w.Write(apiResultBytes)
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
