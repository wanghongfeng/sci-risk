from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import uuid
import threading
import time
import requests


class AlgorithmBase(ABC):

    # ── 必须实现: 身份标识 ─────────────────────────────────────────

    @property
    @abstractmethod
    def name(self) -> str:
        """算法唯一标识名"""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """算法版本"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """算法描述"""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """一级分类: risk / plan / inventory / supply_chain"""
        pass

    @property
    @abstractmethod
    def algo_type(self) -> str:
        """二级分类: simulation / classification / assessment / ..."""
        pass

    # ── 可选覆盖: 展示与 Schema ────────────────────────────────────

    @property
    def label(self) -> str:
        """算法展示名称，默认取 description"""
        return self.description

    @property
    def params_schema(self) -> Dict:
        """输入参数 JSON Schema"""
        return {"type": "object", "properties": {}}

    @property
    def output_schema(self) -> Dict:
        """输出结果 JSON Schema"""
        return {"type": "object", "properties": {}}

    # ── 核心执行方法（子类实现）──────────────────────────────────

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        算法核心逻辑。
        params: 任意 JSON dict（算法自行取用所需字段）
        返回: 任意 JSON dict（不含 taskId/status/duration，由服务层补充）
        """
        pass

    # ── 基类提供的运行方法 ────────────────────────────────────────

    def run(self,
            params: Dict[str, Any],
            callback_url: Optional[str] = None,
            notification_context: Optional[Dict] = None) -> Dict[str, Any]:
        task_id = params.get("taskId", str(uuid.uuid4()))
        start_time = time.time()
        result: Dict[str, Any] = {}
        try:
            result = self.execute(params)
            result["taskId"] = task_id
            result["status"] = "COMPLETED"
            result["duration"] = round(time.time() - start_time, 3)
        except Exception as e:
            result = {
                "taskId": task_id,
                "status": "FAILED",
                "error": str(e),
                "duration": round(time.time() - start_time, 3),
            }
        if callback_url:
            self._send_callback(callback_url, result)
        return result

    def run_async(self,
                  params: Dict[str, Any],
                  callback_url: Optional[str] = None,
                  notification_context: Optional[Dict] = None) -> Dict[str, Any]:
        task_id = params.get("taskId", str(uuid.uuid4()))

        def _run():
            self.run(params, callback_url, notification_context)

        threading.Thread(target=_run, daemon=True).start()
        return {"taskId": task_id, "status": "EXECUTING", "message": f"{self.name} 任务已启动"}

    def _send_callback(self, callback_url: str, result: Dict[str, Any], timeout: int = 10):
        try:
            requests.post(callback_url, json=result, timeout=timeout)
        except Exception as e:
            print(f"Callback failed: {e}")