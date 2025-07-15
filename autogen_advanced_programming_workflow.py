"""
AutoGen高级编程工作流 - 使用GraphFlow实现复杂的多Agent协作
支持并行处理、条件分支和消息过滤的编程工作流系统

工作流程：
1. CodeWriter -> 编写初始代码
2. CodeReviewer + SecurityAnalyzer -> 并行进行代码审阅和安全分析
3. CodeOptimizer -> 根据审阅和安全分析结果优化代码
4. TestGenerator -> 生成测试代码
5. FinalValidator -> 最终验证和总结
"""

import asyncio
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

from autogen_agentchat.agents import AssistantAgent, MessageFilterAgent, MessageFilterConfig, PerSourceFilter
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


@dataclass
class AdvancedProgrammingTask:
    """高级编程任务数据结构"""
    description: str
    requirements: List[str]
    language: str = "python"
    complexity_level: str = "medium"  # low, medium, high
    security_requirements: List[str] = None
    performance_requirements: List[str] = None


class AdvancedProgrammingWorkflow:
    """AutoGen高级编程工作流主类"""
    
    def __init__(self, model_name: str = "gpt-4o", api_key: Optional[str] = None):
        """初始化高级编程工作流"""
        self.model_client = OpenAIChatCompletionClient(
            model=model_name,
            api_key=api_key
        )
        
        # 创建所有Agent
        self.agents = self._create_all_agents()
        
        # 构建工作流图
        self.graph_flow = self._build_workflow_graph()
    
    def _create_all_agents(self) -> Dict[str, AssistantAgent]:
        """创建所有需要的Agent"""
        agents = {}
        
        # 1. 代码编写Agent
        agents['code_writer'] = AssistantAgent(
            name="CodeWriter",
            model_client=self.model_client,
            system_message="""你是一个专业的代码编写专家。请根据需求编写高质量、结构清晰的代码。
            
要求：
- 编写功能完整的代码
- 包含详细注释和文档字符串
- 遵循最佳编程实践
- 考虑错误处理和边界条件
- 提供使用示例

请在代码后添加简要说明。""",
            description="专业代码编写专家"
        )
        
        # 2. 代码审阅Agent
        agents['code_reviewer'] = AssistantAgent(
            name="CodeReviewer",
            model_client=self.model_client,
            system_message="""你是资深的代码审阅专家。请仔细审阅代码并提供详细反馈。

审阅重点：
- 代码逻辑正确性
- 算法效率和性能
- 代码可读性和维护性
- 错误处理完整性
- 编程规范遵循情况

请提供：
- 发现的问题列表
- 具体改进建议
- 代码质量评分(1-10)""",
            description="资深代码审阅专家"
        )
        
        # 3. 安全分析Agent
        agents['security_analyzer'] = AssistantAgent(
            name="SecurityAnalyzer", 
            model_client=self.model_client,
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
        )
        
        # 4. 代码优化Agent（使用消息过滤）
        optimizer_core = AssistantAgent(
            name="CodeOptimizer",
            model_client=self.model_client,
            system_message="""你是代码优化专家。请根据审阅意见和安全分析结果优化代码。

优化目标：
- 修复发现的问题
- 提升代码性能
- 增强安全性
- 改善可读性和维护性
- 保持功能完整性

请提供优化后的完整代码和改进说明。""",
            description="代码优化专家"
        )
        
        # 使用消息过滤，只接收来自审阅者和安全分析师的最新消息
        agents['code_optimizer'] = MessageFilterAgent(
            name="CodeOptimizer",
            wrapped_agent=optimizer_core,
            filter=MessageFilterConfig(
                per_source=[
                    PerSourceFilter(source="CodeWriter", position="first", count=1),
                    PerSourceFilter(source="CodeReviewer", position="last", count=1),
                    PerSourceFilter(source="SecurityAnalyzer", position="last", count=1)
                ]
            )
        )
        
        # 5. 测试生成Agent
        agents['test_generator'] = AssistantAgent(
            name="TestGenerator",
            model_client=self.model_client,
            system_message="""你是测试代码生成专家。请为优化后的代码生成全面的测试。

测试要求：
- 单元测试覆盖主要功能
- 边界条件测试
- 异常情况测试
- 性能测试（如需要）
- 安全测试（如需要）

请使用适当的测试框架（如pytest）编写测试代码。""",
            description="测试代码生成专家"
        )
        
        # 6. 最终验证Agent
        final_validator_core = AssistantAgent(
            name="FinalValidator",
            model_client=self.model_client,
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
        
        # 最终验证Agent只接收关键消息
        agents['final_validator'] = MessageFilterAgent(
            name="FinalValidator",
            wrapped_agent=final_validator_core,
            filter=MessageFilterConfig(
                per_source=[
                    PerSourceFilter(source="user", position="first", count=1),
                    PerSourceFilter(source="CodeOptimizer", position="last", count=1),
                    PerSourceFilter(source="TestGenerator", position="last", count=1)
                ]
            )
        )
        
        return agents
    
    def _build_workflow_graph(self) -> GraphFlow:
        """构建工作流图"""
        builder = DiGraphBuilder()
        
        # 添加所有节点
        for agent in self.agents.values():
            builder.add_node(agent)
        
        # 定义工作流边
        # 1. CodeWriter -> CodeReviewer 和 SecurityAnalyzer (并行)
        builder.add_edge(self.agents['code_writer'], self.agents['code_reviewer'])
        builder.add_edge(self.agents['code_writer'], self.agents['security_analyzer'])
        
        # 2. CodeReviewer 和 SecurityAnalyzer -> CodeOptimizer (汇聚)
        builder.add_edge(self.agents['code_reviewer'], self.agents['code_optimizer'])
        builder.add_edge(self.agents['security_analyzer'], self.agents['code_optimizer'])
        
        # 3. CodeOptimizer -> TestGenerator
        builder.add_edge(self.agents['code_optimizer'], self.agents['test_generator'])
        
        # 4. TestGenerator -> FinalValidator
        builder.add_edge(self.agents['test_generator'], self.agents['final_validator'])
        
        # 构建图
        graph = builder.build()
        
        # 创建GraphFlow
        return GraphFlow(
            participants=list(self.agents.values()),
            graph=graph
        )
    
    async def run_advanced_task(self, task: AdvancedProgrammingTask) -> None:
        """执行高级编程任务"""
        
        # 构建详细任务描述
        task_description = self._build_task_description(task)
        
        print("🚀 启动AutoGen高级编程工作流...")
        print("=" * 80)
        print(f"任务：{task.description}")
        print(f"语言：{task.language}")
        print(f"复杂度：{task.complexity_level}")
        print("=" * 80)
        print("工作流程：")
        print("1. CodeWriter -> 编写初始代码")
        print("2. CodeReviewer + SecurityAnalyzer -> 并行审阅和安全分析")
        print("3. CodeOptimizer -> 根据反馈优化代码")
        print("4. TestGenerator -> 生成测试代码")
        print("5. FinalValidator -> 最终验证和总结")
        print("=" * 80)
        
        # 运行工作流
        stream = self.graph_flow.run_stream(task=task_description)
        await Console(stream)
        
        print("\n" + "=" * 80)
        print("✅ 高级编程工作流完成！")
    
    def _build_task_description(self, task: AdvancedProgrammingTask) -> str:
        """构建任务描述"""
        description = f"""
高级编程任务：{task.description}

基本要求：
{chr(10).join(f"- {req}" for req in task.requirements)}

编程语言：{task.language}
复杂度级别：{task.complexity_level}
"""
        
        if task.security_requirements:
            description += f"""
安全要求：
{chr(10).join(f"- {req}" for req in task.security_requirements)}
"""
        
        if task.performance_requirements:
            description += f"""
性能要求：
{chr(10).join(f"- {req}" for req in task.performance_requirements)}
"""
        
        description += """
请按照工作流程协作完成任务，确保代码质量、安全性和可维护性。
"""
        
        return description
    
    async def close(self):
        """关闭模型客户端连接"""
        await self.model_client.close()


async def main():
    """主函数 - 演示高级编程工作流"""
    
    workflow = AdvancedProgrammingWorkflow(model_name="gpt-4o")
    
    try:
        # 定义复杂编程任务
        task = AdvancedProgrammingTask(
            description="开发一个安全的用户认证系统",
            requirements=[
                "支持用户注册、登录、注销功能",
                "实现密码加密存储",
                "支持会话管理",
                "提供用户权限控制",
                "包含完整的错误处理",
                "提供RESTful API接口"
            ],
            language="python",
            complexity_level="high",
            security_requirements=[
                "防止SQL注入攻击",
                "实现安全的密码策略",
                "支持会话超时机制",
                "防止暴力破解攻击",
                "敏感数据加密传输"
            ],
            performance_requirements=[
                "支持并发用户访问",
                "响应时间小于200ms",
                "支持数据库连接池",
                "实现缓存机制"
            ]
        )
        
        # 执行高级编程任务
        await workflow.run_advanced_task(task)
        
    finally:
        await workflow.close()


if __name__ == "__main__":
    asyncio.run(main())
