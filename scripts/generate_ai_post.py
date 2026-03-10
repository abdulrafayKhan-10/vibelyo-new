#!/usr/bin/env python3
"""
Automated AI draft generator for Vibelyo Hugo content.

Features:
- Provider fallback (DeepSeek -> Qwen -> Ollama)
- Safe by default (draft=true)
- Basic SEO quality gates
- CI-friendly CLI for GitHub Actions
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests


CONFIG_FILE = Path(__file__).parent / "config.json"
CONTENT_DIR = Path(__file__).parent.parent / "content"


@dataclass
class ProviderResult:
    provider: str
    model: str
    content: str


class AIProviderError(RuntimeError):
    pass


class OllamaProvider:
    def __init__(self, api_url: str, model: str, temperature: float, top_p: float):
        self.api_url = api_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.top_p = top_p

    def generate(self, prompt: str, max_tokens: int = 2400) -> ProviderResult:
        url = f"{self.api_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "num_predict": max_tokens,
            },
        }
        try:
            response = requests.post(url, json=payload, timeout=180)
            response.raise_for_status()
            text = response.json().get("response", "").strip()
            if not text:
                raise AIProviderError("Ollama returned empty response")
            return ProviderResult(provider="ollama", model=self.model, content=text)
        except requests.RequestException as exc:
            raise AIProviderError(f"Ollama request failed: {exc}") from exc


class OpenAICompatibleProvider:
    def __init__(
        self,
        name: str,
        base_url: str,
        model: str,
        api_key_env: str,
        temperature: float,
        top_p: float,
    ):
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key_env = api_key_env
        self.temperature = temperature
        self.top_p = top_p

    def generate(self, prompt: str, max_tokens: int = 2400) -> ProviderResult:
        api_key = os.getenv(self.api_key_env, "").strip()
        if not api_key:
            raise AIProviderError(f"Missing environment variable: {self.api_key_env}")

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You write practical, factual, beginner-friendly blog posts."},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=180)
            response.raise_for_status()
            body = response.json()
            choices = body.get("choices", [])
            if not choices:
                raise AIProviderError(f"{self.name} returned no choices")
            text = choices[0].get("message", {}).get("content", "").strip()
            if not text:
                raise AIProviderError(f"{self.name} returned empty content")
            return ProviderResult(provider=self.name, model=self.model, content=text)
        except requests.RequestException as exc:
            raise AIProviderError(f"{self.name} request failed: {exc}") from exc


class Generator:
    def __init__(self, config: Dict):
        self.config = config
        self.categories = set(config.get("categories", []))

    def ensure_enabled(self, allow_disabled: bool = False) -> None:
        if allow_disabled:
            return
        if not self.config.get("enabled", False):
            raise RuntimeError(
                "Generation is disabled. Set scripts/config.json -> enabled: true before running."
            )

    def validate_category(self, category: str) -> None:
        if category not in self.categories:
            valid = ", ".join(sorted(self.categories))
            raise RuntimeError(f"Invalid category '{category}'. Valid categories: {valid}")

    def build_prompt(self, topic: str, category: str, keywords: str) -> str:
        min_words = self.config.get("min_words", 1200)
        max_words = self.config.get("max_words", 2200)
        return f"""Write a beginner-friendly educational article for Vibelyo.site.

Topic: {topic}
Category: {category}
Target keywords: {keywords}

Hard requirements:
1. Length: {min_words}-{max_words} words
2. Use Markdown format
3. Start directly with an engaging introduction paragraph (no title)
4. Use H2 and H3 headings
5. Include practical steps and examples
6. Be realistic and avoid guaranteed earning claims
7. Add a short FAQ section near the end
8. End with a concise action-focused conclusion

