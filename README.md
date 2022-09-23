# 🧮 Trapi-openapi-aggregator
Open api proxy server to aggregate specs of similar infores and trapi versions into single openapi spec for smartapi registration.


### Usage

Create or Edit `servers.json` with list of servers 
```json
["https://automat.ci.transltr.io/ctd/1.3/openapi.json",
 "https://automat.test.transltr.io/ctd/1.3/openapi.json",
"https://automat.transltr.io/ctd/1.3/openapi.json",
  "https://automat.renci.org/ctd/1.3/openapi.json"]
```
If these servers have matching infores and trapi versions they will aggregated as a single openapispec.


##### Python 
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run Webserver:
```bash
uvicorn --port 8080 src.server:app
```


##### Docker
Run via docker run 
```bash
docker run --rm --name agg-server -p 8080:8080 -v server.json:/code/server.json ghcr.io/translatorsri/trapi-openapi-aggregator:latest
```
