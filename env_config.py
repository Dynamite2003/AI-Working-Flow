"""
AutoGen编程工作流环境配置管理模块
支持从.env文件和环境变量加载配置
"""

import os
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path


def load_env_file(env_path: str = ".env") -> Dict[str, str]:
    """
    加载.env文件
    
    Args:
        env_path: .env文件路径
        
    Returns:
        配置字典
    """
    env_vars = {}
    
    if not os.path.exists(env_path):
        return env_vars
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                
                # 解析键值对
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # 移除引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    env_vars[key] = value
    
    except Exception as e:
        print(f"⚠️  加载.env文件失败: {e}")
    
    return env_vars


def get_env_value(key: str, default: Any = None, env_vars: Optional[Dict[str, str]] = None) -> Any:
    """
    获取环境变量值，支持类型转换
    
    Args:
        key: 环境变量键
        default: 默认值
        env_vars: 环境变量字典
        
    Returns:
        环境变量值
    """
    # 优先从系统环境变量获取
    value = os.getenv(key)
    
    # 如果系统环境变量没有，从.env文件获取
    if value is None and env_vars:
        value = env_vars.get(key)
    
    # 如果都没有，使用默认值
    if value is None:
        return default
    
    # 类型转换
    if isinstance(default, bool):
        return value.lower() in ('true', '1', 'yes', 'on')
    elif isinstance(default, int):
        try:
            return int(value)
        except ValueError:
            return default
    elif isinstance(default, float):
        try:
            return float(value)
        except ValueError:
            return default
    elif isinstance(default, list):
        return [item.strip() for item in value.split(',') if item.strip()]
    
    return value


@dataclass
class APIConfig:
    """API配置（支持OpenAI和Gemini）"""
    provider: str = "openai"  # openai, gemini
    api_key: str = ""
    base_url: Optional[str] = None
    org_id: Optional[str] = None  # 仅OpenAI使用
    model: str = "gpt-4o"
    temperature: float = 0.1
    max_tokens: Optional[int] = None
    timeout: int = 60


@dataclass
class WorkflowConfig:
    """工作流配置"""
    basic_max_messages: int = 15
    advanced_max_messages: int = 25
    enable_parallel_processing: bool = True
    enable_message_filtering: bool = True
    enable_security_analysis: bool = True
    enable_performance_optimization: bool = True
    security_check_level: str = "standard"
    performance_check_level: str = "standard"


@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"
    verbose: bool = False
    file_path: Optional[str] = None
    enable_color: bool = True


@dataclass
class ProjectConfig:
    """项目配置"""
    name: str = "AutoGen Programming Workflow"
    version: str = "1.0.0"
    default_language: str = "python"
    results_dir: str = "results"
    debug_mode: bool = False
    save_intermediate_results: bool = False


@dataclass
class CacheConfig:
    """缓存配置"""
    enable_cache: bool = False
    expiry_hours: int = 24


@dataclass
class ProxyConfig:
    """代理配置"""
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None