Quality requirements:
- Clear language for beginners
- No fluff, no repeated paragraphs
- Factually careful tone
- Use bullet lists and numbered lists where useful
"""

    def create_frontmatter(
        self,
        title: str,
        description: str,
        category: str,
        tags: List[str],
        keywords: str,
        provider_info: ProviderResult,
    ) -> str:
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:00")
        tags_json = json.dumps(tags, ensure_ascii=True)
        safe_title = title.replace('"', "'")
        safe_desc = description.replace('"', "'")
        safe_keywords = keywords.replace('"', "'")

        return (
            "---\n"
            f"title: \"{safe_title}\"\n"
            f"description: \"{safe_desc}\"\n"
            f"date: {now}\n"
            "draft: true\n"
            f"categories: [\"{category}\"]\n"
            f"tags: {tags_json}\n"
            f"keywords: \"{safe_keywords}\"\n"
            "ai_assisted: true\n"
            f"ai_model: \"{provider_info.provider}/{provider_info.model}\"\n"
            "---\n\n"
        )

    @staticmethod
    def sanitize_filename(value: str) -> str:
        text = re.sub(r"[^a-zA-Z0-9\s-]", "", value.lower()).strip()
        text = re.sub(r"\s+", "-", text)
        text = re.sub(r"-+", "-", text)
        return f"{text[:100]}.md"

    @staticmethod
    def word_count(text: str) -> int:
        return len(re.findall(r"\b\w+\b", text))

    def quality_report(self, body: str, keywords: str) -> Dict:
        words = self.word_count(body)
        h2_count = len(re.findall(r"^##\s+", body, flags=re.MULTILINE))
        h3_count = len(re.findall(r"^###\s+", body, flags=re.MULTILINE))
        faq_present = bool(re.search(r"##\s+FAQ|##\s+Frequently Asked Questions", body, flags=re.IGNORECASE))

        keyword_tokens = [k.strip().lower() for k in keywords.split(",") if k.strip()]
        keyword_hits = sum(1 for kw in keyword_tokens if kw in body.lower())

        return {
            "word_count": words,
            "h2_count": h2_count,
            "h3_count": h3_count,
            "faq_present": faq_present,
            "keyword_tokens": keyword_tokens,
            "keyword_hits": keyword_hits,
            "passes_min_words": words >= int(self.config.get("min_words", 1200)),
            "passes_keywords": keyword_hits >= max(1, min(2, len(keyword_tokens))),
        }

    def pick_provider(self) -> List[str]:
        order = self.config.get("provider_fallback_order", ["ollama"])
        return [p for p in order if p]

    def run_provider(self, prompt: str) -> ProviderResult:
        providers_cfg = self.config.get("providers", {})
        errors: List[str] = []

        for name in self.pick_provider():
            try:
                if name == "ollama":
                    ollama_model = providers_cfg.get("ollama", {}).get("model", self.config.get("model", "llama3"))
                    provider = OllamaProvider(
                        api_url=self.config.get("ollama_api_url", "http://localhost:11434"),
                        model=ollama_model,
                        temperature=float(self.config.get("temperature", 0.7)),
                        top_p=float(self.config.get("top_p", 0.9)),
                    )
                    return provider.generate(prompt)

                provider_cfg = providers_cfg.get(name, {})
                provider = OpenAICompatibleProvider(
                    name=name,
                    base_url=provider_cfg.get("base_url", ""),
                    model=provider_cfg.get("model", ""),
                    api_key_env=provider_cfg.get("api_key_env", ""),
                    temperature=float(self.config.get("temperature", 0.7)),
                    top_p=float(self.config.get("top_p", 0.9)),
                )
                return provider.generate(prompt)
            except Exception as exc:
                errors.append(f"{name}: {exc}")

        raise RuntimeError("All providers failed: " + " | ".join(errors))

    def save_post(self, category: str, filename: str, markdown: str) -> Path:
        category_dir = CONTENT_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        file_path = category_dir / filename
        file_path.write_text(markdown, encoding="utf-8")
        return file_path


def load_config(path: Path) -> Dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Config file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON config: {exc}") from exc


def parse_tags(raw: str) -> List[str]:
    return [t.strip() for t in raw.split(",") if t.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AI-assisted Hugo draft post")
    parser.add_argument("--category", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--keywords", required=True, help="Comma-separated keywords")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--config", default=str(CONFIG_FILE))
    parser.add_argument("--allow-disabled", action="store_true", help="Allow generation even when config.enabled is false")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(Path(args.config))
    generator = Generator(config)

    generator.ensure_enabled(allow_disabled=args.allow_disabled)
    generator.validate_category(args.category)

    prompt = generator.build_prompt(topic=args.topic, category=args.category, keywords=args.keywords)
    provider_result = generator.run_provider(prompt)

    tags = parse_tags(args.tags) or parse_tags(args.keywords)
    frontmatter = generator.create_frontmatter(
        title=args.title,
        description=args.description,
        category=args.category,
        tags=tags,
        keywords=args.keywords,
        provider_info=provider_result,
    )

    quality = generator.quality_report(provider_result.content, args.keywords)
    filename = generator.sanitize_filename(args.title)
    markdown = frontmatter + provider_result.content.strip() + "\n"
    output_path = generator.save_post(args.category, filename, markdown)

    print(json.dumps({
        "output_file": str(output_path),
        "provider": provider_result.provider,
        "model": provider_result.model,
        "quality": quality,
    }, indent=2))

    if os.getenv("GITHUB_OUTPUT"):
        with open(os.getenv("GITHUB_OUTPUT"), "a", encoding="utf-8") as fp:
            fp.write(f"output_file={output_path.as_posix()}\n")
            fp.write(f"provider={provider_result.provider}\n")
            fp.write(f"model={provider_result.model}\n")
            fp.write(f"word_count={quality['word_count']}\n")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
