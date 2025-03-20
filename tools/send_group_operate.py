from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.requests_tool import requests_post


class SendGroupOperateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        yield self.create_json_message(
            requests_post(tool_parameters["apiUrl"], self.runtime.credentials["rino_api_key"], tool_parameters["data"]))
