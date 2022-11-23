import os
from typing import List
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template


class Generator:
    PATH_TEMPLATES = os.path.dirname(os.path.realpath(__file__)) + '/templates'
    TEMPLATE_INTERFACES = 'interfaces.py.j2'
    TEMPLATE_SCENARIO = 'scenario.py.j2'
    TEMPLATE_CONTEXTS = 'contexts.py.j2'
    TEMPLATE_HELPERS = 'helpers.py.j2'
    TEMPLATE_HELPER_METHOD = 'helper_method.j2'
    TEMPLATE_VEDRO_CFG = 'vedro.cfg.py.j2'

    DIRECTORY_INTERFACES = 'interfaces'
    DIRECTORY_SCENARIOS = 'scenarios'
    DIRECTORY_CONTEXTS = 'contexts'
    DIRECTORY_HELPERS = 'helpers'

    FILE_INTERFACES = 'api.py'
    FILE_CONTEXTS = 'api.py'
    FILE_HELPERS = 'helpers.py'
    FILE_VEDRO_CFG = 'vedro.cfg.py'

    def __init__(self):
        self.environment = Environment(loader=FileSystemLoader(self.PATH_TEMPLATES))

    def get_scenario_path(self, scenario_name: str) -> str:
        return f'{self.DIRECTORY_SCENARIOS}/{scenario_name}.py'

    @staticmethod
    def get_helper_method_name(api_route: str) -> str:
        return 'prepare' + api_route.replace('/', '_').replace('.', '')

    def get_template(self, template_name: str) -> Template:
        return self.environment.get_template(name=template_name)

    @staticmethod
    def check_created_dir(dir_name: str):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    @staticmethod
    def check_created_package(package_name: str):
        if not os.path.exists(package_name):
            os.mkdir(package_name)
            Path(f'{package_name}/__init__.py').touch()

    def generate_interfaces(self):
        self.check_created_package(self.DIRECTORY_INTERFACES)
        file_path = f'{self.DIRECTORY_INTERFACES}/{self.FILE_INTERFACES}'
        if not os.path.exists(file_path):
            template = self.get_template(self.TEMPLATE_INTERFACES)
            with open(file_path, 'w') as file:
                file.write(template.render())

    def generate_contexts(self):
        self.check_created_package(self.DIRECTORY_CONTEXTS)
        template = self.get_template(self.TEMPLATE_CONTEXTS)
        file_path = f'{self.DIRECTORY_CONTEXTS}/{self.FILE_CONTEXTS}'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(template.render())

    def generate_scenario(self, route: str, file_requests: str):
        self.check_created_dir(self.DIRECTORY_SCENARIOS)
        scenario_name = file_requests.split('.')[0]
        if not os.path.exists(self.get_scenario_path(scenario_name=scenario_name)):
            template = self.get_template(self.TEMPLATE_SCENARIO)
            with open(self.get_scenario_path(scenario_name=scenario_name), 'w') as file:
                method_name = self.get_helper_method_name(route)
                file.write(template.render(
                    api_route=route,
                    file_requests=file_requests,
                    context_method_name=method_name
                ))

    def generate_helpers(self, routes: List):
        self.check_created_package(self.DIRECTORY_HELPERS)
        file_path = f'{self.DIRECTORY_HELPERS}/{self.FILE_HELPERS}'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                template = self.get_template(self.TEMPLATE_HELPERS)
                f.write(template.render())
        with open(file_path, 'r') as file:
            content = file.read()
        with open(file_path, 'a') as f:
            for route in routes:
                helper_method_name = self.get_helper_method_name(route)
                if helper_method_name not in content:
                    template = self.get_template(self.TEMPLATE_HELPER_METHOD)
                    f.write(template.render(helper_method_name=helper_method_name))

    def generate_vedro_cfg(self):
        if not os.path.exists(self.FILE_VEDRO_CFG):
            template = self.get_template(self.TEMPLATE_VEDRO_CFG)
            with open(self.FILE_VEDRO_CFG, 'w') as file:
                file.write(template.render())


def get_api_route(file_path: str) -> str:
    with open(file_path) as requests_file:
        return requests_file.readline().split('?')[0]


def requests_files(path):
    file_names = list()
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            file_names.append(file)
    return file_names


def generation():
    generator = Generator()

    generator.generate_vedro_cfg()
    generator.generate_interfaces()
    generator.generate_contexts()

    api_routes = list()
    for file_name in requests_files('requests'):
        api_route = get_api_route(f'requests/{file_name}')
        api_routes.append(api_route)
        generator.generate_scenario(route=api_route, file_requests=file_name)

    generator.generate_helpers(routes=list(set(api_routes)))
