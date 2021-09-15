import os
import sys

from jinja2 import Environment, select_autoescape, FileSystemLoader
import base64
import yaml


def jinja_template(
        template_path,
        values_path,
        user_name,
        set_uuid,
        short_uuid,
        port_rtmp=None,
        nginx_rec_rtmp=None,
        nginx_encoder=None,
        role=None,
):
    config_data = yaml.safe_load(open(values_path).read())
    env = Environment(loader=FileSystemLoader('/'),
                      trim_blocks=True,
                      lstrip_blocks=True,
                      autoescape=select_autoescape(['yaml', 'yml', 'j2'])
                      )
    env.filters['b64encode'] = lambda x: base64.b64encode(x.encode('utf-8')).decode('utf-8')
    template = env.get_template(template_path)

    config_data['user_name'] = user_name
    config_data['uuid'] = set_uuid
    config_data['short_uuid'] = short_uuid
    config_data['role'] = role
    config_data['port_rtmp'] = port_rtmp
    config_data['nginx_rec_rtmp'] = nginx_rec_rtmp
    config_data['nginx_encoder'] = nginx_encoder

    rendered_template = yaml.safe_load_all(template.render(config_data))
    return rendered_template
