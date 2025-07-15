"""
AutoGen编程工作流使用示例
展示如何使用基础和高级工作流完成不同类型的编程任务
"""

import asyncio
import os
from autogen_programming_workflow import ProgrammingWorkflow, ProgrammingTask
from autogen_advanced_programming_workflow import AdvancedProgrammingWorkflow, AdvancedProgrammingTask


async def basic_workflow_example():
    """基础工作流示例"""
    print("🔥 基础工作流示例")
    print("=" * 50)
    
    # 创建工作流实例
    workflow = ProgrammingWorkflow(model_name="gpt-4o")
    
    try:
        # 示例1: 数据结构实现
        task1 = ProgrammingTask(
            description="实现一个高效的LRU缓存",
            requirements=[
                "支持get和put操作",
                "实现LRU淘汰策略", 
                "时间复杂度O(1)",
                "包含完整的错误处理",
                "提供使用示例和测试"
            ],
            language="python"
        )
        
        print("📝 任务1: LRU缓存实现")
        await workflow.run_programming_task(task1)
        
        print("\n" + "="*50)
        
        # 示例2: Web API开发
        task2 = ProgrammingTask(
            description="创建一个RESTful API服务",
            requirements=[
                "使用Flask框架",
                "实现CRUD操作",
                "支持JSON数据格式",
                "包含输入验证",
                "添加错误处理中间件",
                "提供API文档"
            ],
            language="python"
        )
        
        print("📝 任务2: RESTful API服务")
        await workflow.run_programming_task(task2)
        
    finally:
        await workflow.close()


async def advanced_workflow_example():
    """高级工作流示例"""
    print("\n🚀 高级工作流示例")
    print("=" * 50)
    
    # 创建高级工作流实例
    workflow = AdvancedProgrammingWorkflow(model_name="gpt-4o")
    
    try:
        # 示例1: 安全系统开发
        task1 = AdvancedProgrammingTask(
            description="开发一个JWT认证系统",
            requirements=[
                "实现用户注册和登录",
                "生成和验证JWT令牌",
                "支持令牌刷新机制",
                "实现权限控制装饰器",
                "提供用户信息管理接口"
            ],
            language="python",
            complexity_level="high",
            security_requirements=[
                "密码安全哈希存储",
                "防止JWT令牌泄露",
                "实现令牌黑名单机制",
                "防止暴力破解攻击",
                "敏感操作二次验证"
            ],
            performance_requirements=[
                "支持1000+并发用户",
                "令牌验证时间<10ms",
                "数据库查询优化",
                "实现Redis缓存"
            ]
        )
        
        print("🔐 任务1: JWT认证系统")
        await workflow.run_advanced_task(task1)
        
        print("\n" + "="*50)
        
        # 示例2: 分布式系统组件
        task2 = AdvancedProgrammingTask(
            description="实现一个分布式任务队列系统",
            requirements=[
                "支持任务的提交和执行",
                "实现任务优先级队列",
                "支持任务重试机制",
                "提供任务状态监控",
                "支持分布式worker节点",
                "实现负载均衡"
            ],
            language="python", 
            complexity_level="high",
            security_requirements=[
                "任务数据加密传输",
                "worker节点身份验证",
                "防止恶意任务执行"
            ],
            performance_requirements=[
                "支持10000+任务/秒",
                "任务调度延迟<100ms",
                "支持水平扩展",
                "实现故障转移机制"
            ]
        )
        
        print("⚡ 任务2: 分布式任务队列系统")
        await workflow.run_advanced_task(task2)
        
    finally:
        await workflow.close()


async def custom_task_example():
    """自定义任务示例"""
    print("\n🎨 自定义任务示例")
    print("=" * 50)
    
    workflow = ProgrammingWorkflow(model_name="gpt-4o")
    
    try:
        # 用户可以根据需要定义自己的任务
        custom_task = ProgrammingTask(
            description="创建一个智能聊天机器人",
            requirements=[
                "集成自然语言处理",
                "支持多轮对话",
                "实现意图识别",
                "支持上下文记忆",
                "提供情感分析功能",
                "支持多种输入格式"
            ],
            language="python"
        )
        
        print("🤖 自定义任务: 智能聊天机器人")
        await workflow.run_programming_task(custom_task)
        
    finally:
        await workflow.close()


async def main():
    """主函数 - 运行所有示例"""
    
    # 检查API密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  请设置OPENAI_API_KEY环境变量")
        print("export OPENAI_API_KEY='your-api-key'")
        return
    
    print("🌟 AutoGen编程工作流系统示例")
    print("=" * 60)
    
    try:
        # 运行基础工作流示例
        await basic_workflow_example()
        
        # 运行高级工作流示例  
        await advanced_workflow_example()
        
        # 运行自定义任务示例
        await custom_task_example()
        
        print("\n" + "=" * 60)
        print("✅ 所有示例运行完成！")
        
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        print("请检查API密钥和网络连接")


if __name__ == "__main__":
    # 运行示例
    asyncio.run(main())
