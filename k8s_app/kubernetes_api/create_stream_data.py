import os

from k8s_app.kubernetes_api.create_stream import create_stream
from k8s_app.kubernetes_api.clusters_dir import CLUSTERS_DIRECTORY, TEMPLATES_DIRECTORY
from k8s_app.kubernetes_api.port_generator import set_diff_ports, set_single_ports

vars_template = os.path.join(TEMPLATES_DIRECTORY, 'vars.yaml')
deployment_file = TEMPLATES_DIRECTORY
config_file_path = CLUSTERS_DIRECTORY


def create_stream_diff_clusters(
        clusters_info,
        selected_cluster,
        request_user_name,
        requested_file,
        base_uuid,
        short_uuid,
        role=None,
):

    ports = set_diff_ports(clusters_info)

    create_stream(
        config_file=os.path.join(config_file_path, selected_cluster),
        user_name=f'{request_user_name}-{short_uuid}',
        template_name=os.path.join(deployment_file, requested_file),
        template_value=vars_template,
        role=role,
        short_uuid=short_uuid,
        tmpl_uuid=base_uuid,
        port_rtmp=ports['port_rtmp'],
        nginx_rec_rtmp=ports['nginx_rec_rtmp'],
        nginx_encoder=ports['nginx_encoder'],
    )


def create_stream_single_cluster(
        clusters_info,
        selected_cluster,
        request_user_name,
        requested_file,
        base_uuid,
        short_uuid,
        role=None,
):

    ports = set_single_ports(clusters_info)

    create_stream(
        config_file=os.path.join(config_file_path, selected_cluster),
        user_name=f'{request_user_name}-{short_uuid}',
        template_name=os.path.join(deployment_file, requested_file),
        template_value=vars_template,
        role=role,
        short_uuid=short_uuid,
        tmpl_uuid=base_uuid,
        port_rtmp=ports['port_rtmp'],
        nginx_rec_rtmp=ports['nginx_rec_rtmp'],
        nginx_encoder=ports['nginx_encoder'],
    )
