from flask import Blueprint, request, jsonify
from services import registry_service, algorithm_service
from models.entities import TaskRequest
from config import settings


api_blueprint = Blueprint('api', __name__)


# 鈹€鈹€ 鍋ュ悍妫€鏌?鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@api_blueprint.route('/health', methods=['GET'])
def health():
    """
    鍋ュ悍妫€鏌ユ帴鍙?    ---
    tags:
      - 绯荤粺鎺ュ彛
    responses:
      200:
        description: 鏈嶅姟鍋ュ悍鐘舵€?        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            algorithms:
              type: array
              items:
                type: string
    """
    return jsonify({
        'status': 'healthy',
        'service': 'multi-algorithm-service',
        'version': '1.0.0',
        'port': settings.ALGORITHM_PORT,
        'algorithms': [algo.name for algo in registry_service.get_all()],
    })


# 鈹€鈹€ 鍒嗙被浣撶郴 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@api_blueprint.route('/categories', methods=['GET'])
def get_categories():
    """
    鑾峰彇绠楁硶涓ょ骇鍒嗙被鏍?    ---
    tags:
      - 鍒嗙被浣撶郴
    responses:
      200:
        description: 涓ょ骇鍒嗙被鏍?        schema:
          type: object
          properties:
            categories:
              type: array
              items:
                type: object
                properties:
                  category:
                    type: string
                    example: risk
                  label:
                    type: string
                    example: 椋庨櫓
                  types:
                    type: array
                    items:
                      type: object
                      properties:
                        type:
                          type: string
                          example: simulation
                        label:
                          type: string
                          example: 椋庨櫓妯℃嫙
                        count:
                          type: integer
                          example: 1
    """
    return jsonify({'categories': registry_service.get_category_tree()})


# 鈹€鈹€ 绠楁硶鍒楄〃锛堟敮鎸佹寜鍒嗙被杩囨护锛夆攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@api_blueprint.route('/algorithms', methods=['GET'])
def list_algorithms():
    """
    鑾峰彇绠楁硶鍒楄〃锛屾敮鎸佹寜 category / type 杩囨护
    ---
    tags:
      - 绠楁硶绠＄悊
    parameters:
      - name: category
        in: query
        type: string
        description: 涓€绾у垎绫昏繃婊?(risk / plan / inventory / supply_chain)
        example: risk
      - name: type
        in: query
        type: string
        description: 浜岀骇鍒嗙被杩囨护 (simulation / classification / ...)
        example: simulation
    responses:
      200:
        description: 绠楁硶鍒楄〃
    """
    category = request.args.get('category')
    algo_type = request.args.get('type')

    if category:
        algos = registry_service.get_by_category(category, algo_type)
    else:
        algos = registry_service.get_all()

    return jsonify({
        'algorithms': [
            {
                'name': a.name,
                'version': a.version,
                'label': a.label,
                'category': a.category,
                'type': a.algo_type,
                'description': a.description,
                'paramsSchema': a.params_schema,
                'outputSchema': a.output_schema,
            }
            for a in algos
        ]
    })


# 鈹€鈹€ 缁熶竴鎵ц鍏ュ彛锛堟帹鑽愶級鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@api_blueprint.route('/algorithm/execute', methods=['POST'])
def execute_unified():
    """
    缁熶竴绠楁硶鎵ц鍏ュ彛
    ---
    tags:
      - 绠楁硶鎵ц
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - algorithmName
            - callbackUrl
          properties:
            algorithmName:
              type: string
              description: 绠楁硶鍚嶇О鎴?slug
              example: tariff-risk-algorithm
            taskId:
              type: string
              description: 浠诲姟ID锛堝彲閫夛紝涓嶆彁渚涘垯鑷姩鐢熸垚锛?            callbackUrl:
              type: string
              description: 鐘舵€佸洖璋僓RL
              example: http://localhost:8080/api/simulation/status
            params:
              type: object
              description: 绠楁硶鍙傛暟锛堜换鎰?JSON锛岀敱鍚勭畻娉曞畾涔夛級
              example: {"tariffRate": 25}
            notification:
              type: object
              description: 閫氱煡閰嶇疆锛堝彲閫夛級
              properties:
                type:
                  type: string
                  enum: [email, sms, webhook, im, none]
                  example: email
                recipients:
                  type: array
                  items:
                    type: string
                  example: ["user@example.com"]
                title:
                  type: string
                  example: 鍏崇◣椋庨櫓妯℃嫙瀹屾垚閫氱煡
    responses:
      200:
        description: 浠诲姟鍚姩鎴愬姛
        schema:
          type: object
          properties:
            taskId:
              type: string
            status:
              type: string
              example: STARTED
      400:
        description: 鍙傛暟閿欒
      404:
        description: 绠楁硶涓嶅瓨鍦?    """
    data = request.get_json() or {}
    algorithm_name = data.get('algorithmName')
    if not algorithm_name:
        return jsonify({'error': 'Missing algorithmName'}), 400

    algorithm = registry_service.get(algorithm_name)
    if not algorithm:
        return jsonify({'error': f'Algorithm {algorithm_name} not found'}), 404

    # 灏?params 瀛愬璞″睍寮€锛屽苟淇濈暀 taskId/callbackUrl/notification 瀛楁
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

    return jsonify(algorithm_service.execute(algorithm, task_request))


# 鈹€鈹€ 鏃х増鎵ц璺敱锛堜繚鐣欏吋瀹癸級鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

@api_blueprint.route('/<algorithm_name>/execute', methods=['POST'])
def execute_legacy(algorithm_name):
    """
    鍏煎鏃х増鎵ц鎺ュ彛锛?{algorithm_name}/execute锛?    ---
    tags:
      - 绠楁硶鎵ц
    parameters:
      - name: algorithm_name
        in: path
        type: string
        required: true
        description: 绠楁硶 slug (tariff / scenario)
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - callbackUrl
          properties:
            taskId:
              type: string
            callbackUrl:
              type: string
              example: http://localhost:8080/api/simulation/status
            notification:
              type: object
              description: 閫氱煡閰嶇疆锛堝彲閫夛級
    responses:
      200:
        description: 浠诲姟鍚姩鎴愬姛
      400:
        description: 鍙傛暟閿欒
      404:
        description: 绠楁硶涓嶅瓨鍦?    """
    algorithm = registry_service.get(algorithm_name)
    if not algorithm:
        return jsonify({'error': f'Algorithm {algorithm_name} not found'}), 404

    task_request = TaskRequest.from_dict(request.get_json() or {})
    if not task_request.callback_url:
        return jsonify({'error': 'Missing callbackUrl'}), 400

    return jsonify(algorithm_service.execute(algorithm, task_request))


# 鈹€鈹€ 娉ㄥ唽鍒板悗绔紙鏈嶅姟鍚姩鏃惰皟鐢級鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

def register_algorithms():
    try:
        for meta in registry_service.get_metadata():
            from utils import http_client
            response = http_client.post(
                f"{settings.BACKEND_URL}/api/algorithm/register",
                json={
                    'name': meta.name,
                    'version': meta.version,
                    'endpoint': meta.endpoint,
                    'description': meta.description,
                    'category': meta.category,
                    'type': meta.algo_type,
                    'label': meta.label,
                    'paramsSchema': meta.params_schema,
                    'outputSchema': meta.output_schema,
                }
            )
            print(f"Registered {meta.name}: {response.status_code}")
    except Exception as e:
        print(f"Failed to register to backend (non-critical): {e}")
        print("Service will continue running without registration")
