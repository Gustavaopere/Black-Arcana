# Tunneling

- Provider: **Mowzie's Mobs** (`mowziesmobs`)
- Version: `1.8.2`
- Provider ability id: `tunneling`
- Classificação: **Geomancy player power**
- Provider surface: Earthrend Gauntlet
- State: `CONDITIONAL`

## Identidade semântica

Ação Geomancy registrada no `PLAYER_ABILITIES` exato. Sua identidade existe no artefato atual, mas a disponibilidade implantada é controlada por configuração provider-native.

## Reachability

O exact `TunnelingAbility.canUse()` lê `ConfigHandler$EarthrendGauntlet.enableTunneling`. Somente o valor efetivo implantado pode decidir strict vs deployed-disabled; source/default não é substituto.

## Evidence boundary

A ficha registra somente identidade, causalidade, deduplicação e reachability já sustentadas pelo catálogo canônico. Fórmulas, dano, duração, cooldown/durabilidade, animação, networking e demais detalhes finos não são inferidos.

Source: `../PLAYER-MAGIC-INVENTORY.md`.
