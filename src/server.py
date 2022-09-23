import fastapi
from src.aggregator import merge_specs, server_list, get_available_servers
import uvicorn

app = fastapi.FastAPI(
    title="🧮 Trapi Openapi Aggregator",
    description="Proxy server for openapi docs for Translator api services."
)

all_specs = merge_specs(server_list)


@app.get('/trapi/{infores}/{version}')
async def get_spec(infores, version):
    spec = all_specs['trapi'].get(infores, {}).get(version)
    if not spec:
        return f"{infores} {version} Not found", 404
    return spec

@app.get('/utility/{infores}')
async def get_spec(infores, version):
    spec = all_specs['utility'].get(infores, {}).get('Utility')
    if not spec:
        return f"{infores} {version} Not found", 404
    return spec

@app.get('/all_servers')
async def get_all_servers():
    return get_available_servers(all_specs)

if __name__ == '__main__':
    uvicorn.run(app, port=7878)