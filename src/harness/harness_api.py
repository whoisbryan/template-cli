import requests
import os
from rich import print

from dotenv import load_dotenv

load_dotenv()  # This line brings all environment variables from .env into os.environ

HARNESS_TOKEN = os.environ['HARNESS_TOKEN']
HARNESS_ACCOUNT = os.environ['HARNESS_ACCOUNT']


def get_orgs():
        # La URL de la API con los parámetros de consulta incluidos
    url = "https://app.harness.io/v1/orgs"

    # Los parámetros de consulta (query parameters)
    params = {
        'page': 0,
        'sort': 'name',
        'order': 'ASC'
    }

    # Los encabezados (headers) de la petición
    headers = {
        'Harness-Account': HARNESS_ACCOUNT,
        'x-api-key': HARNESS_TOKEN
    }
    # Realizar una solicitud GET a la API
    response = requests.get(url, headers=headers, params=params)

    orgs = response.json()

    orgs_json = [{"identifier": org['org']['identifier'], "name": org['org']['name']} for org in orgs]

    identifier_name_dict = {org['org']['identifier']: org['org']['name'] for org in orgs}
    # print (orgs_json)
    return orgs_json


def get_projects_in_org(org_id : str):
    # print(org_id)
    # La URL de la API con los parámetros de consulta incluidos
    url = "https://app.harness.io/ng/api/projects"

    # Los parámetros de consulta (query parameters)
    params = {
        'accountIdentifier': HARNESS_ACCOUNT,
        'orgIdentifier': org_id,
        'pageIndex': 0,
        'sortOrders': 'fieldName=string&orderType=ASC'
    }

    # Los encabezados (headers) de la petición
    headers = {
        'x-api-key': HARNESS_TOKEN
    }
    # Realizar una solicitud GET a la API
    response = requests.get(url, headers=headers, params=params).json()

    # print(response)
    # Extraer los proyectos
    projects = response.get('data', {}).get('content', [])
    # print(projects)
    # Crear un json con los identificadores y nombres
    projects_json = [{"identifier": project['project']['identifier'], "name": project['project']['name']} for project in projects]

    return projects_json


def get_templates_dir():
    # TODO: tagear los templates e intentar traer por tags, para que solo muestre los templates para pipelines.
    url = 'https://app.harness.io/v1/templates'

    headers = {
        'Harness-Account': HARNESS_ACCOUNT,
        'x-api-key': HARNESS_TOKEN
    }
    params = {
        'page': 0,
        'sort': 'identifier',
        'order': 'ASC',
        'type': 'STABLE_TEMPLATE',
        'recursive': 'false',
        'entity_types': 'Pipeline'
    }

    response = requests.get(url, headers=headers, params=params)

    filtered_templates_json = [{"identifier": template["identifier"], "name": template["name"]} for template in response.json()] # if "pipeline" in template.get("tags", {})

    return filtered_templates_json


def create_pipeline(template_values):

    from pathlib import Path

    url = f'https://app.harness.io/v1/orgs/{template_values["ORG_ID"]}/projects/{template_values["PROJECT_ID"]}/pipelines'  # Reemplaza {org} y {project} con los valores correspondientes

    headers = {
        'Content-Type': 'application/json',
        'Harness-Account': HARNESS_ACCOUNT,  
        'x-api-key': HARNESS_TOKEN 
    }

    pipeline_yaml = Path('tmp/templates-created/solarie/solarie-pipeline.tmp').read_text()

    data = {
        "pipeline_yaml": pipeline_yaml,
        "identifier": template_values["SERVICE_NAME_UNDERSCORE"],
        "name": template_values["SERVICE_NAME"],
        "description": f"Pipeline for service {template_values["SERVICE_NAME"]}",
        "tags": {},
        "git_details": {
            "branch_name": "main", 
            "file_path": ".harness/pipeline.yaml",
            "commit_message": "Added Harness Pipeline",
            "connector_ref": "account.GitHub_App",
            "store_type": "REMOTE",
            "repo_name": template_values["SERVICE_NAME"]
        }
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Imprimir el código de estado de la respuesta y el contenido
    # print(response.status_code)
    # if response.status_code > 200 and response.status_code < 400:
    #     print(Padding(f"[i bold]Done[/i bold] ✅", 1))
    # print(response.json())  # Si la respuesta es JSON

    return response