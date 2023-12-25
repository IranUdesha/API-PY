from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
import uvicorn

import json
from fastapi.responses import JSONResponse

server_list = "server_list.json"

api_keys = [
    "aR6eT0uJ6qM3gZ5hD6gZ0tZ2eL2aH2jL"
]

def read_json_file(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

app = FastAPI()

api_key_header = APIKeyHeader(name="Authentication")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

@app.get("/api/data")
def data(api_key: str = Security(get_api_key)):
    # Process the request for authenticated users
        server_list_data = read_json_file(server_list)
        return JSONResponse(content=server_list_data)
    
    # return read_json_file(server_list)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=80, headers=[('Access-Control-Allow-Origin', '*'), ('server', ' ')],)

