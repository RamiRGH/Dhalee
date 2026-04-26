import json
import logging
import re
from openai import AsyncOpenAI
from app.config import get_settings

logger = logging.getLogger("dhalee.llm")

MAX_OUTPUT_TOKENS = 4096
MAX_TOTAL_CHARS_PER_CALL = 12000


def _truncate_prompt(system_prompt: str, user_prompt: str) -> tuple[str, str]:
    total = len(system_prompt) + len(user_prompt)
    if total <= MAX_TOTAL_CHARS_PER_CALL:
        return system_prompt, user_prompt

    allowed_user = max(0, MAX_TOTAL_CHARS_PER_CALL - len(system_prompt))
    truncated = user_prompt[:allowed_user]
    logger.warning(
        "Prompt truncated | original_user=%d allowed_user=%d",
        len(user_prompt),
        allowed_user,
    )
    return system_prompt, truncated


async def llm_chat(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    settings = get_settings()
    client = AsyncOpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    system_prompt, user_prompt = _truncate_prompt(system_prompt, user_prompt)

    logger.info(
        "LLM chat request | model=%s | temp=%s | sys_len=%d | user_len=%d | max_output=%d",
        settings.openai_model,
        temperature,
        len(system_prompt),
        len(user_prompt),
        MAX_OUTPUT_TOKENS,
    )

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_completion_tokens=MAX_OUTPUT_TOKENS,
        )
    except Exception as e:
        logger.exception("LLM chat request failed")
        raise

    choice = response.choices[0]
    content = choice.message.content or ""
    finish_reason = choice.finish_reason

    logger.info(
        "LLM chat response | content_len=%d | finish_reason=%s | raw_preview=%s",
        len(content),
        finish_reason,
        content[:200].replace("\n", " "),
    )

    if finish_reason == "length":
        raise RuntimeError(
            f"The model ({settings.openai_model}) hit its output token limit (max_completion_tokens={MAX_OUTPUT_TOKENS}) "
            "and returned empty or incomplete content.\n\n"
            "This usually means the model does not have enough output capacity for the task.\n"
            "Try a model with a larger context/output window, or reduce the prompt length."
        )

    return content


def _extract_json(text: str) -> dict:
    logger.debug("Extracting JSON from text (len=%d)", len(text))

    if not text or not text.strip():
        logger.error("Cannot extract JSON: LLM returned empty/whitespace-only content")
        raise ValueError("LLM returned empty content — cannot parse JSON.")

    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        candidate = match.group(1).strip()
        logger.debug("Found markdown code block, candidate len=%d", len(candidate))
    else:
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            candidate = match.group(1).strip()
            logger.debug("Found raw JSON block, candidate len=%d", len(candidate))
        else:
            candidate = text.strip()
            logger.debug("No JSON block pattern matched, using stripped full text len=%d", len(candidate))

    try:
        parsed = json.loads(candidate)
        logger.debug("JSON parsed successfully | keys=%s", list(parsed.keys()) if isinstance(parsed, dict) else type(parsed))
        return parsed
    except json.JSONDecodeError as e:
        logger.error(
            "JSON decode failed | error=%s | raw_preview=%s | candidate_preview=%s",
            e,
            text[:500].replace("\n", " "),
            candidate[:500].replace("\n", " "),
        )
        raise ValueError(f"JSON decode failed: {e}. Raw preview: {text[:300]}")


async def llm_json(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> dict:
    content = await llm_chat(system_prompt, user_prompt, temperature)
    return _extract_json(content)
