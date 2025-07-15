#!/usr/bin/env python3
"""
AutoGen编程工作流配置验证脚本
用于验证.env配置文件的正确性
"""

import sys
import os
from pathlib import Path

try:
    from env_config import get_config, EnvironmentConfig
except ImportError:
    print("❌ 无法导入env_config模块，请确保文件存在")
    sys.exit(1)


def check_env_file():
    """检查.env文件是否存在"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    print("🔍 检查配置文件...")
    
    if not env_file.exists():
        print("❌ .env文件不存在")
        if env_example.exists():
            print("💡 建议运行: make setup-env 或 cp .env.example .env")
        else:
            print("💡 请创建.env文件并设置必要的配置")
        return False
    
    print("✅ .env文件存在")
    return True


def validate_configuration():
    """验证配置"""
    try:
        print("\n🔧 加载配置...")
        config = get_config()
        
        print("✅ 配置加载成功")
        
        print("\n🔍 验证配置...")
        errors = config.validate_config()
        
        if errors:
            print("❌ 配置验证失败:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        print("✅ 配置验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        return False


def print_config_summary():
    """打印配置摘要"""
    try:
        config = get_config()
        
        print("\n📋 配置摘要:")
        print("=" * 50)
        
        # OpenAI配置
        print("🤖 OpenAI配置:")
        print(f"  模型: {config.openai.model}")
        print(f"  温度: {config.openai.temperature}")
        print(f"  超时: {config.openai.timeout}秒")
        if config.openai.base_url:
            print(f"  基础URL: {config.openai.base_url}")
        
        # 工作流配置
        print("\n⚙️  工作流配置:")
        print(f"  基础工作流最大消息数: {config.workflow.basic_max_messages}")
        print(f"  高级工作流最大消息数: {config.workflow.advanced_max_messages}")
        print(f"  并行处理: {'启用' if config.workflow.enable_parallel_processing else '禁用'}")
        print(f"  消息过滤: {'启用' if config.workflow.enable_message_filtering else '禁用'}")
        print(f"  安全分析: {'启用' if config.workflow.enable_security_analysis else '禁用'}")
        print(f"  性能优化: {'启用' if config.workflow.enable_performance_optimization else '禁用'}")
        
        # 项目配置
        print("\n📁 项目配置:")
        print(f"  项目名称: {config.project.name}")
        print(f"  版本: {config.project.version}")
        print(f"  默认语言: {config.project.default_language}")
        print(f"  结果目录: {config.project.results_dir}")
        print(f"  调试模式: {'启用' if config.project.debug_mode else '禁用'}")
        print(f"  保存中间结果: {'启用' if config.project.save_intermediate_results else '禁用'}")
        
        # 日志配置
        print("\n📝 日志配置:")
        print(f"  日志级别: {config.logging.level}")
        print(f"  详细日志: {'启用' if config.logging.verbose else '禁用'}")
        print(f"  彩色输出: {'启用' if config.logging.enable_color else '禁用'}")
        if config.logging.file_path:
            print(f"  日志文件: {config.logging.file_path}")
        
        # 缓存配置
        print("\n💾 缓存配置:")
        print(f"  启用缓存: {'是' if config.cache.enable_cache else '否'}")
        if config.cache.enable_cache:
            print(f"  过期时间: {config.cache.expiry_hours}小时")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 无法打印配置摘要: {e}")


def check_api_connectivity():
    """检查API连接性"""
    try:
        print("\n🌐 检查API连接性...")
        
        config = get_config()
        
        # 这里可以添加实际的API连接测试
        # 为了避免消耗API配额，这里只做基本检查
        
        if not config.openai.api_key:
            print("❌ API密钥未设置")
            return False
        
        if not config.openai.api_key.startswith('sk-'):
            print("⚠️  API密钥格式可能不正确（应以'sk-'开头）")
        
        print("✅ API配置看起来正确")
        print("💡 实际连接性需要在运行工作流时验证")
        return True
        
    except Exception as e:
        print(f"❌ API连接性检查失败: {e}")
        return False


def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    
    required_packages = [
        'autogen_agentchat',
        'autogen_core', 
        'autogen_ext',
        'openai',
        'python_dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('_', '-'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 请安装缺失的包: pip install {' '.join(missing_packages)}")
        print("或运行: make install")
        return False
    
    print("✅ 所有依赖包已安装")
    return True


def main():
    """主函数"""
    print("🔍 AutoGen编程工作流配置验证")
    print("=" * 60)
    
    success = True
    
    # 检查.env文件
    if not check_env_file():
        success = False
    
    # 检查依赖包
    if not check_dependencies():
        success = False
    
    # 验证配置
    if not validate_configuration():
        success = False
    
    # 检查API连接性
    if not check_api_connectivity():
        success = False
    
    # 打印配置摘要
    if success:
        print_config_summary()
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 所有检查通过！系统已准备就绪")
        print("💡 可以运行: make run-demo 开始使用")
    else:
        print("❌ 存在配置问题，请修复后重试")
        print("💡 运行 make setup-env 创建配置文件")
        print("💡 运行 make install 安装依赖")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
