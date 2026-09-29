# Blazing Brand

- Provider: **Simply Swords: Cataclysm** (`simplycataclysm`)
- Physical line: `1.0.2+1.21.1+neoforge`
- Material owner: **Ignitium**
- Classificação: **supernatural weapon ability / hit-triggered**
- Source surface: `IgnitiumSwordItem`
- State: `SOURCE-PINNED IDENTITY / DEPLOYED STARTUP CONDITIONAL`

## Identidade semântica

Raiz provider-owned de combate associada à família Ignitium. O source pin exato fecha uma única identidade Blazing Brand; stacking de brand, redução defensiva e lifesteal pertencem ao mesmo fluxo causal e não são contados como ações separadas.

Status effects, partículas, sons e settlement de dano/cura são consequências downstream da mesma raiz.

## Reachability

A ativação atual depende do valor efetivo de `blazingBrandChance` no STARTUP config implantado.

- `0` => trait desabilitado;
- valor não-zero => candidato ativo, sujeito ao restante da validação provider-native.

O default do source não substitui o valor implantado.

## Evidence boundary

A existência da identidade, owner e gate são source-pinned. Chance efetiva, fórmulas, stacks, valores defensivos, dano e lifesteal não são inferidos nesta ficha.

Source: `../SOURCE-1.0.2-ABILITY-INVENTORY.md`.
