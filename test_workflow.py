"""
AutoGen编程工作流测试文件
用于测试基础和高级工作流的功能
"""

import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock
import pytest

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from autogen_programming_workflow import ProgrammingWorkflow, ProgrammingTask
from autogen_advanced_programming_workflow import AdvancedProgrammingWorkflow, AdvancedProgrammingTask
from config import get_model_config, get_agent_config, get_workflow_config


class TestProgrammingWorkflow:
    """基础编程工作流测试类"""
    
    def test_programming_task_creation(self):
        """测试编程任务创建"""
        task = ProgrammingTask(
            description="测试任务",
            requirements=["需求1", "需求2"],
            language="python"
        )
        
        assert task.description == "测试任务"
        assert len(task.requirements) == 2
        assert task.language == "python"
    
    def test_workflow_initialization(self):
        """测试工作流初始化"""
        # 使用模拟的API密钥进行测试
        workflow = ProgrammingWorkflow(
            model_name="gpt-4o",
            api_key="test-key"
        )
        
        assert workflow.code_writer.name == "CodeWriter"
        assert workflow.code_reviewer.name == "CodeReviewer" 
        assert workflow.code_optimizer.name == "CodeOptimizer"
        assert workflow.team is not None
    
    def test_agent_system_messages(self):
        """测试Agent系统消息配置"""
        workflow = ProgrammingWorkflow(api_key="test-key")
        
        # 检查系统消息是否包含关键词
        writer_msg = workflow.code_writer.system_message
        assert "代码编写专家" in writer_msg
        assert "高质量" in writer_msg
        
        reviewer_msg = workflow.code_reviewer.system_message
        assert "审阅专家" in reviewer_msg
        assert "改进建议" in reviewer_msg
        
        optimizer_msg = workflow.code_optimizer.system_message
        assert "优化专家" in optimizer_msg
        assert "OPTIMIZATION_COMPLETE" in optimizer_msg


class TestAdvancedProgrammingWorkflow:
    """高级编程工作流测试类"""
    
    def test_advanced_task_creation(self):
        """测试高级编程任务创建"""
        task = AdvancedProgrammingTask(
            description="高级测试任务",
            requirements=["需求1", "需求2"],
            language="python",
            complexity_level="high",
            security_requirements=["安全需求1"],
            performance_requirements=["性能需求1"]
        )
        
        assert task.description == "高级测试任务"
        assert task.complexity_level == "high"
        assert len(task.security_requirements) == 1
        assert len(task.performance_requirements) == 1
    
    def test_advanced_workflow_initialization(self):
        """测试高级工作流初始化"""
        workflow = AdvancedProgrammingWorkflow(api_key="test-key")
        
        # 检查所有Agent是否正确创建
        expected_agents = [
            "code_writer", "code_reviewer", "security_analyzer",
            "code_optimizer", "test_generator", "final_validator"
        ]
        
        for agent_name in expected_agents:
            assert agent_name in workflow.agents
        
        assert workflow.graph_flow is not None
    
    def test_workflow_graph_structure(self):
        """测试工作流图结构"""
        workflow = AdvancedProgrammingWorkflow(api_key="test-key")
        
        # 验证图流包含所有参与者
        participants = workflow.graph_flow.participants
        assert len(participants) == 6
        
        # 验证Agent名称
        agent_names = [agent.name for agent in participants]
        expected_names = [
            "CodeWriter", "CodeReviewer", "SecurityAnalyzer",
            "CodeOptimizer", "TestGenerator", "FinalValidator"
        ]
        
        for name in expected_names:
            assert name in agent_names


