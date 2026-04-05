import threading
import uuid
import time
from typing import Dict, Any, Optional
from models.base import AlgorithmBase
from models.entities import TaskRequest, TaskResult
from utils import http_client


class AlgorithmService:
    def __init__(self):
        self._task_threads: Dict[str, threading.Thread] = {}

    def execute(self, algorithm: AlgorithmBase, task_request: TaskRequest) -> Dict[str, Any]:
        task_id = task_request.task_id or str(uuid.uuid4())

        def run():
            try:
                self._send_status(task_id, task_request.callback_url,
                                  f"【执行中】开始执行{algorithm.description}，进度10%", 10)
                time.sleep(1)
                self._send_status(task_id, task_request.callback_url,
                                  "【执行中】处理数据，进度50%", 50)
                time.sleep(1)

                result = algorithm.execute(task_request.params)
                result['taskId'] = task_id
                result['status'] = 'COMPLETED'
                result['algorithmName'] = algorithm.name

                self._send_status(task_id, task_request.callback_url,
                                  f"【执行完成】{algorithm.description}", 100)
                self._send_result(task_id, task_request.callback_url, result)

                # 发送通知（如果请求中携带了通知上下文）
                if task_request.notification:
                    self._send_notification(task_request.notification, result)

            except Exception as e:
                print(f"Execution error: {e}")
                self._send_status(task_id, task_request.callback_url,
                                  f"【错误】{str(e)}", 0)

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        self._task_threads[task_id] = thread

        return {'taskId': task_id, 'status': 'STARTED'}

    def _send_status(self, task_id: str, callback_url: str,
                     status: str, progress: int) -> None:
        if not callback_url:
            return
        try:
            http_client.post(callback_url, json={
                'taskId': task_id,
                'status': status,
                'progress': progress,
            })
        except Exception as e:
            print(f"Failed to send status: {e}")

    def _send_result(self, task_id: str, callback_url: str,
                     result: Dict[str, Any]) -> None:
        if not callback_url:
            return
        try:
            result_url = callback_url.replace('/status', '/result')
            http_client.post(result_url, json=result)
        except Exception as e:
            print(f"Failed to send result: {e}")

    def _send_notification(self, notification: Dict, result: Dict[str, Any]) -> None:
        """通知发送（当前为预留接口，待接入消息中台后实现）"""
        ntype = notification.get('type', 'none')
        recipients = notification.get('recipients', [])
        if ntype == 'none' or not recipients:
            return
        # TODO: 接入消息中台后在此实现各类型通知发送
        print(f"[Notification] type={ntype}, recipients={recipients}, "
              f"taskId={result.get('taskId')}, status={result.get('status')}")


algorithm_service = AlgorithmService()
