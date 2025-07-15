# AutoGen编程工作流系统 Makefile

.PHONY: help install test run-basic run-advanced run-demo clean format lint

# 默认目标
help:
	@echo "AutoGen编程工作流系统"
	@echo "====================="
	@echo ""
	@echo "可用命令:"
	@echo "  setup-env    - 创建.env配置文件"
	@echo "  setup-gemini - 快速设置Gemini API"
	@echo "  install      - 安装依赖包"
	@echo "  test         - 运行测试"
	@echo "  test-gemini  - 测试Gemini API配置"
	@echo "  run-basic    - 运行基础工作流"
	@echo "  run-advanced - 运行高级工作流"
	@echo "  run-demo     - 运行演示模式"
	@echo "  example      - 运行使用示例"
	@echo "  format       - 格式化代码"
	@echo "  lint         - 代码检查"
	@echo "  clean        - 清理临时文件"
	@echo ""
	@echo "首次使用:"
	@echo "  OpenAI用户: make setup-env"
	@echo "  Gemini用户: make setup-gemini"

# 创建环境配置文件
setup-env:
	@echo "🔧 创建环境配置文件..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ .env文件已创建，请编辑并设置您的API密钥"; \
		echo "📝 请编辑.env文件中的OPENAI_API_KEY"; \
	else \
		echo "⚠️  .env文件已存在"; \
	fi

# 快速设置Gemini API
setup-gemini:
	@echo "🚀 快速设置Gemini API..."
	python setup_gemini.py

# 安装依赖
install:
	@echo "📦 安装依赖包..."
	pip install -r requirements.txt
	@echo "✅ 依赖安装完成"

# 运行测试
test:
	@echo "🧪 运行测试..."
	python test_workflow.py
	@echo "✅ 测试完成"

# 测试Gemini API配置
test-gemini:
	@echo "🧪 测试Gemini API配置..."
	python test_gemini_config.py

# 运行基础工作流
run-basic:
	@echo "🔥 启动基础编程工作流..."
	python run_workflow.py --mode basic

# 运行高级工作流
run-advanced:
	@echo "🚀 启动高级编程工作流..."
	python run_workflow.py --mode advanced

# 运行演示模式
run-demo:
	@echo "⚡ 启动演示模式..."
	python run_workflow.py --mode demo

# 运行使用示例
example:
	@echo "📚 运行使用示例..."
	python example_usage.py

# 代码格式化
format:
	@echo "🎨 格式化代码..."
	@if command -v black >/dev/null 2>&1; then \
		black *.py; \
	else \
		echo "⚠️  black未安装，跳过格式化"; \
	fi
	@if command -v isort >/dev/null 2>&1; then \
		isort *.py; \
	else \
		echo "⚠️  isort未安装，跳过导入排序"; \
	fi

# 代码检查
lint:
	@echo "🔍 代码检查..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 *.py --max-line-length=100 --ignore=E203,W503; \
	else \
		echo "⚠️  flake8未安装，跳过代码检查"; \
	fi

# 清理临时文件
clean:
	@echo "🧹 清理临时文件..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "✅ 清理完成"

# 检查环境
check-env:
	@echo "🔧 检查环境配置..."
	@if [ ! -f .env ]; then \
		echo "❌ .env文件不存在"; \
		echo "请运行: make setup-env"; \
		exit 1; \
	fi
	@python -c "from env_config import get_config; config = get_config(); errors = config.validate_config(); print('✅ 配置验证通过') if not errors else [print(f'❌ {error}') for error in errors] or exit(1)"
	@python -c "import sys; print(f'Python版本: {sys.version}')"

# 安装开发依赖
install-dev:
	@echo "📦 安装开发依赖..."
	pip install black isort flake8 pytest pytest-asyncio
	@echo "✅ 开发依赖安装完成"

# 完整设置
setup: setup-env install install-dev
	@echo "🚀 完整环境设置完成"
	@echo "请编辑.env文件设置您的API密钥"

# 运行所有检查
check-all: check-env lint test
	@echo "✅ 所有检查通过"
