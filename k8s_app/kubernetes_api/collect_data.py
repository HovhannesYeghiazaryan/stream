import os
from collections import defaultdict

from kubernetes import config, client
from k8s_app.kubernetes_api.clusters_dir import CLUSTERS_DIRECTORY, all_files
from k8s_app.kubernetes_api.get_values import main_namespace


def collect_clusters_data():
    collected_data = defaultdict(dict, {
        'encoder_ports': set(),
        'receiver_ports': set(),
        'all_ports': set(),
        'element_uuid': {
            'receiver': defaultdict(dict),
            'encoder': defaultdict(dict),
        },
    })

    for file in all_files:
        core_v1_api = client.CoreV1Api(api_client=config.new_client_from_config(
            config_file=os.path.join(CLUSTERS_DIRECTORY, file)))

        apps_v1_api = client.AppsV1Api(api_client=config.new_client_from_config(
            config_file=os.path.join(CLUSTERS_DIRECTORY, file)))

        cluster_pods = core_v1_api.list_namespaced_pod(main_namespace).items
        cluster_services = core_v1_api.list_namespaced_service(main_namespace).items
        cluster_node = core_v1_api.list_node().items

        for pod in cluster_pods:
            for name in ('receiver', 'encoder'):
                if name in pod.metadata.name:
                    collected_data['element_uuid'][name][pod.metadata.labels['uuid']].update(
                        {
                            'cluster_name': file,
                            'pod_phase': pod.status.phase,
                            'pod_name': pod.metadata.name,
                            'pod_host_ip': pod.status.host_ip,
                            'user_name': pod.metadata.labels['userName'],
                        }
                    )

        for service in cluster_services:
            service_uuid = service.metadata.labels['uuid']
            for port in service.spec.ports:
                for svc_component in ('receiver', 'encoder'):
                    if svc_component in service.metadata.name:
                        collected_data['all_ports'].add(port.node_port)
                        collected_data[f'{svc_component}_ports'].add(port.node_port)

                if 'receiver' in service.metadata.name:
                    if 'stream_proto' in service.metadata.labels.keys():
                        protocol = service.metadata.labels['stream_proto']
                        for proto in ('rtmp', 'http'):
                            if proto in protocol:
                                collected_data['element_uuid']['receiver'][service_uuid].update(
                                    {
                                        f'{proto}_port': port.node_port,
                                        f'{proto}_proto': proto,
                                    }
                                )
                    else:
                        for proto in ('rtmp', 'http'):
                            collected_data['element_uuid']['receiver'][service_uuid].update(
                                {
                                    f'{proto}_port': port.node_port,
                                    f'{proto}_proto': 'Unknown',
                                }
                            )

                if 'encoder' in service.metadata.name:
                    if 'stream_proto' in service.metadata.labels.keys():
                        collected_data['element_uuid']['encoder'][service_uuid].update(
                            {
                                'port': port.node_port,
                                'proto': service.metadata.labels['stream_proto'],
                            }
                        )
                    else:
                        collected_data['element_uuid']['encoder'][service_uuid].update(
                            {
                                'port': port.node_port,
                                'proto': 'Unknown',
                            }
                        )

    return collected_data