class EnvironmentConfig:
    """环境配置管理器"""
    
    def __init__(self, env_file: str = ".env"):
        """
        初始化环境配置
        
        Args:
            env_file: .env文件路径
        """
        self.env_file = env_file
        self.env_vars = load_env_file(env_file)
        
        # 加载各个配置模块
        self.api = self._load_api_config()
        self.workflow = self._load_workflow_config()
        self.logging = self._load_logging_config()
        self.project = self._load_project_config()
        self.cache = self._load_cache_config()
        self.proxy = self._load_proxy_config()
        
        # 设置日志
        self._setup_logging()
        
        # 创建必要的目录
        self._create_directories()
    
    def _load_api_config(self) -> APIConfig:
        """加载API配置（支持OpenAI和Gemini）"""
        provider = get_env_value("API_PROVIDER", "openai", self.env_vars).lower()

        # 根据提供商获取API密钥
        if provider == "gemini":
            api_key = get_env_value("GEMINI_API_KEY", env_vars=self.env_vars)
            default_model = "gemini-pro"
            base_url = get_env_value("GEMINI_BASE_URL", env_vars=self.env_vars)
        else:  # openai
            api_key = get_env_value("OPENAI_API_KEY", env_vars=self.env_vars)
            default_model = "gpt-4o"
            base_url = get_env_value("OPENAI_BASE_URL", env_vars=self.env_vars)

        if not api_key:
            if provider == "gemini":
                raise ValueError("GEMINI_API_KEY未设置，请在.env文件或环境变量中设置")
            else:
                raise ValueError("OPENAI_API_KEY未设置，请在.env文件或环境变量中设置")

        return APIConfig(
            provider=provider,
            api_key=api_key,
            base_url=base_url,
            org_id=get_env_value("OPENAI_ORG_ID", env_vars=self.env_vars) if provider == "openai" else None,
            model=get_env_value("DEFAULT_MODEL", default_model, self.env_vars),
            temperature=get_env_value("MODEL_TEMPERATURE", 0.1, self.env_vars),
            max_tokens=get_env_value("MAX_TOKENS", env_vars=self.env_vars),
            timeout=get_env_value("REQUEST_TIMEOUT", 60, self.env_vars)
        )
    
    def _load_workflow_config(self) -> WorkflowConfig:
        """加载工作流配置"""
        return WorkflowConfig(
            basic_max_messages=get_env_value("BASIC_WORKFLOW_MAX_MESSAGES", 15, self.env_vars),
            advanced_max_messages=get_env_value("ADVANCED_WORKFLOW_MAX_MESSAGES", 25, self.env_vars),
            enable_parallel_processing=get_env_value("ENABLE_PARALLEL_PROCESSING", True, self.env_vars),
            enable_message_filtering=get_env_value("ENABLE_MESSAGE_FILTERING", True, self.env_vars),
            enable_security_analysis=get_env_value("ENABLE_SECURITY_ANALYSIS", True, self.env_vars),
            enable_performance_optimization=get_env_value("ENABLE_PERFORMANCE_OPTIMIZATION", True, self.env_vars),
            security_check_level=get_env_value("SECURITY_CHECK_LEVEL", "standard", self.env_vars),
            performance_check_level=get_env_value("PERFORMANCE_CHECK_LEVEL", "standard", self.env_vars)
        )
    
    def _load_logging_config(self) -> LoggingConfig:
        """加载日志配置"""
        return LoggingConfig(
            level=get_env_value("LOG_LEVEL", "INFO", self.env_vars),
            verbose=get_env_value("VERBOSE_LOGGING", False, self.env_vars),
            file_path=get_env_value("LOG_FILE", env_vars=self.env_vars),
            enable_color=get_env_value("ENABLE_COLOR_OUTPUT", True, self.env_vars)
        )
    
    def _load_project_config(self) -> ProjectConfig:
        """加载项目配置"""
        return ProjectConfig(
            name=get_env_value("PROJECT_NAME", "AutoGen Programming Workflow", self.env_vars),
            version=get_env_value("PROJECT_VERSION", "1.0.0", self.env_vars),
            default_language=get_env_value("DEFAULT_LANGUAGE", "python", self.env_vars),
            results_dir=get_env_value("RESULTS_DIR", "results", self.env_vars),
            debug_mode=get_env_value("DEBUG_MODE", False, self.env_vars),
            save_intermediate_results=get_env_value("SAVE_INTERMEDIATE_RESULTS", False, self.env_vars)
        )
    
    def _load_cache_config(self) -> CacheConfig:
        """加载缓存配置"""
        return CacheConfig(
            enable_cache=get_env_value("ENABLE_RESPONSE_CACHE", False, self.env_vars),
            expiry_hours=get_env_value("CACHE_EXPIRY_HOURS", 24, self.env_vars)
        )
    
    def _load_proxy_config(self) -> ProxyConfig:
        """加载代理配置"""
        return ProxyConfig(
            http_proxy=get_env_value("HTTP_PROXY", env_vars=self.env_vars),
            https_proxy=get_env_value("HTTPS_PROXY", env_vars=self.env_vars)
        )
    
    def _setup_logging(self):
        """设置日志"""
        level = getattr(logging, self.logging.level.upper(), logging.INFO)
        
        # 配置日志格式
        if self.logging.enable_color:
            format_str = "%(asctime)s - \033[1;36m%(name)s\033[0m - \033[1;%(levelcolor)sm%(levelname)s\033[0m - %(message)s"
        else:
            format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # 配置处理器
        handlers = [logging.StreamHandler()]
        
        if self.logging.file_path:
            # 确保日志目录存在
            log_dir = os.path.dirname(self.logging.file_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            handlers.append(logging.FileHandler(self.logging.file_path))
        
        # 配置根日志器
        logging.basicConfig(
            level=level,
            format=format_str,
            handlers=handlers,
            force=True
        )
        
        # 设置详细模式
        if self.logging.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
    
    def _create_directories(self):
        """创建必要的目录"""
        directories = [self.project.results_dir]
        
        if self.logging.file_path:
            log_dir = os.path.dirname(self.logging.file_path)
            if log_dir:
                directories.append(log_dir)
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def validate_config(self) -> List[str]:
        """
        验证配置
        
        Returns:
            错误信息列表
        """
        errors = []
        
        # 验证API配置
        if not self.api.api_key:
            if self.api.provider == "gemini":
                errors.append("GEMINI_API_KEY未设置")
            else:
                errors.append("OPENAI_API_KEY未设置")

        if self.api.temperature < 0 or self.api.temperature > 2:
            errors.append("MODEL_TEMPERATURE必须在0-2之间")
        
        # 验证工作流配置
        if self.workflow.basic_max_messages <= 0:
            errors.append("BASIC_WORKFLOW_MAX_MESSAGES必须大于0")
        
        if self.workflow.advanced_max_messages <= 0:
            errors.append("ADVANCED_WORKFLOW_MAX_MESSAGES必须大于0")
        
        # 验证日志级别
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.logging.level.upper() not in valid_levels:
            errors.append(f"LOG_LEVEL必须是以下之一: {', '.join(valid_levels)}")
        
        return errors
    
    def print_config_summary(self):
        """打印配置摘要"""
        print(f"🔧 {self.project.name} v{self.project.version}")
        print("=" * 50)
        print(f"API提供商: {self.api.provider}")
        print(f"模型: {self.api.model}")
        print(f"温度: {self.api.temperature}")
        print(f"默认语言: {self.project.default_language}")
        print(f"日志级别: {self.logging.level}")
        print(f"并行处理: {'启用' if self.workflow.enable_parallel_processing else '禁用'}")
        print(f"安全分析: {'启用' if self.workflow.enable_security_analysis else '禁用'}")
        print(f"性能优化: {'启用' if self.workflow.enable_performance_optimization else '禁用'}")
        print("=" * 50)


# 全局配置实例
config = None


def get_config(env_file: str = ".env") -> EnvironmentConfig:
    """
    获取全局配置实例
    
    Args:
        env_file: .env文件路径
        
    Returns:
        配置实例
    """
    global config
    if config is None:
        config = EnvironmentConfig(env_file)
    return config


def reload_config(env_file: str = ".env") -> EnvironmentConfig:
    """
    重新加载配置
    
    Args:
        env_file: .env文件路径
        
    Returns:
        新的配置实例
    """
    global config
    config = EnvironmentConfig(env_file)
    return config
