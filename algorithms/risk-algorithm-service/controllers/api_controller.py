from flask import Blueprint, request, jsonify
from services import registry_service, algorithm_service, discovery_service
from models.entities import TaskRequest
from config import settings


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'multi-algorithm-service',
        'version': '1.0.0',
        'port': settings.ALGORITHM_PORT,
        'algorithms': [algo.name for algo in registry_service.get_all()],
        'remoteAlgorithms': [algo.name for algo in registry_service.get_all_remote()],
    })


@api_blueprint.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': registry_service.get_category_tree()})


@api_blueprint.route('/algorithms', methods=['GET'])
def list_algorithms():
    category = request.args.get('category')
    algo_type = request.args.get('type')
    include_remote = request.args.get('includeRemote', 'true').lower() == 'true'

    if category:
        algos = registry_service.get_by_category(category, algo_type)
        result = [
            {
                'name': a.name,
                'version': a.version,
                'label': a.label,
                'category': a.category,
                'type': a.algo_type,
                'description': a.description,
                'paramsSchema': a.params_schema,
                'outputSchema': a.output_schema,
                'isRemote': False,
            }
            for a in algos
        ]
    else:
        result = registry_service.get_all_algorithms() if include_remote else [
            {
                'name': a.name,
                'version': a.version,
                'label': a.label,
                'category': a.category,
                'type': a.algo_type,
                'description': a.description,
                'paramsSchema': a.params_schema,
                'outputSchema': a.output_schema,
                'isRemote': False,
            }
            for a in registry_service.get_all()
        ]

    return jsonify({'algorithms': result})


@api_blueprint.route('/algorithm/execute', methods=['POST'])
def execute_unified():
    data = request.get_json() or {}
    algorithm_name = data.get('algorithmName')
    if not algorithm_name:
        return jsonify({'error': 'Missing algorithmName'}), 400

    local_algo = registry_service.get(algorithm_name)
    if local_algo:
        inner_params = data.get('params') or {}
        flat = {
            'taskId': data.get('taskId', ''),
            'callbackUrl': data.get('callbackUrl', ''),
            'notification': data.get('notification'),
            **inner_params,
        }
        task_request = TaskRequest.from_dict(flat)
        if not task_request.callback_url:
            return jsonify({'error': 'Missing callbackUrl'}), 400
        return jsonify(algorithm_service.execute(local_algo, task_request))

    remote_algo = registry_service.get_remote(algorithm_name)
    if remote_algo:
        return jsonify(discovery_service.execute_remote_algorithm(algorithm_name, data))

    return jsonify({'error': f'Algorithm {algorithm_name} not found'}), 404


@api_blueprint.route('/<algorithm_name>/execute', methods=['POST'])
def execute_legacy(algorithm_name):
    local_algo = registry_service.get(algorithm_name)
    if local_algo:
        task_request = TaskRequest.from_dict(request.get_json() or {})
        if not task_request.callback_url:
            return jsonify({'error': 'Missing callbackUrl'}), 400
        return jsonify(algorithm_service.execute(local_algo, task_request))

    remote_algo = registry_service.get_remote(algorithm_name)
    if remote_algo:
        return jsonify(discovery_service.execute_remote_algorithm(
            algorithm_name, request.get_json() or {}))

    return jsonify({'error': f'Algorithm {algorithm_name} not found'}), 404


@api_blueprint.route('/remote-services', methods=['GET'])
def list_remote_services():
    services = discovery_service.get_remote_services()
    return jsonify({'remoteServices': services})


@api_blueprint.route('/remote-services', methods=['POST'])
def add_remote_service():
    data = request.get_json() or {}
    name = data.get('name')
    base_url = data.get('baseUrl')
    if not name or not base_url:
        return jsonify({'error': 'Missing name or baseUrl'}), 400

    discovery_service.register_remote_service(
        name=name,
        base_url=base_url,
        health_endpoint=data.get('healthEndpoint', '/health'),
        algorithms_endpoint=data.get('algorithmsEndpoint', '/algorithms'),
        execute_endpoint=data.get('executeEndpoint', '/algorithm/execute'),
    )

    remote_algos = discovery_service.discover_remote_algorithms(force_refresh=True)
    registry_service.sync_remote_algorithms(remote_algos)

    return jsonify({'message': f'Remote service {name} added', 'algorithmsDiscovered': len(remote_algos)})


@api_blueprint.route('/remote-services/<service_name>/refresh', methods=['POST'])
def refresh_remote_service(service_name: str):
    services = discovery_service.get_remote_services()
    if not any(s['name'] == service_name for s in services):
        return jsonify({'error': f'Remote service {service_name} not found'}), 404

    remote_algos = discovery_service.discover_remote_algorithms(force_refresh=True)
    registry_service.sync_remote_algorithms(remote_algos)
    return jsonify({'message': 'Refreshed', 'algorithmsCount': len(remote_algos)})


def register_algorithms():
    pass