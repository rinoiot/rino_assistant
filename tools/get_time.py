from collections.abc import Generator
from typing import Any
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class GetTimeTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        timezone_input = tool_parameters["timezone"]
        
        # 标准化时区名称
        timezone_normalized = self._normalize_timezone(timezone_input)
        
        try:
            # 使用系统时间和zoneinfo库获取指定时区的时间
            tz = ZoneInfo(timezone_normalized)
            utc_now = datetime.now(timezone.utc)
            local_time = utc_now.astimezone(tz)
            
            # 获取星期信息
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekday_name = weekdays[local_time.weekday()]
            
            # 格式化时间
            formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # 获取UTC偏移量
            utc_offset = local_time.strftime('%z')
            if utc_offset:
                # 格式化为 +08:00 形式
                utc_offset = f"{utc_offset[:3]}:{utc_offset[3:]}"
            
            result = {
                "timezone": timezone_normalized,
                "current_time": formatted_time,
                "weekday": weekday_name,
                "utc_offset": utc_offset,
                "year": local_time.year,
                "month": local_time.month,
                "day": local_time.day,
                "hour": local_time.hour,
                "minute": local_time.minute,
                "second": local_time.second
            }
                
        except Exception as e:
            # 处理时区错误和其他异常
            if "ZoneInfo" in str(type(e)) or "timezone" in str(e).lower():
                result = {
                    "error": f"未知的时区: {timezone_input}",
                    "timezone": timezone_input
                }
            else:
                result = {
                    "error": f"获取时间失败: {str(e)}",
                    "timezone": timezone_input
                }
        
        yield self.create_json_message(result)
    
    def _normalize_timezone(self, timezone_str: str) -> str:
        """标准化时区名称，处理常见的大小写问题"""
        # 常见时区映射
        timezone_map = {
            # 亚洲主要时区
            "asia/shanghai": "Asia/Shanghai",
            "asia/beijing": "Asia/Shanghai",
            "asia/tokyo": "Asia/Tokyo",
            "asia/seoul": "Asia/Seoul",
            "asia/hong_kong": "Asia/Hong_Kong",
            "asia/singapore": "Asia/Singapore",
            "asia/taipei": "Asia/Taipei",
            "asia/bangkok": "Asia/Bangkok",
            "asia/jakarta": "Asia/Jakarta",
            "asia/manila": "Asia/Manila",
            "asia/kuala_lumpur": "Asia/Kuala_Lumpur",
            "asia/mumbai": "Asia/Kolkata",
            "asia/kolkata": "Asia/Kolkata",
            "asia/dubai": "Asia/Dubai",
            "asia/riyadh": "Asia/Riyadh",
            "asia/tehran": "Asia/Tehran",
            "asia/karachi": "Asia/Karachi",
            "asia/dhaka": "Asia/Dhaka",
            "asia/almaty": "Asia/Almaty",
            
            # 北美时区
            "america/new_york": "America/New_York",
            "america/chicago": "America/Chicago",
            "america/denver": "America/Denver",
            "america/los_angeles": "America/Los_Angeles",
            "america/phoenix": "America/Phoenix",
            "america/anchorage": "America/Anchorage",
            "america/honolulu": "Pacific/Honolulu",
            "america/toronto": "America/Toronto",
            "america/vancouver": "America/Vancouver",
            "america/montreal": "America/Montreal",
            "america/mexico_city": "America/Mexico_City",
            "america/guatemala": "America/Guatemala",
            "america/panama": "America/Panama",
            "america/havana": "America/Havana",
            "america/jamaica": "America/Jamaica",
            
            # 欧洲主要时区
            "europe/london": "Europe/London",
            "europe/paris": "Europe/Paris",
            "europe/berlin": "Europe/Berlin",
            "europe/rome": "Europe/Rome",
            "europe/madrid": "Europe/Madrid",
            "europe/amsterdam": "Europe/Amsterdam",
            "europe/brussels": "Europe/Brussels",
            "europe/zurich": "Europe/Zurich",
            "europe/vienna": "Europe/Vienna",
            "europe/prague": "Europe/Prague",
            "europe/warsaw": "Europe/Warsaw",
            "europe/budapest": "Europe/Budapest",
            "europe/stockholm": "Europe/Stockholm",
            "europe/oslo": "Europe/Oslo",
            "europe/copenhagen": "Europe/Copenhagen",
            "europe/helsinki": "Europe/Helsinki",
            "europe/moscow": "Europe/Moscow",
            "europe/istanbul": "Europe/Istanbul",
            "europe/athens": "Europe/Athens",
            "europe/lisbon": "Europe/Lisbon",
            "europe/dublin": "Europe/Dublin",
            
            # 其他常用时区
            "utc": "UTC",
            "gmt": "GMT",
            "est": "America/New_York",
            "cst": "America/Chicago",
            "mst": "America/Denver",
            "pst": "America/Los_Angeles",
            "cet": "Europe/Paris",
            "eet": "Europe/Athens",
            "jst": "Asia/Tokyo",
            "kst": "Asia/Seoul",
            "ist": "Asia/Kolkata",
        }
        
        # 转换为小写进行匹配
        lower_timezone = timezone_str.lower()
        
        # 如果在映射表中找到，返回标准格式
        if lower_timezone in timezone_map:
            return timezone_map[lower_timezone]
        
        # 尝试首字母大写的格式（如 Asia/Shanghai）
        parts = timezone_str.split('/')
        if len(parts) == 2:
            normalized = f"{parts[0].capitalize()}/{parts[1].capitalize()}"
            return normalized
        
        # 如果都不匹配，返回原始输入
        return timezone_str
