"""
Gemini API客户端适配器
将Gemini API适配为AutoGen兼容的接口
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any, Union
import json

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from autogen_core.models import ChatCompletionClient
from autogen_core.models._types import (
    ChatCompletionTokenLogprob,
    ChatCompletionTokenLogprobs,
    CreateResult,
    LLMMessage,
    SystemMessage,
    UserMessage,
    AssistantMessage,
    RequestUsage,
)


class GeminiChatCompletionClient(ChatCompletionClient):
    """Gemini API客户端，兼容AutoGen的ChatCompletionClient接口"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-pro",
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        timeout: int = 60,
        **kwargs
    ):
        """
        初始化Gemini客户端
        
        Args:
            api_key: Gemini API密钥
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大令牌数
            timeout: 超时时间
        """
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "google-generativeai包未安装。请运行: pip install google-generativeai"
            )
        
        self.api_key = api_key
        self.model_name = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        
        # 配置Gemini API
        genai.configure(api_key=api_key)
        
        # 创建模型实例
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        # 安全设置 - 允许所有内容以避免过度审查
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        self.model = genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _convert_messages_to_gemini_format(self, messages: List[LLMMessage]) -> str:
        """将AutoGen消息格式转换为Gemini格式"""
        conversation = []
        
        for message in messages:
            if isinstance(message, SystemMessage):
                # Gemini没有专门的系统消息，将其作为用户消息的前缀
                conversation.append(f"System: {message.content}")
            elif isinstance(message, UserMessage):
                conversation.append(f"User: {message.content}")
            elif isinstance(message, AssistantMessage):
                conversation.append(f"Assistant: {message.content}")
            else:
                # 其他类型的消息也作为用户消息处理
                conversation.append(f"User: {str(message.content)}")
        
        return "\n\n".join(conversation)
    
    async def create(
        self,
        messages: List[LLMMessage],
        *,
        cancellation_token: Optional[Any] = None,
        **kwargs
    ) -> CreateResult:
        """
        创建聊天完成
        
        Args:
            messages: 消息列表
            cancellation_token: 取消令牌
            **kwargs: 其他参数
            
        Returns:
            创建结果
        """
        try:
            # 转换消息格式
            prompt = self._convert_messages_to_gemini_format(messages)
            
            self.logger.debug(f"发送到Gemini的提示: {prompt[:200]}...")
            
            # 调用Gemini API
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            # 检查响应
            if not response.text:
                raise ValueError("Gemini API返回空响应")
            
            self.logger.debug(f"Gemini响应: {response.text[:200]}...")
            
            # 构造返回结果
            return CreateResult(
                content=response.text,
                finish_reason="stop",
                usage=RequestUsage(
                    prompt_tokens=0,  # Gemini API不提供详细的token计数
                    completion_tokens=0,
                    total_tokens=0
                ),
                cached=False,
                logprobs=None
            )
            
        except Exception as e:
            self.logger.error(f"Gemini API调用失败: {e}")
            raise RuntimeError(f"Gemini API调用失败: {e}")
    
    @property
    def capabilities(self) -> Dict[str, Any]:
        """返回客户端能力"""
        return {
            "vision": "gemini-pro-vision" in self.model_name,
            "function_calling": False,  # Gemini的函数调用支持有限
            "json_output": False,
            "streaming": False
        }
    
    def count_tokens(self, messages: List[LLMMessage]) -> int:
        """
        计算消息的令牌数（近似）
        
        Args:
            messages: 消息列表
            
        Returns:
            令牌数
        """
        # 简单的令牌计数估算
        text = self._convert_messages_to_gemini_format(messages)
        # 粗略估算：1个令牌约等于4个字符
        return len(text) // 4
    
    async def close(self):
        """关闭客户端连接"""
        # Gemini客户端不需要显式关闭
        self.logger.info("Gemini客户端已关闭")


def create_model_client(api_config):
    """
    根据API配置创建模型客户端
    
    Args:
        api_config: API配置对象
        
    Returns:
        模型客户端实例
    """
    if api_config.provider == "gemini":
        return GeminiChatCompletionClient(
            api_key=api_config.api_key,
            model=api_config.model,
            temperature=api_config.temperature,
            max_tokens=api_config.max_tokens,
            timeout=api_config.timeout
        )
    else:
        # 使用OpenAI客户端
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        return OpenAIChatCompletionClient(
            model=api_config.model,
            api_key=api_config.api_key,
            base_url=api_config.base_url,
            timeout=api_config.timeout
        )


# 兼容性函数
def get_model_client(config):
    """获取模型客户端（兼容旧代码）"""
    return create_model_client(config.api)
