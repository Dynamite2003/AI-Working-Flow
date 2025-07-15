"""
AutoGen编程工作流配置文件
包含模型配置、Agent配置和工作流参数设置
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """模型配置"""
    name: str = "gpt-4o"
    api_key: Optional[str] = None
    temperature: float = 0.1
    max_tokens: Optional[int] = None
    timeout: int = 60


@dataclass 
class AgentConfig:
    """Agent配置"""
    name: str
    system_message: str
    description: str
    tools: List[str] = None


@dataclass
class WorkflowConfig:
    """工作流配置"""
    max_messages: int = 15
    termination_keywords: List[str] = None
    enable_parallel_processing: bool = True
    enable_message_filtering: bool = True


class ProgrammingWorkflowConfig:
    """编程工作流配置类"""
    
    # 模型配置
    MODEL_CONFIG = ModelConfig(
        name="gpt-4o",
        temperature=0.1,
        timeout=60
    )
    
    # 基础Agent配置
    BASIC_AGENTS = {
        "code_writer": AgentConfig(
            name="CodeWriter",
            system_message="""你是一个专业的代码编写专家。你的职责是：

1. 根据用户需求编写高质量的代码
2. 确保代码功能完整、逻辑清晰
3. 添加必要的注释和文档字符串
4. 遵循最佳编程实践

编写代码时请：
- 使用清晰的变量和函数命名
- 添加适当的错误处理
- 包含必要的导入语句
- 提供使用示例

完成代码编写后，请说明代码的主要功能和使用方法。""",
            description="专业的代码编写专家，负责根据需求编写高质量代码"
        ),
        
        "code_reviewer": AgentConfig(
            name="CodeReviewer",
            system_message="""你是一个资深的代码审阅专家。你的职责是：

1. 仔细审阅提供的代码
2. 检查代码的正确性、效率和安全性
3. 提出具体的改进建议
4. 评估代码是否符合最佳实践

审阅时请关注：
- 代码逻辑是否正确
- 是否存在潜在的bug或安全问题
- 代码效率和性能
- 可读性和维护性
- 错误处理是否充分
- 是否遵循编程规范

请提供详细的审阅报告，包括：
- 发现的问题
- 改进建议
- 代码质量评分（1-10分）

如果代码质量很高，可以说"APPROVE"表示通过审阅。""",
            description="资深代码审阅专家，负责审阅代码质量并提出改进建议"
        ),
        
        "code_optimizer": AgentConfig(
            name="CodeOptimizer", 
            system_message="""你是一个代码优化专家。你的职责是：

1. 分析原始代码和审阅意见
2. 根据审阅建议优化代码
3. 提升代码的性能、可读性和维护性
4. 确保优化后的代码功能完整

优化时请：
- 修复审阅中指出的问题
- 改进代码结构和算法效率
- 增强错误处理和边界条件检查
- 优化代码风格和注释
- 保持原有功能不变

请提供：
- 优化后的完整代码
- 优化说明和改进点总结
- 性能提升预期

完成优化后请说"OPTIMIZATION_COMPLETE"表示工作完成。""",
            description="代码优化专家，负责根据审阅意见优化和改进代码"
        )
    }
    
    # 高级Agent配置
    ADVANCED_AGENTS = {
        "security_analyzer": AgentConfig(
            name="SecurityAnalyzer",
            system_message="""你是代码安全分析专家。请从安全角度分析代码。

安全检查项：
- 输入验证和数据清理
- 权限控制和访问管理
- 敏感数据处理
- 注入攻击防护
- 异常处理安全性

请提供：
- 安全风险评估
- 安全漏洞列表
- 安全加固建议
- 安全等级评分(1-10)""",
            description="代码安全分析专家"
        ),
        
        "test_generator": AgentConfig(
            name="TestGenerator",
            system_message="""你是测试代码生成专家。请为优化后的代码生成全面的测试。

测试要求：
- 单元测试覆盖主要功能
- 边界条件测试
- 异常情况测试
- 性能测试（如需要）
- 安全测试（如需要）

请使用适当的测试框架（如pytest）编写测试代码。""",
            description="测试代码生成专家"
        ),
        
        "final_validator": AgentConfig(
            name="FinalValidator",
            system_message="""你是最终验证专家。请对整个编程工作流的结果进行最终验证和总结。

