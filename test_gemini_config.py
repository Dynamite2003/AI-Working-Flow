#!/usr/bin/env python3
"""
Gemini配置测试脚本
用于验证Gemini API配置是否正确
"""

import asyncio
import sys
import os

try:
    from env_config import get_config
    from gemini_client import create_model_client, GEMINI_AVAILABLE
    from autogen_core.models import UserMessage, SystemMessage
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保已安装所有依赖: make install")
    sys.exit(1)


async def test_gemini_basic():
    """测试Gemini基本功能"""
    print("🧪 测试Gemini基本功能...")
    
    try:
        # 加载配置
        config = get_config()
        
        if config.api.provider != "gemini":
            print(f"⚠️  当前API提供商是 {config.api.provider}，不是 gemini")
            print("请在.env文件中设置 API_PROVIDER=gemini")
            return False
        
        print(f"✅ API提供商: {config.api.provider}")
        print(f"✅ 模型: {config.api.model}")
        print(f"✅ API密钥: {config.api.api_key[:20]}...")
        
        # 检查Gemini库是否可用
        if not GEMINI_AVAILABLE:
            print("❌ google-generativeai库未安装")
            print("请运行: pip install google-generativeai")
            return False
        
        print("✅ google-generativeai库已安装")
        
        # 创建客户端
        client = create_model_client(config.api)
        print("✅ Gemini客户端创建成功")
        
        # 测试简单对话
        messages = [
            SystemMessage(content="你是一个有用的AI助手。"),
            UserMessage(content="请说'Hello, World!'", source="user")
        ]
        
        print("🔄 发送测试消息...")
        result = await client.create(messages)
        
        print("✅ 测试成功！")
        print(f"📝 Gemini响应: {result.content}")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


async def test_gemini_programming():
    """测试Gemini编程能力"""
    print("\n🧪 测试Gemini编程能力...")
    
    try:
        config = get_config()
        client = create_model_client(config.api)
        
        messages = [
            SystemMessage(content="你是一个专业的Python程序员。"),
            UserMessage(content="请编写一个简单的Python函数来计算斐波那契数列", source="user")
        ]
        
        print("🔄 发送编程任务...")
        result = await client.create(messages)
        
        print("✅ 编程测试成功！")
        print(f"📝 Gemini代码响应:\n{result.content}")
        
        await client.close()
        return True
        
    except Exception as e:
        print(f"❌ 编程测试失败: {e}")
        return False


def check_env_file():
    """检查.env文件配置"""
    print("🔍 检查.env文件配置...")
    
    if not os.path.exists(".env"):
        print("❌ .env文件不存在")
        print("请运行: make setup-env")
        return False
    
    print("✅ .env文件存在")
    
    # 读取.env文件内容
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查关键配置
    checks = [
        ("API_PROVIDER=gemini", "API提供商设置为gemini"),
        ("GEMINI_API_KEY=", "Gemini API密钥"),
        ("DEFAULT_MODEL=gemini", "默认模型设置")
    ]
    
    for check, description in checks:
        if check in content:
            print(f"✅ {description}")
        else:
            print(f"⚠️  {description} - 可能未正确配置")
    
    return True


def print_gemini_setup_guide():
    """打印Gemini设置指南"""
    print("\n📖 Gemini API设置指南:")
    print("=" * 50)
    print("1. 获取Gemini API密钥:")
    print("   - 访问: https://makersuite.google.com/app/apikey")
    print("   - 创建新的API密钥")
    print("")
    print("2. 配置.env文件:")
    print("   API_PROVIDER=gemini")
    print("   GEMINI_API_KEY=your-gemini-api-key-here")
    print("   DEFAULT_MODEL=gemini-pro")
    print("")
    print("3. 安装依赖:")
    print("   pip install google-generativeai")
    print("")
    print("4. 可用的Gemini模型:")
    print("   - gemini-pro: 文本生成")
    print("   - gemini-pro-vision: 多模态（文本+图像）")
    print("=" * 50)


async def main():
    """主函数"""
    print("🚀 Gemini配置测试工具")
    print("=" * 60)
    
    # 检查.env文件
    if not check_env_file():
        print_gemini_setup_guide()
        return
    
    # 测试基本功能
    basic_success = await test_gemini_basic()
    
    if basic_success:
        # 测试编程能力
        await test_gemini_programming()
        
        print("\n" + "=" * 60)
        print("🎉 Gemini配置测试完成！")
        print("💡 现在可以运行: make run-demo 开始使用")
    else:
        print("\n" + "=" * 60)
        print("❌ Gemini配置测试失败")
        print_gemini_setup_guide()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        print("请检查配置和网络连接")