class TestConfiguration:
    """配置测试类"""
    
    def test_model_config(self):
        """测试模型配置"""
        config = get_model_config()
        
        assert config.name == "gpt-4o"
        assert config.temperature == 0.1
        assert config.timeout == 60
    
    def test_agent_config(self):
        """测试Agent配置"""
        writer_config = get_agent_config("code_writer")
        assert writer_config is not None
        assert writer_config.name == "CodeWriter"
        assert "代码编写专家" in writer_config.system_message
        
        reviewer_config = get_agent_config("code_reviewer")
        assert reviewer_config is not None
        assert reviewer_config.name == "CodeReviewer"
        
        # 测试不存在的Agent
        invalid_config = get_agent_config("invalid_agent")
        assert invalid_config is None
    
    def test_workflow_config(self):
        """测试工作流配置"""
        basic_config = get_workflow_config("basic")
        assert basic_config.max_messages == 15
        assert not basic_config.enable_parallel_processing
        
        advanced_config = get_workflow_config("advanced")
        assert advanced_config.max_messages == 25
        assert advanced_config.enable_parallel_processing


class TestTaskExecution:
    """任务执行测试类（需要真实API密钥）"""
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="需要OPENAI_API_KEY环境变量"
    )
    async def test_simple_task_execution(self):
        """测试简单任务执行"""
        workflow = ProgrammingWorkflow()
        
        task = ProgrammingTask(
            description="编写一个简单的Hello World函数",
            requirements=[
                "函数名为hello_world",
                "返回字符串'Hello, World!'",
                "包含文档字符串"
            ],
            language="python"
        )
        
        try:
            # 这里只是测试工作流能否正常启动
            # 实际执行会调用OpenAI API
            assert workflow.team is not None
            assert len(workflow.team.participants) == 3
            
        finally:
            await workflow.close()
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="需要OPENAI_API_KEY环境变量"
    )
    async def test_advanced_task_setup(self):
        """测试高级任务设置"""
        workflow = AdvancedProgrammingWorkflow()
        
        task = AdvancedProgrammingTask(
            description="创建一个简单的计算器类",
            requirements=[
                "支持基本数学运算",
                "包含错误处理"
            ],
            language="python",
            complexity_level="low"
        )
        
        try:
            # 测试任务描述构建
            task_description = workflow._build_task_description(task)
            assert "简单的计算器类" in task_description
            assert "python" in task_description.lower()
            
        finally:
            await workflow.close()


def run_unit_tests():
    """运行单元测试"""
    print("🧪 运行AutoGen编程工作流单元测试")
    print("=" * 50)
    
    # 基础测试
    test_basic = TestProgrammingWorkflow()
    test_basic.test_programming_task_creation()
    test_basic.test_workflow_initialization()
    test_basic.test_agent_system_messages()
    print("✅ 基础工作流测试通过")
    
    # 高级测试
    test_advanced = TestAdvancedProgrammingWorkflow()
    test_advanced.test_advanced_task_creation()
    test_advanced.test_advanced_workflow_initialization()
    test_advanced.test_workflow_graph_structure()
    print("✅ 高级工作流测试通过")
    
    # 配置测试
    test_config = TestConfiguration()
    test_config.test_model_config()
    test_config.test_agent_config()
    test_config.test_workflow_config()
    print("✅ 配置测试通过")
    
    print("\n🎉 所有单元测试通过！")


async def run_integration_tests():
    """运行集成测试（需要API密钥）"""
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  跳过集成测试：需要OPENAI_API_KEY环境变量")
        return
    
    print("🔗 运行集成测试")
    print("=" * 50)
    
    test_execution = TestTaskExecution()
    
    try:
        await test_execution.test_simple_task_execution()
        print("✅ 简单任务执行测试通过")
        
        await test_execution.test_advanced_task_setup()
        print("✅ 高级任务设置测试通过")
        
        print("\n🎉 所有集成测试通过！")
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")


async def main():
    """主测试函数"""
    print("🚀 AutoGen编程工作流测试套件")
    print("=" * 60)
    
    # 运行单元测试
    run_unit_tests()
    
    # 运行集成测试
    await run_integration_tests()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")


if __name__ == "__main__":
    asyncio.run(main())
