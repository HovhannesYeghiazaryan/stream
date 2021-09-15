import os
import yaml

from k8s_app.kubernetes_api.clusters_dir import TEMPLATES_DIRECTORY


path_to_values = os.path.join(TEMPLATES_DIRECTORY, 'vars.yaml')
get_namespace = yaml.safe_load(open(path_to_values).read())
main_namespace = get_namespace['namespace']
