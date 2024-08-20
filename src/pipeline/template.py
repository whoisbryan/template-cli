import os
from string import Template


# Create tmp dirs to correct flow :)
os.makedirs("tmp/templates-created/", exist_ok=True)
os.makedirs("tmp/repos/", exist_ok=True) 


def create_files(template_values):
    service_name = template_values["SERVICE_NAME"]

    f = open("templates/pipeline.tmpl", "r")
    src = Template(f.read())
    f.close()

    result = src.substitute(**template_values)

    os.makedirs(f"tmp/templates-created/{service_name}", exist_ok=True)
    tmp_dir = f"tmp/templates-created/{service_name}/{service_name}-pipeline.tmp"

    __create_file(content=result,file_path=tmp_dir)
    __copy_to_repo(result, service_name)


def __copy_to_repo(result, service_name):

    repo_dir = f"tmp/repos/{service_name}"
    os.makedirs(f"{repo_dir}/.harness/", exist_ok=True)
    __create_file(content=result,file_path=f"{repo_dir}/.harness/pipeline.yaml")


def __create_file(content, file_path):
    new_file = open(file_path, "w")
    new_file.write(content)


