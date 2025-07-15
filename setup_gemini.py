#!/usr/bin/env python3
"""
Gemini API快速设置脚本
帮助用户快速配置Gemini API
"""

import os
import sys
import shutil


def print_banner():
    """打印横幅"""
    print("🚀 AutoGen编程工作流 - Gemini API设置")
    print("=" * 60)


def check_env_example():
    """检查.env.example文件"""
    if not os.path.exists(".env.example"):
        print("❌ .env.example文件不存在")
        return False
    return True


def create_env_file():
    """创建.env文件"""
    if os.path.exists(".env"):
        response = input("⚠️  .env文件已存在，是否覆盖？(y/N): ").strip().lower()
        if response != 'y':
            print("取消操作")
            return False
    
    try:
        shutil.copy(".env.example", ".env")
        print("✅ .env文件创建成功")
        return True
    except Exception as e:
        print(f"❌ 创建.env文件失败: {e}")
        return False


def get_gemini_api_key():
    """获取Gemini API密钥"""
    print("\n📖 获取Gemini API密钥:")
    print("1. 访问: https://makersuite.google.com/app/apikey")
    print("2. 使用Google账户登录")
    print("3. 点击'Create API Key'")
    print("4. 复制生成的API密钥")
    print("")
    
    while True:
        api_key = input("请输入您的Gemini API密钥: ").strip()
        if api_key:
            if api_key.startswith("AIza"):
                return api_key
            else:
                print("⚠️  Gemini API密钥通常以'AIza'开头，请检查是否正确")
                response = input("是否继续使用此密钥？(y/N): ").strip().lower()
                if response == 'y':
                    return api_key
        else:
            print("❌ API密钥不能为空")


def update_env_file(api_key):
    """更新.env文件"""
    try:
        # 读取.env文件
        with open(".env", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 更新配置
        lines = content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.startswith("API_PROVIDER="):
                updated_lines.append("API_PROVIDER=gemini")
            elif line.startswith("GEMINI_API_KEY="):
                updated_lines.append(f"GEMINI_API_KEY={api_key}")
            elif line.startswith("DEFAULT_MODEL="):
                updated_lines.append("DEFAULT_MODEL=gemini-pro")
            elif line.startswith("# GEMINI_API_KEY="):
                updated_lines.append(f"GEMINI_API_KEY={api_key}")
            else:
                updated_lines.append(line)
        
        # 写回文件
        with open(".env", "w", encoding="utf-8") as f:
            f.write('\n'.join(updated_lines))
        
        print("✅ .env文件更新成功")
        return True
        
    except Exception as e:
        print(f"❌ 更新.env文件失败: {e}")
        return False


def show_configuration():
    """显示当前配置"""
    print("\n📋 当前配置:")
    print("-" * 30)
    
    try:
        with open(".env", "r", encoding="utf-8") as f:
            content = f.read()
        
        for line in content.split('\n'):
            if line.startswith("API_PROVIDER="):
                print(f"API提供商: {line.split('=', 1)[1]}")
            elif line.startswith("GEMINI_API_KEY="):
                key = line.split('=', 1)[1]
                if key:
                    print(f"Gemini API密钥: {key[:20]}...")
                else:
                    print("Gemini API密钥: 未设置")
            elif line.startswith("DEFAULT_MODEL="):
                print(f"默认模型: {line.split('=', 1)[1]}")
    
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")


def test_configuration():
    """测试配置"""
    print("\n🧪 测试配置...")
    
    try:
        # 尝试导入并测试
        import subprocess
        result = subprocess.run([
            sys.executable, "test_gemini_config.py"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ 配置测试通过")
            return True
        else:
            print("❌ 配置测试失败")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ 测试超时")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def show_next_steps():
    """显示后续步骤"""
    print("\n🎯 后续步骤:")
    print("1. 安装依赖: make install")
    print("2. 测试配置: make test-gemini")
    print("3. 运行演示: make run-demo")
    print("4. 查看文档: cat README.md")


def main():
    """主函数"""
    print_banner()
    
    # 检查.env.example文件
    if not check_env_example():
        print("请确保在项目根目录运行此脚本")
        sys.exit(1)
    
    # 创建.env文件
    if not create_env_file():
        sys.exit(1)
    
    # 获取API密钥
    api_key = get_gemini_api_key()
    
    # 更新.env文件
    if not update_env_file(api_key):
        sys.exit(1)
    
    # 显示配置
    show_configuration()
    
    # 询问是否测试配置
    print("\n" + "=" * 60)
    response = input("是否现在测试配置？(Y/n): ").strip().lower()
    
    if response != 'n':
        if test_configuration():
            print("\n🎉 Gemini API配置完成！")
        else:
            print("\n⚠️  配置可能有问题，请检查API密钥")
    
    show_next_steps()
    
    print("\n" + "=" * 60)
    print("✅ 设置完成！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  设置被用户中断")
    except Exception as e:
        print(f"\n❌ 设置出错: {e}")
        sys.exit(1)
