# Agent Platform

Provider-agnostic orchestration for structured market reasoning. The default
provider is deterministic and offline; production LLM providers are injected
behind the `LLMProvider` protocol and cannot place live orders directly.
