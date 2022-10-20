# container-cmdr

## Building

```
docker build -t container-cmdr .
```

## Run a command in a different container with a POST

Run the server
```
docker run --rm -p '8080:8080' --userns host -v /var/run/docker.sock:/var/run/docker.sock -it container-cmdr
```

Run a different container
```
docker run --rm --name nginx -d nginx:stable
```

Run run a command in the nginx container
```
curl -H 'Content-Type: application/json' -X POST -d '{"container": "nginx", "exec": "nginx -s reload"}' http://127.0.0.1:8080
{"output":"2022/10/20 06:00:28 [notice] 113#113: signal process started\n"}
```

## AUTH_TOKEN

If AUTH_TOKEN is set, it's needed as a header in order to execute commands
```
docker run -e 'AUTH_TOKEN=1234' -p '8080:8080' --userns host -v /var/run/docker.sock:/var/run/docker.sock -it container-cmdr
```

```
curl -H 'Content-Type: application/json' -X POST -d '{"container": "nginx", "exec": "nginx -s reload"}' http://127.0.0.1:8080
{"error": "an api key is required"}
```

```
curl -H 'X-Auth-Token: 1234' -H 'Content-Type: application/json' -X POST -d '{"container": "nginx", "exec": "nginx -s reload"}' http://127.0.0.1:8080
{"output":"2022/10/20 06:34:08 [notice] 217#217: signal process started\n"
```
