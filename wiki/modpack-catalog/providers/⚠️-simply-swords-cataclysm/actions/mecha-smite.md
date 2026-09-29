# Mecha Smite

- Provider: **Simply Swords: Cataclysm** (`simplycataclysm`)
- Physical line: `1.0.2+1.21.1+neoforge`
- Material owner: **Witherite**
- Classificação: **supernatural weapon ability / hit-triggered multi-branch proc**
- Source surface: `WitheriteSwordItem`
- State: `SOURCE-PINNED IDENTITY / DEPLOYED STARTUP CONDITIONAL`

## Identidade semântica

Raiz provider-owned única com branches harmful e regenerative. Wither, fire e self-regeneration são resultados internos de Mecha Smite; não são três ações independentes.

A ficha preserva uma identidade causal mesmo quando uma branch específica estiver desabilitada pelo STARTUP config.

## Reachability

A classificação implantada exige os valores efetivos:

- `mechaSmiteHarmfulEffectsChance`;
- `mechaSmiteFireDuration`;
- `mechaSmiteWitherDuration`;
- `mechaSmiteRegenChance`;
- `mechaSmiteRegenUsesPercentage`;
- `mechaSmiteRegenPercentage`;
- `mechaSmiteRegenThreshold`.

A branch harmful requer chance não-zero e pelo menos uma duração harmful não-zero. A branch regenerative é classificada separadamente pela chance e pelo modo/valor de threshold selecionado. A identidade só pode ser promovida ao strict quando o estado implantado tornar ao menos uma causalidade provider-native efetivamente alcançável.

Defaults do source não substituem esses valores.

## Evidence boundary

A identidade única e a topologia de gates estão fechadas. Fórmulas, amplificadores, duração efetiva, chance e thresholds implantados permanecem não verificados até coleta autoritativa.

Source: `../SOURCE-1.0.2-ABILITY-INVENTORY.md`.
