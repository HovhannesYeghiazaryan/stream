from k8s_app.kubernetes_api.utils import allocate_port


def set_diff_ports(clusters_info):
    used_ports = clusters_info['receiver_ports']
    port_rtmp = allocate_port(used_ports)
    nginx_rec_rtmp = allocate_port(used_ports)
    nginx_encoder = allocate_port(clusters_info['encoder_ports'])

    return dict(
        port_rtmp=port_rtmp,
        nginx_rec_rtmp=nginx_rec_rtmp,
        nginx_encoder=nginx_encoder,
    )


def set_single_ports(clusters_info):
    used_ports = clusters_info['all_ports']
    port_rtmp = allocate_port(used_ports)
    nginx_rec_rtmp = allocate_port(used_ports)
    nginx_encoder = allocate_port(used_ports)

    return dict(
        port_rtmp=port_rtmp,
        nginx_rec_rtmp=nginx_rec_rtmp,
        nginx_encoder=nginx_encoder,
    )
