import os

import httpx
import yaml
import logging
from functools import reduce
import json
import pathlib


logger = logging.getLogger()

with open(os.path.join(pathlib.Path(__file__).parent.resolve(), '..', 'servers.json')) as stream:
    server_list = json.load(stream)


def merge_specs(server_list):
    grouped = {'trapi': {}, 'utility': {}}
    for server in server_list:

        spec = get_spec(server)
        info = spec.get('info', {})
        x_tran = info.get('x-translator', {})
        info_res = x_tran.get('infores')
        store_as = 'trapi'
        trapi_v = spec.get('info', {}).get('x-trapi', {}).get('version')
        component_type = x_tran.get('component')

        if not info_res:
            logger.error(f"No infores tag found for {server}")
            continue
        if not trapi_v:
            store_as = 'utility'
            trapi_v = component_type
            if not component_type:
                logger.error(f"No Trapi or component type version specified for {server}")
                continue
        grouped_infores = grouped[store_as].get(info_res, {})
        grouped_trapi = grouped_infores.get(trapi_v, [])
        grouped_trapi.append(spec)
        grouped[store_as][info_res] = grouped_infores
        grouped[store_as][info_res][trapi_v] = grouped_trapi
    specs = {}
    for comp_type in grouped:
        sub_group = grouped[comp_type]
        all_specs = specs.get(comp_type, {})
        for info_res in sub_group:
            for trapi in sub_group[info_res]:
                leader_spec = sub_group[info_res][trapi][0]
                servers = list(reduce(lambda y, x:
                                         y + list(filter(lambda entry: entry.get('url', '').startswith('http'), x['servers'])),
                                      sub_group[info_res][trapi], []))
                leader_spec['servers'] = servers
                leader_spec['title'] = f"{info_res.replace('infores:', '').capitalize()} (Trapi v{trapi})"
                all_specs[info_res] = all_specs.get(info_res, {})
                all_specs[info_res][trapi] = leader_spec
        specs[comp_type] = all_specs
    return specs


def get_available_servers(merged_specs):
    result = {}
    for comp_type in merged_specs:
        result[comp_type] = {}
        for infores in merged_specs[comp_type]:
            result[comp_type][infores] = {}
            for trapi_v in merged_specs[comp_type][infores]:
                result[comp_type][infores][trapi_v] = merged_specs[comp_type][infores][trapi_v]['servers']
    return result


def get_spec(url):
    if url.endswith('.yaml') or url.endswith('.yml'):
        return get_yaml_spec(url)
    else:
        return get_json_spec(url)


def get_yaml_spec(url):
    with httpx.Client() as client:
        response =  client.get(url)
        if response.status_code == 200:
            return yaml.load(response.text, Loader=yaml.FullLoader)
        else:
            logger.error(f"{url} return status code {response.status_code}")
            return {}


def get_json_spec(url):
    with httpx.Client() as client:
        try:
            response = client.get(url)
        except Exception as ex:
            logger.error(f"Exception {ex.with_traceback()} reading from {url}")
            return {}
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"{url} returned status code {response.status_code}")
            return {}
