# OpenClaw memory search: OpenAI/Gemini APIs are optional

## Problem
Many users ask: "Do I need OpenAI or Gemini API keys for OpenClaw memory to work?"

## Short answer
No. OpenClaw memory itself works without OpenAI/Gemini.

What is optional is **semantic memory search** (`memory_search`).
That feature needs an embeddings provider (remote or local).

## What "memory" means in OpenClaw
OpenClaw memory is stored in Markdown files in your workspace, such as:
- `memory/YYYY-MM-DD.md`
- `MEMORY.md` (optional)

These files are the source of truth.

## When API keys are required
You need an API key only when using a **remote embeddings provider** (`openai`, `gemini`, or `voyage`) for memory search.

Also important: Codex OAuth for chat/completions does **not** automatically cover embeddings for memory search.

## Local/offline option
If you want no external embedding API, use local embeddings:

```json5
agents: {
  defaults: {
    memorySearch: {
      provider: "local",
      local: {
        modelPath: "hf:your-embedding-model.gguf"
      },
      fallback: "none"
    }
  }
}
```

## If `memorySearch.provider` is not set
OpenClaw auto-selects in this order:
1. `local` (if local model path is configured and available)
2. `openai` (if key is available)
3. `gemini` (if key is available)
4. `voyage` (if key is available)
5. otherwise semantic memory search stays disabled until configured

## Important nuance about `fallback = "none"`
`fallback = "none"` means "do not fall back to another provider."

By itself, it does **not** always mean "disable memory search entirely." Whether search works still depends on your selected provider and whether that provider is configured correctly.

## Optional related tool
If you want a chronological "what happened" timeline, see:
- [claw-history-skill](https://github.com/BlueBirdBack/claw-history-skill)

It complements memory files/search, but does **not** replace embedding-based semantic recall.

## References
- [OpenClaw docs: Memory](https://docs.openclaw.ai/concepts/memory)

## Credits
- **B3** — question framing and practical review direction
- **Rac** — merged and standardized write-up
