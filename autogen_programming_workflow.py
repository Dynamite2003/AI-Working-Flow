"""
AutoGen编程工作流 - 三个Agent协作编程系统
使用最新的AutoGen框架实现代码编写、审阅和优化的完整工作流

Agent1: CodeWriterAgent - 负责编写代码
Agent2: CodeReviewerAgent - 负责审阅代码并提出修改建议  
Agent3: CodeOptimizerAgent - 根据前两个agent的输出重新优化代码
"""

import asyncio
import json
import re
from typing import List, Dict, Optional
from dataclasses import dataclass

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


@dataclass
class ProgrammingTask:
    """编程任务数据结构"""
    description: str
    requirements: List[str]
    language: str = "python"


class ProgrammingWorkflow:
    """AutoGen编程工作流主类"""
    
    def __init__(self, model_name: str = "gpt-4o", api_key: Optional[str] = None):
        """
        初始化编程工作流
        
        Args:
            model_name: 使用的模型名称
            api_key: OpenAI API密钥，如果为None则从环境变量获取
        """
        self.model_client = OpenAIChatCompletionClient(
            model=model_name,
            api_key=api_key  # 如果为None，会自动从OPENAI_API_KEY环境变量获取
        )
        
        # 创建三个专门的Agent
        self.code_writer = self._create_code_writer_agent()
        self.code_reviewer = self._create_code_reviewer_agent()
        self.code_optimizer = self._create_code_optimizer_agent()
        
        # 设置终止条件
        self.termination_condition = self._create_termination_condition()
        
        # 创建团队
        self.team = self._create_team()
    
    def _create_code_writer_agent(self) -> AssistantAgent:
        """创建代码编写Agent"""
        system_message = """你是一个专业的代码编写专家。你的职责是：

1. 根据用户需求编写高质量的代码
2. 确保代码功能完整、逻辑清晰
3. 添加必要的注释和文档字符串
4. 遵循最佳编程实践

编写代码时请：
- 使用清晰的变量和函数命名
- 添加适当的错误处理
- 包含必要的导入语句
- 提供使用示例

完成代码编写后，请说明代码的主要功能和使用方法。
"""
        
        return AssistantAgent(
            name="CodeWriter",
            model_client=self.model_client,
            system_message=system_message,
            description="专业的代码编写专家，负责根据需求编写高质量代码"
        )
    
    def _create_code_reviewer_agent(self) -> AssistantAgent:
        """创建代码审阅Agent"""
        system_message = """你是一个资深的代码审阅专家。你的职责是：

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

如果代码质量很高，可以说"APPROVE"表示通过审阅。
"""
        
        return AssistantAgent(
            name="CodeReviewer", 
            model_client=self.model_client,
            system_message=system_message,
            description="资深代码审阅专家，负责审阅代码质量并提出改进建议"
        )
    
    def _create_code_optimizer_agent(self) -> AssistantAgent:
        """创建代码优化Agent"""
        system_message = """你是一个代码优化专家。你的职责是：

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

完成优化后请说"OPTIMIZATION_COMPLETE"表示工作完成。
"""
        
        return AssistantAgent(
            name="CodeOptimizer",
            model_client=self.model_client, 
            system_message=system_message,
            description="代码优化专家，负责根据审阅意见优化和改进代码"
        )
    
    def _create_termination_condition(self):
        """创建终止条件"""
        # 当优化完成或达到最大消息数时终止
        text_termination = TextMentionTermination("OPTIMIZATION_COMPLETE")
        max_messages_termination = MaxMessageTermination(max_messages=15)
        
        return text_termination | max_messages_termination
    
    def _create_team(self) -> RoundRobinGroupChat:
        """创建Agent团队"""
        return RoundRobinGroupChat(
            participants=[self.code_writer, self.code_reviewer, self.code_optimizer],
            termination_condition=self.termination_condition
        )
    
    async def run_programming_task(self, task: ProgrammingTask) -> None:
        """
        执行编程任务
        
        Args:
            task: 编程任务对象
        """
        # 构建任务描述
        task_description = f"""
编程任务：{task.description}

要求：
{chr(10).join(f"- {req}" for req in task.requirements)}

编程语言：{task.language}

请按照以下流程协作完成：
1. CodeWriter: 根据需求编写代码
2. CodeReviewer: 审阅代码并提出改进建议  
3. CodeOptimizer: 根据审阅意见优化代码

开始工作！
"""
        
        print("🚀 启动AutoGen编程工作流...")
        print("=" * 60)
        print(f"任务：{task.description}")
        print(f"语言：{task.language}")
        print("=" * 60)
        
        # 运行团队协作
        stream = self.team.run_stream(task=task_description)
        await Console(stream)
        
        print("\n" + "=" * 60)
        print("✅ 编程工作流完成！")
    
    async def close(self):
        """关闭模型客户端连接"""
        await self.model_client.close()


async def main():
    """主函数 - 演示编程工作流的使用"""
    
    # 创建编程工作流实例
    workflow = ProgrammingWorkflow(model_name="gpt-4o")
    
    try:
        # 定义编程任务
        task = ProgrammingTask(
            description="创建一个Python类来管理学生信息",
            requirements=[
                "包含学生姓名、年龄、学号、成绩等属性",
                "提供添加、删除、查询学生的方法",
                "支持按成绩排序功能",
                "包含数据验证和错误处理",
                "提供清晰的使用示例"
            ],
            language="python"
        )
        
        # 执行编程任务
        await workflow.run_programming_task(task)
        
    finally:
        # 关闭连接
        await workflow.close()


if __name__ == "__main__":
    # 运行主程序
    asyncio.run(main())
