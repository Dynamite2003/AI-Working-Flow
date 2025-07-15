#!/usr/bin/env python3
"""
AutoGen编程工作流启动脚本
提供命令行界面来运行不同类型的编程工作流
"""

import asyncio
import argparse
import os
import sys
from typing import List

from autogen_programming_workflow import ProgrammingWorkflow, ProgrammingTask
from autogen_advanced_programming_workflow import AdvancedProgrammingWorkflow, AdvancedProgrammingTask


def check_api_key():
    """检查API密钥是否设置"""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误: 未找到OPENAI_API_KEY环境变量")
        print("请设置您的OpenAI API密钥:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)


def get_user_input(prompt: str, required: bool = True) -> str:
    """获取用户输入"""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("此字段为必填项，请重新输入。")


def get_requirements() -> List[str]:
    """获取需求列表"""
    requirements = []
    print("\n请输入项目需求（每行一个，输入空行结束）:")
    
    while True:
        req = input(f"需求 {len(requirements) + 1}: ").strip()
        if not req:
            break
        requirements.append(req)
    
    return requirements


def get_security_requirements() -> List[str]:
    """获取安全需求列表"""
    requirements = []
    print("\n请输入安全需求（每行一个，输入空行结束，可选）:")
    
    while True:
        req = input(f"安全需求 {len(requirements) + 1}: ").strip()
        if not req:
            break
        requirements.append(req)
    
    return requirements


def get_performance_requirements() -> List[str]:
    """获取性能需求列表"""
    requirements = []
    print("\n请输入性能需求（每行一个，输入空行结束，可选）:")
    
    while True:
        req = input(f"性能需求 {len(requirements) + 1}: ").strip()
        if not req:
            break
        requirements.append(req)
    
    return requirements


async def run_basic_workflow():
    """运行基础工作流"""
    print("🔥 基础编程工作流")
    print("=" * 50)
    
    # 获取任务信息
    description = get_user_input("请输入项目描述: ")
    language = get_user_input("请输入编程语言 (默认: python): ", required=False) or "python"
    requirements = get_requirements()
    
    if not requirements:
        print("❌ 至少需要一个项目需求")
        return
    
    # 创建任务
    task = ProgrammingTask(
        description=description,
        requirements=requirements,
        language=language
    )
    
    # 运行工作流
    workflow = ProgrammingWorkflow()
    try:
        await workflow.run_programming_task(task)
    finally:
        await workflow.close()


async def run_advanced_workflow():
    """运行高级工作流"""
    print("🚀 高级编程工作流")
    print("=" * 50)
    
    # 获取基本信息
    description = get_user_input("请输入项目描述: ")
    language = get_user_input("请输入编程语言 (默认: python): ", required=False) or "python"
    
    # 获取复杂度级别
    print("\n复杂度级别:")
    print("1. low - 简单项目")
    print("2. medium - 中等复杂度项目")
    print("3. high - 高复杂度项目")
    
    complexity_choice = get_user_input("请选择复杂度级别 (1-3, 默认: 2): ", required=False) or "2"
    complexity_map = {"1": "low", "2": "medium", "3": "high"}
    complexity_level = complexity_map.get(complexity_choice, "medium")
    
    # 获取需求
    requirements = get_requirements()
    if not requirements:
        print("❌ 至少需要一个项目需求")
        return
    
    # 获取安全和性能需求
    security_requirements = get_security_requirements()
    performance_requirements = get_performance_requirements()
    
    # 创建高级任务
    task = AdvancedProgrammingTask(
        description=description,
        requirements=requirements,
        language=language,
        complexity_level=complexity_level,
        security_requirements=security_requirements if security_requirements else None,
        performance_requirements=performance_requirements if performance_requirements else None
    )
    
    # 运行高级工作流
    workflow = AdvancedProgrammingWorkflow()
    try:
        await workflow.run_advanced_task(task)
    finally:
        await workflow.close()


async def run_quick_demo():
    """运行快速演示"""
    print("⚡ 快速演示模式")
    print("=" * 50)
    
    # 预定义的演示任务
    demo_tasks = {
        "1": {
            "type": "basic",
            "task": ProgrammingTask(
                description="创建一个简单的待办事项管理器",
                requirements=[
                    "支持添加、删除、标记完成任务",
                    "任务可以设置优先级",
                    "支持任务搜索功能",
                    "数据持久化存储",
                    "提供简单的命令行界面"
                ],
                language="python"
            )
        },
        "2": {
            "type": "advanced",
            "task": AdvancedProgrammingTask(
                description="开发一个简单的博客API系统",
                requirements=[
                    "用户注册和登录功能",
                    "文章的CRUD操作",
                    "评论系统",
                    "文章分类和标签",
                    "RESTful API设计"
                ],
                language="python",
                complexity_level="medium",
                security_requirements=[
                    "用户密码安全存储",
                    "API访问权限控制",
                    "防止XSS和SQL注入"
                ],
                performance_requirements=[
                    "支持100+并发用户",
                    "API响应时间<500ms",
                    "数据库查询优化"
                ]
            )
        }
    }
    
    print("选择演示任务:")
    print("1. 基础工作流 - 待办事项管理器")
    print("2. 高级工作流 - 博客API系统")
    
    choice = get_user_input("请选择 (1-2): ")
    
    if choice not in demo_tasks:
        print("❌ 无效选择")
        return
    
    demo = demo_tasks[choice]
    
    if demo["type"] == "basic":
        workflow = ProgrammingWorkflow()
        try:
            await workflow.run_programming_task(demo["task"])
        finally:
            await workflow.close()
    else:
        workflow = AdvancedProgrammingWorkflow()
        try:
            await workflow.run_advanced_task(demo["task"])
        finally:
            await workflow.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="AutoGen编程工作流启动器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run_workflow.py --mode basic     # 运行基础工作流
  python run_workflow.py --mode advanced  # 运行高级工作流
  python run_workflow.py --mode demo      # 运行快速演示
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["basic", "advanced", "demo"],
        default="basic",
        help="工作流模式 (默认: basic)"
    )
    
    args = parser.parse_args()
    
    print("🌟 AutoGen编程工作流系统")
    print("=" * 60)
    
    # 检查API密钥
    check_api_key()
    
    # 根据模式运行相应的工作流
    try:
        if args.mode == "basic":
            asyncio.run(run_basic_workflow())
        elif args.mode == "advanced":
            asyncio.run(run_advanced_workflow())
        elif args.mode == "demo":
            asyncio.run(run_quick_demo())
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        print("请检查网络连接和API密钥设置")


if __name__ == "__main__":
    main()
