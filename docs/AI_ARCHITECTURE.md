# AI architecture

Orchestration is a single workflow:

1. Safety scan (crisis, injection)
2. Agent routing (`select_agent`)
3. Context assembly from authorized results/goals
4. Provider complete
5. Persist messages + increment usage

Providers implement `complete(message, context, agent)`. Swap with `AI_PROVIDER=openai|anthropic|educational`.
