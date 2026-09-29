# Mecha Pulse

- Provider: **Simply Swords: Cataclysm** (`simplycataclysm`)
- Physical line: `1.0.2+1.21.1+neoforge`
- Material owner: **Witherite**
- Classificação: **supernatural weapon ability / charge-state combat proc**
- Source surface: `WitheriteSwordItem`
- State: `SOURCE-PINNED IDENTITY / DEPLOYED STARTUP CONDITIONAL`

## Identidade semântica

Raiz provider-owned de combate que usa uma state machine de charge → threshold → resolução → cooldown. Shockwave, stun, dano adicional, `pulse_charge` e `pulse_cooldown` são fases/efeitos da mesma habilidade e adicionam +0 identidades.

## Reachability

A progressão normal da ação depende do valor efetivo de `mechaPulseChargeChance` no STARTUP config implantado.

- `0` => sem progressão normal de charge;
- valor não-zero => candidato ativo, sujeito ao restante da validação provider-native.

O default do source não substitui o valor implantado.

## Evidence boundary

A identidade, owner, state-machine class e gate estão fechados. Thresholds, dano, stun, cooldown e probabilidades efetivas não são inferidos.

Source: `../SOURCE-1.0.2-ABILITY-INVENTORY.md`.
