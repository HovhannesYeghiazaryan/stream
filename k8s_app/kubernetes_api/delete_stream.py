import os

from k8s_app.kubernetes_api.clusters_dir import CLUSTERS_DIRECTORY
from kubernetes import client, config
from kubernetes.client import ApiException


def delete_deployment(client_api, name, namespace):
    """
    Delete Deployment.apps from current namespace
    """
    try:
        client_api.delete_namespaced_deployment(
            name=name,
            namespace=namespace,
            propagation_policy='Foreground',
            async_req=True,
        )
    except ApiException as api_ex:
        raise ApiException(f'Cant delete Deployment {name}') from api_ex
    print(f'Deployment {name} in namespace {namespace} deleted')


def delete_service(client_api, name, namespace):
    """
    Delete Services from current namespace
    """
    try:
        client_api.delete_namespaced_service(
            name=name,
            namespace=namespace,
            propagation_policy='Foreground',
            async_req=True,
        )
    except ApiException as api_ex:
        raise ApiException(f'Cant delete Service {name}') from api_ex
    print(f'Service {name} in namespace {namespace} deleted')


def delete_secret(client_api, name, namespace):
    """
    Delete Secrets from current namespace
    """
    try:
        client_api.delete_namespaced_secret(
            name=name,
            namespace=namespace,
            propagation_policy='Foreground',
            async_req=True,
        )
    except ApiException as api_ex:
        raise ApiException(f'Cant delete secret {name}') from api_ex
    print(f'Secret {name} in namespace {namespace} deleted')


def delete_elements(files, core_uuid, namespace):
    """
    Loop over all clusters contexts, load kubernetes config
    check uuid equality for every kubernetes element
    if they are have same value call delete function
    for every deployment.apps, services, secrets
    """
    for file in files:
        core_v1_api = client.CoreV1Api(api_client=config.new_client_from_config(
            config_file=os.path.join(CLUSTERS_DIRECTORY, file)))

        apps_v1_api = client.AppsV1Api(api_client=config.new_client_from_config(
            config_file=os.path.join(CLUSTERS_DIRECTORY, file)))

        for deploy in apps_v1_api.list_namespaced_deployment(namespace).items:
            if core_uuid == deploy.metadata.labels['uuid']:
                delete_deployment(
                    client_api=apps_v1_api,
                    name=deploy.metadata.name,
                    namespace=namespace
                )

        for secret in core_v1_api.list_namespaced_secret(namespace).items:
            if isinstance(secret.metadata.labels, dict):
                if core_uuid == secret.metadata.labels['uuid']:
                    delete_secret(
                        client_api=core_v1_api,
                        name=secret.metadata.name,
                        namespace=namespace,
                    )

        for service in core_v1_api.list_namespaced_service(namespace).items:
            if core_uuid == service.metadata.labels['uuid']:
                delete_service(
                    client_api=core_v1_api,
                    name=service.metadata.name,
                    namespace=namespace,
                )
