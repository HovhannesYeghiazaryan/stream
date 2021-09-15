from kubernetes import utils, client, config
from k8s_app.kubernetes_api.get_values import main_namespace
from k8s_app.kubernetes_api.jinja_renderer import jinja_template


def create_stream(
        config_file,
        user_name,
        template_name,
        template_value,
        short_uuid,
        role,
        tmpl_uuid,
        port_rtmp,
        nginx_rec_rtmp,
        nginx_encoder,
):

    config.load_kube_config(config_file=config_file)
    k8s_client = client.ApiClient()
    received_data = jinja_template(
        template_path=template_name,
        values_path=template_value,
        user_name=user_name,
        set_uuid=tmpl_uuid,
        short_uuid=short_uuid,
        role=role,
        port_rtmp=port_rtmp,
        nginx_rec_rtmp=nginx_rec_rtmp,
        nginx_encoder=nginx_encoder,
    )
    try:
        for data in received_data:
            utils.create_from_dict(
                k8s_client=k8s_client,
                data=data,
                namespace=main_namespace,
                verbose=True,
            )
    except Exception as ex:
        raise Exception(f'Create stream failed {ex}')

