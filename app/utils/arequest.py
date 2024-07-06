import httpx


async def send(method, url, **kwargs):
    # 60.0: The total time allowed for the entire request, including connection time, reading, and writing.
    # connect=10.0: The maximum time allowed to establish a connection to the server.
    timeout = httpx.Timeout(60.0, connect=10.0)
    transport = httpx.AsyncHTTPTransport(retries=3)

    async with httpx.AsyncClient(timeout=timeout, transport=transport, http2=True) as client:
        response = await client.request(method, url, **kwargs)
    return response


async def get(url, params: dict = None, data: dict = None, json: dict = None, headers: dict = None, follow_redirects: bool = True):
    response = await send(method="GET", url=url, params=params, data=data, json=json, headers=headers, follow_redirects=follow_redirects)
    return response


async def post(url, params: dict = None, data: dict = None, json: dict = None, headers: dict = None, files=None, follow_redirects: bool = True):
    response = await send(method="POST", url=url, params=params, data=data, json=json, headers=headers, files=files, follow_redirects=follow_redirects)
    return response


async def put(url, params: dict = None, data: dict = None, json: dict = None, headers: dict = None):
    response = await send(method="PUT", url=url, params=params, data=data, json=json, headers=headers)
    return response


async def delete(url, params: dict = None, data: dict = None, json: dict = None, headers: dict = None):
    response = await send(method="DELETE", url=url, params=params, data=data, json=json, headers=headers)
    return response

