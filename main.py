#install fastapi -  pip install fastapi[all]
#install uvicorn - pip install uvicorn[standard]
#pip install uvicorn[standard] certifi


from fastapi import FastAPI, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader
import uvicorn

import json
from fastapi.responses import JSONResponse
import logging

server_list = "server_list.json"

api_keys = [
    "API-Key"
]


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/access.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()


@app.middleware("https")
async def log_requests(request: Request, call_next):
    """
    Log the request to the access log.

    Args:
        request (Request): The request.
        call_next (function): The next function to call.

    Returns:
        Response: The response.
    """
    logging.info(f"{request.client.host} - {request.method} - {request.url.path}")
    return await call_next(request) # pragma: no cover



def read_json_file(file_path):
    """
    Read data from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The data read from the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data



api_key_header = APIKeyHeader(name="Authentication")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """
    Get the API Key from the header.

    Args:
        api_key_header (str): The API Key header.

    Returns:
        str: The API Key.

    Raises:
        HTTPException: If the API Key is invalid or missing.
    """
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

@app.get("/api/data")
def data(api_key: str = Security(get_api_key)):
    """
    Process the request for authenticated users and return server list data.

    Args:
        api_key (str): The API Key.

    Returns:
        JSONResponse: The server list data as a JSON response.
    """
    server_list_data = read_json_file(server_list)
    return JSONResponse(content=server_list_data)

if __name__ == '__main__':
    print("Server is running")
    uvicorn.run(app, host='localhost', port=80, headers=[('Access-Control-Allow-Origin', '*'), ('server', ' ')])

    #print(reply)