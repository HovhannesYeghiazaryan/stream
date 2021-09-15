import json
import uuid
from operator import itemgetter

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from k8s_app.kubernetes_api.clusters_dir import all_files
from k8s_app.kubernetes_api.create_stream_data import create_stream_diff_clusters, create_stream_single_cluster
from k8s_app.kubernetes_api.delete_stream import delete_elements
from k8s_app.kubernetes_api.collect_data import collect_clusters_data
from k8s_app import filters  # noqa
from k8s_app.kubernetes_api.get_values import main_namespace


class BaseView(View):

    def get(self, request):
        return render(request, 'base.html', {'files_path': all_files})

    def prepare_params(self, receiver_select, encoder_select, cluster_user_name):
        if encoder_select == receiver_select:
            base_uuid = str(uuid.uuid4())
            short_uuid = base_uuid[:8]
            data = [
                dict(
                    requested_file='common.yaml.j2',
                    base_uuid=base_uuid,
                    short_uuid=short_uuid,
                ),
                dict(requested_file='receiver-rtmp-deploy.yaml.j2',
                     role='receiver',
                     base_uuid=base_uuid,
                     short_uuid=short_uuid,
                     ),
                dict(requested_file='encoder-deploy.yaml.j2',
                     role='encoder',
                     base_uuid=base_uuid,
                     short_uuid=short_uuid,
                     ),
            ]
        else:
            base_uuid = str(uuid.uuid4())
            short_uuid = base_uuid[:8]
            data = [
                dict(
                    requested_file='common.yaml.j2',
                    base_uuid=base_uuid,
                    short_uuid=short_uuid,
                ),
                dict(
                    requested_file='common.yaml.j2',
                    base_uuid=base_uuid,
                    short_uuid=short_uuid,
                ),
                dict(
                    requested_file='receiver-rtmp-deploy.yaml.j2',
                    role='receiver',
                    base_uuid=base_uuid,
                    short_uuid=short_uuid,
                ),
                dict(
                    requested_file='encoder-deploy.yaml.j2',
                    role='encoder',
                    base_uuid=base_uuid,
                    short_uuid=short_uuid,
                ),
            ]
        for params in data:
            params['selected_cluster'] = encoder_select
            params['request_user_name'] = cluster_user_name

        return data

    def post(self, request):

        receiver_select, encoder_select, cluster_user_name = itemgetter(
            'receiverSelect', 'encoderSelect', 'clusterUserName'
        )(request.POST)

        if encoder_select == receiver_select:
            create_stream_func = create_stream_single_cluster
        else:
            create_stream_func = create_stream_diff_clusters

        clusters_info = collect_clusters_data()
        for params in self.prepare_params(receiver_select, encoder_select, cluster_user_name):
            create_stream_func(clusters_info, **params)

        return HttpResponseRedirect('/status/')


class StatusView(View):

    def get(self, request):
        return render(request, 'status.html', context={'clusters_metadata': collect_clusters_data()})

    def post(self, request):

        if json.loads(request.body) == 'reload':
            collect_clusters_data()
            return HttpResponseRedirect('/status/')

        elif core_uuid := json.loads(request.body)['uuid_value']:
            delete_elements(files=all_files, core_uuid=core_uuid, namespace=main_namespace)
            return HttpResponseRedirect('/status/')

        return render(request, 'status.html')
