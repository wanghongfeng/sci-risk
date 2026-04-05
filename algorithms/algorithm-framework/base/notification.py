from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class NotificationContext:
    """通知上下文，调用算法时可随请求传入"""
    type: str = "none"          # email / sms / webhook / im / none
    recipients: List[str] = field(default_factory=list)
    title: str = ""

    @classmethod
    def from_dict(cls, data: Dict) -> 'NotificationContext':
        return cls(
            type=data.get("type", "none"),
            recipients=data.get("recipients", []),
            title=data.get("title", ""),
        )


class NotificationService:
    """
    通知服务 — 接口已定义，具体实现留空，等待接入消息中台。

    已定义的通知类型:
        email   — 邮件通知
        sms     — 短信通知
        webhook — Webhook 回调
        im      — 即时消息 (企业微信/钉钉等)
    """

    def notify_email(self, recipients: List[str], title: str, content: str,
                     task_result: Dict[str, Any]) -> None:
        """发送邮件通知（待实现）"""
        pass

    def notify_sms(self, recipients: List[str], content: str) -> None:
        """发送短信通知（待实现）"""
        pass

    def notify_webhook(self, url: str, payload: Dict[str, Any]) -> None:
        """发送 Webhook 通知（待实现）"""
        pass

    def notify_im(self, recipients: List[str], content: str) -> None:
        """发送即时消息通知（待实现）"""
        pass

    def send(self, ctx: NotificationContext, task_result: Dict[str, Any],
             duration_seconds: float) -> None:
        """根据通知类型自动路由到对应接口"""
        if ctx.type == "none" or not ctx.recipients:
            return

        task_id = task_result.get("taskId", "")
        status = task_result.get("status", "")
        algo_name = task_result.get("algorithmName", "")
        content = (
            f"任务 {task_id}（{algo_name}）执行{status}，"
            f"耗时 {duration_seconds:.2f}s"
        )

        if ctx.type == "email":
            self.notify_email(
                ctx.recipients,
                ctx.title or "算法执行通知",
                content,
                task_result
            )
        elif ctx.type == "sms":
            self.notify_sms(ctx.recipients, content)
        elif ctx.type == "webhook":
            for url in ctx.recipients:
                self.notify_webhook(url, task_result)
        elif ctx.type == "im":
            self.notify_im(ctx.recipients, content)


# 全局单例
notification_service = NotificationService()