验证内容：
- 代码功能完整性
- 代码质量评估
- 安全性评估
- 测试覆盖度
- 整体项目质量

请提供最终报告和建议。完成后请说"WORKFLOW_COMPLETE"。""",
            description="最终验证和总结专家"
        )
    }
    
    # 工作流配置
    BASIC_WORKFLOW_CONFIG = WorkflowConfig(
        max_messages=15,
        termination_keywords=["OPTIMIZATION_COMPLETE", "APPROVE"],
        enable_parallel_processing=False,
        enable_message_filtering=False
    )
    
    ADVANCED_WORKFLOW_CONFIG = WorkflowConfig(
        max_messages=25,
        termination_keywords=["WORKFLOW_COMPLETE"],
        enable_parallel_processing=True,
        enable_message_filtering=True
    )
    
    # 编程语言配置
    SUPPORTED_LANGUAGES = {
        "python": {
            "file_extension": ".py",
            "test_framework": "pytest",
            "linting_tools": ["flake8", "black", "isort"],
            "security_tools": ["bandit", "safety"]
        },
        "javascript": {
            "file_extension": ".js",
            "test_framework": "jest",
            "linting_tools": ["eslint", "prettier"],
            "security_tools": ["npm audit", "snyk"]
        },
        "java": {
            "file_extension": ".java",
            "test_framework": "junit",
            "linting_tools": ["checkstyle", "spotbugs"],
            "security_tools": ["spotbugs", "owasp"]
        },
        "go": {
            "file_extension": ".go",
            "test_framework": "testing",
            "linting_tools": ["golint", "gofmt"],
            "security_tools": ["gosec", "nancy"]
        }
    }
    
    # 复杂度级别配置
    COMPLEXITY_LEVELS = {
        "low": {
            "max_functions": 5,
            "max_lines": 200,
            "security_focus": "basic",
            "performance_focus": "basic"
        },
        "medium": {
            "max_functions": 15,
            "max_lines": 500,
            "security_focus": "standard",
            "performance_focus": "standard"
        },
        "high": {
            "max_functions": 30,
            "max_lines": 1000,
            "security_focus": "advanced",
            "performance_focus": "advanced"
        }
    }
    
    # 安全检查配置
    SECURITY_CHECKS = {
        "input_validation": [
            "检查输入参数验证",
            "防止注入攻击",
            "数据类型验证"
        ],
        "authentication": [
            "身份验证机制",
            "会话管理",
            "权限控制"
        ],
        "data_protection": [
            "敏感数据加密",
            "数据传输安全",
            "数据存储安全"
        ],
        "error_handling": [
            "异常处理安全性",
            "错误信息泄露防护",
            "日志安全"
        ]
    }
    
    # 性能优化配置
    PERFORMANCE_OPTIMIZATIONS = {
        "algorithm": [
            "时间复杂度优化",
            "空间复杂度优化",
            "算法选择优化"
        ],
        "database": [
            "查询优化",
            "索引使用",
            "连接池配置"
        ],
        "caching": [
            "内存缓存",
            "分布式缓存",
            "缓存策略"
        ],
        "concurrency": [
            "并发处理",
            "异步编程",
            "线程安全"
        ]
    }


# 获取配置的便捷函数
def get_model_config() -> ModelConfig:
    """获取模型配置"""
    return ProgrammingWorkflowConfig.MODEL_CONFIG


def get_agent_config(agent_name: str) -> Optional[AgentConfig]:
    """获取指定Agent的配置"""
    all_agents = {
        **ProgrammingWorkflowConfig.BASIC_AGENTS,
        **ProgrammingWorkflowConfig.ADVANCED_AGENTS
    }
    return all_agents.get(agent_name)


def get_workflow_config(workflow_type: str = "basic") -> WorkflowConfig:
    """获取工作流配置"""
    if workflow_type == "advanced":
        return ProgrammingWorkflowConfig.ADVANCED_WORKFLOW_CONFIG
    return ProgrammingWorkflowConfig.BASIC_WORKFLOW_CONFIG


def get_language_config(language: str) -> Optional[Dict]:
    """获取编程语言配置"""
    return ProgrammingWorkflowConfig.SUPPORTED_LANGUAGES.get(language.lower())


def get_complexity_config(level: str) -> Optional[Dict]:
    """获取复杂度配置"""
    return ProgrammingWorkflowConfig.COMPLEXITY_LEVELS.get(level.lower())
