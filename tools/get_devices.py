from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.requests_tool import requests_get


class GetDevicesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        params = {
            "homeId": tool_parameters["homeId"],
        }
        yield self.create_json_message(requests_get(tool_parameters["apiUrl"], self.runtime.credentials["rino_api_key"], params))
