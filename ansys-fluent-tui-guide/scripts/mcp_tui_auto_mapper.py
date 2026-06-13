#!/usr/bin/env python3
"""
MCP-TUI Command Auto-Mapper
自动将 MCP 工具调用映射到 TUI 命令，并生成 .jou 脚本

这个模块与 server.py 配合使用，当 MCP 工具被调用时：
1. 记录 MCP 工具名称和参数
2. 自动映射到对应的 TUI 命令
3. 累积命令，最后生成完整的 .jou 脚本
4. 返回映射信息给 Claude
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class TUICommand:
    """表示一个 TUI 命令"""
    command: str
    description: str
    category: str
    mcp_tool: str
    mcp_params: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_jou_line(self) -> str:
        """转换为 .jou 脚本行"""
        return self.command

    def to_dict(self) -> Dict:
        return {
            'command': self.command,
            'description': self.description,
            'category': self.category,
            'mcp_tool': self.mcp_tool,
            'mcp_params': self.mcp_params,
            'timestamp': self.timestamp
        }


class MCPToTUIMapper:
    """MCP 工具到 TUI 命令的自动映射器"""

    # MCP 工具到 TUI 命令的映射表
    MAPPING_TABLE = {
        # Fluent 文件操作
        "fluent_read_case": {
            "template": '/file/read-case "{file_path}"',
            "params_map": {"file_path": "file_path"},
            "description": "Read Fluent case file",
            "category": "file"
        },
        "fluent_read_mesh": {
            "template": '/file/read-mesh "{file_path}"',
            "params_map": {"file_path": "file_path"},
            "description": "Read mesh file",
            "category": "file"
        },
        "fluent_save": {
            "template": '/file/write-case "{prefix}.cas"\n/file/write-data "{prefix}.dat"',
            "params_map": {"prefix": "prefix"},
            "description": "Save case and data files",
            "category": "file"
        },

        # 求解器配置
        "fluent_set_solver": {
            "multi_param": True,
            "description": "Configure solver settings",
            "category": "solver",
            "mappings": {
                "viscous_model": {
                    "laminar": "/define/models/viscous laminar yes",
                    "k-epsilon": "/define/models/turbulence k-epsilon yes",
                    "k-omega": "/define/models/turbulence k-omega yes",
                    "spalart-allmaras": "/define/models/turbulence spalart-allmaras yes",
                    "sst": "/define/models/turbulence k-omega sst yes"
                },
                "energy": {
                    True: "/define/models/energy enable",
                    False: "/define/models/energy disable"
                },
                "transient": {
                    True: "/define/general/time transient",
                    False: "/define/general/time steady"
                }
            }
        },

        # 物理定义
        "fluent_set_material": {
            "template": '/define/materials/fluid {material}',
            "params_map": {"material": "material"},
            "description": "Set material properties",
            "category": "physics",
            "note": "Assumes fluid material type"
        },

        # 边界条件
        "fluent_set_boundary": {
            "multi_param": True,
            "description": "Set boundary conditions",
            "category": "boundary",
            "mappings": {
                "velocity_inlet": {
                    "template": '/define/boundary-conditions/{zone} velocity-inlet\n/define/boundary-conditions/{zone}/velocity {velocity}',
                    "params_map": {"zone": "zone", "velocity": "params.velocity"}
                },
                "pressure_outlet": {
                    "template": '/define/boundary-conditions/{zone} pressure-outlet\n/define/boundary-conditions/{zone}/gauge-pressure {pressure}',
                    "params_map": {"zone": "zone", "pressure": "params.gauge-pressure"}
                },
                "wall": {
                    "template": '/define/boundary-conditions/{zone} wall',
                    "params_map": {"zone": "zone"}
                }
            }
        },

        # 求解控制
        "fluent_initialize": {
            "template": '/solve/initialize/initialize-flow',
            "description": "Initialize flow field",
            "category": "solve"
        },
        "fluent_iterate": {
            "template": '/solve/iterate {iterations}',
            "params_map": {"iterations": "iterations"},
            "description": "Run solver iterations",
            "category": "solve"
        },

        # 其他
        "fluent_tui": {
            "template": "{command}",
            "params_map": {"command": "command"},
            "description": "Direct TUI command",
            "category": "direct"
        },
    }

    def __init__(self):
        """初始化映射器"""
        self.command_history: List[TUICommand] = []
        self.active_session = True

    def map_mcp_to_tui(self, mcp_tool: str, params: Dict[str, Any]) -> Optional[TUICommand]:
        """
        将 MCP 工具调用映射到 TUI 命令

        Args:
            mcp_tool: MCP 工具名称 (如 "fluent_set_solver")
            params: MCP 工具参数字典

        Returns:
            TUICommand 对象，或 None 如果无法映射
        """
        if mcp_tool not in self.MAPPING_TABLE:
            return None

        mapping = self.MAPPING_TABLE[mcp_tool]

        # 处理多参数情况
        if mapping.get("multi_param"):
            return self._handle_multi_param(mcp_tool, params, mapping)

        # 处理单参数情况
        template = mapping.get("template", "")
        params_map = mapping.get("params_map", {})

        try:
            # 替换模板中的参数
            formatted_command = template
            for key, param_name in params_map.items():
                value = self._get_param_value(params, param_name)
                formatted_command = formatted_command.replace(f"{{{key}}}", str(value))

            tui_cmd = TUICommand(
                command=formatted_command,
                description=mapping.get("description", ""),
                category=mapping.get("category", "unknown"),
                mcp_tool=mcp_tool,
                mcp_params=params
            )

            self.command_history.append(tui_cmd)
            return tui_cmd

        except Exception as e:
            print(f"Error mapping {mcp_tool}: {e}")
            return None

    def _handle_multi_param(self, mcp_tool: str, params: Dict[str, Any],
                            mapping: Dict) -> Optional[TUICommand]:
        """处理多参数映射"""
        commands = []

        if mcp_tool == "fluent_set_solver":
            # 处理各个求解器参数
            mappings = mapping.get("mappings", {})

            if "viscous_model" in params:
                model = params["viscous_model"]
                if model in mappings.get("viscous_model", {}):
                    commands.append(mappings["viscous_model"][model])

            if "energy" in params:
                is_enabled = params["energy"]
                cmd = mappings.get("energy", {}).get(is_enabled)
                if cmd:
                    commands.append(cmd)

            if "transient" in params:
                is_transient = params["transient"]
                cmd = mappings.get("transient", {}).get(is_transient)
                if cmd:
                    commands.append(cmd)

        elif mcp_tool == "fluent_set_boundary":
            # 处理边界条件
            bc_type = params.get("bc_type")
            zone = params.get("zone")
            bc_mapping = mapping.get("mappings", {}).get(bc_type)

            if bc_mapping:
                template = bc_mapping.get("template", "")
                params_map = bc_mapping.get("params_map", {})

                formatted = template
                for key, param_path in params_map.items():
                    value = self._get_param_value(params, param_path)
                    formatted = formatted.replace(f"{{{key}}}", str(value))

                commands.append(formatted)

        if commands:
            combined_command = "\n".join(commands)
            tui_cmd = TUICommand(
                command=combined_command,
                description=mapping.get("description", ""),
                category=mapping.get("category", "unknown"),
                mcp_tool=mcp_tool,
                mcp_params=params
            )
            self.command_history.append(tui_cmd)
            return tui_cmd

        return None

    def _get_param_value(self, params: Dict, path: str) -> Any:
        """从嵌套字典中获取参数值"""
        keys = path.split(".")
        value = params
        for key in keys:
            value = value.get(key, "")
        return value

    def generate_jou_script(self, filename: Optional[str] = None) -> str:
        """
        生成 .jou 脚本

        Args:
            filename: 可选的输出文件名

        Returns:
            生成的脚本内容
        """
        if not self.command_history:
            return ""

        script_lines = [
            "; Fluent Journal File",
            "; Auto-generated by MCP-TUI Auto-Mapper",
            f"; Generated: {datetime.now().isoformat()}",
            "; This script can be executed standalone in ANSYS Fluent",
            ""
        ]

        for cmd in self.command_history:
            script_lines.append(f"; {cmd.category.upper()}: {cmd.description}")
            script_lines.append(cmd.to_jou_line())
            script_lines.append("")

        script_content = "\n".join(script_lines)

        if filename:
            with open(filename, 'w') as f:
                f.write(script_content)

        return script_content

    def get_mapping_report(self) -> str:
        """获取映射报告（供 Claude 显示）"""
        if not self.command_history:
            return "No MCP operations tracked yet."

        report_lines = [
            "=== MCP to TUI Command Mapping Report ===\n"
        ]

        for i, cmd in enumerate(self.command_history, 1):
            report_lines.append(f"{i}. MCP Tool: {cmd.mcp_tool}")
            report_lines.append(f"   ↓ Maps to TUI:")
            for line in cmd.command.split("\n"):
                report_lines.append(f"   {line}")
            report_lines.append(f"   Description: {cmd.description}")
            report_lines.append("")

        # 添加生成的脚本
        script = self.generate_jou_script()
        report_lines.append("\n=== Generated .jou Script ===")
        report_lines.append(script)

        return "\n".join(report_lines)

    def reset(self):
        """重置映射器"""
        self.command_history = []
        self.active_session = False

    def export_to_json(self) -> str:
        """导出为 JSON 格式"""
        data = {
            "generated": datetime.now().isoformat(),
            "commands": [cmd.to_dict() for cmd in self.command_history],
            "script": self.generate_jou_script()
        }
        return json.dumps(data, indent=2)


# 全局映射器实例
_mapper_instance = MCPToTUIMapper()


def map_mcp_call(mcp_tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    便利函数：映射 MCP 工具调用到 TUI 命令

    这个函数应该在 server.py 中的每个 MCP 工具调用后被调用

    Returns:
        包含映射信息的字典
    """
    tui_cmd = _mapper_instance.map_mcp_to_tui(mcp_tool, params)

    if tui_cmd:
        return {
            "success": True,
            "mcp_tool": mcp_tool,
            "tui_command": tui_cmd.command,
            "description": tui_cmd.description,
            "category": tui_cmd.category,
            "message": f"✓ MCP → TUI Mapped\n  TUI: {tui_cmd.command}"
        }
    else:
        return {
            "success": False,
            "mcp_tool": mcp_tool,
            "message": f"⚠ No mapping found for {mcp_tool}"
        }


def get_current_script() -> str:
    """获取当前累积的 .jou 脚本"""
    return _mapper_instance.generate_jou_script()


def get_mapping_report() -> str:
    """获取完整的映射报告"""
    return _mapper_instance.get_mapping_report()


def reset_mapper():
    """重置映射器"""
    _mapper_instance.reset()


if __name__ == "__main__":
    # 示例用法
    mapper = MCPToTUIMapper()

    # 测试映射
    test_calls = [
        ("fluent_read_case", {"file_path": "mesh.cas"}),
        ("fluent_set_solver", {"viscous_model": "spalart-allmaras", "energy": True}),
        ("fluent_set_boundary", {"zone": "inlet", "bc_type": "velocity_inlet",
                                 "params": {"velocity": 5.0}}),
        ("fluent_iterate", {"iterations": 500}),
    ]

    for tool, params in test_calls:
        result = mapper.map_mcp_to_tui(tool, params)
        if result:
            print(f"\n✓ {tool}")
            print(f"  TUI: {result.command}")

    # 生成脚本
    print("\n" + "="*50)
    print("Generated .jou Script:")
    print("="*50)
    print(mapper.generate_jou_script())
