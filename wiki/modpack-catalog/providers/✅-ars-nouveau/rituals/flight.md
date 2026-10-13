# Flight

Status: `SOURCE-PINNED 5.13.1 / RANGE-EFFECT RITUAL`

- Registry id: `ars_nouveau:ritual_flight`
- Class: `RitualFlight`
- Effect: provider `FLIGHT_EFFECT`
- Effect duration per application: `60 × 20 = 1200 ticks`
- Range: `60` blocks
- Source cost declaration: `200`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native lifecycle

`RitualFlight` extends Ars Nouveau's `RangeEffectRitual`. A player is eligible only server-side, within range, and while the ritual is not already waiting for Source. When `attemptRefresh` successfully applies the effect, the ritual marks itself as needing Source.

The ritual also exposes a jump-event path: when a `ServerPlayer` jumps without the Flight effect, it attempts to refresh/apply the ritual effect. Successful application synchronizes the player's prior flight state through `PacketUpdateFlight`.

## Authority / Black Arcana boundary

Flight capability, effect refresh and Source debit are Ars Nouveau authority. Black Arcana must not grant a second flight state, consume another resource or convert every jump into a new cast/mastery event.

This provider capability is distinct from Black Arcana mobility spells and from external glider/stamina systems; integration requires a real semantic boundary rather than presentation matching.

## QA

Source lifecycle is pinned to 5.13.1. Interaction with other flight providers, ability modifiers and full-pack movement systems remains runtime QA.

## Localizadores e parâmetros para Codex — fonte exata

- **Java:** [`RitualFlight.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualFlight.java) no commit `112920ff774831f204031da75b4c4e73d3765157` correspondente ao catálogo Ars 5.13.1.
- **Implementação:** `RitualFlight extends RangeEffectRitual`; `getEffect=FLIGHT_EFFECT`, `getDuration=1200 ticks`, `getRange=60 blocks`, `getSourceCost=200` no código-fonte desta versão.
- **Ativação e refresh:** `applyEffect(ServerPlayer)` salva estado `wasFlying`, chama `super.applyEffect(player,false)` e sincroniza `PacketUpdateFlight` só no sucesso. `onJumpEvent` tenta `attemptRefresh` somente para player sem efeito.
- **Perk de ritual:** alcance, duração, custo, recarga e elegibilidade são knobs conceitualmente separados; ampliar buff sem manter contrato de `RangeEffectRitual` e custo Source seria bypass.
- **Mastery:** evento de pulo não é automaticamente uma conclusão de ritual. Atribuir XP somente a uma ação canônica comprovada; nenhuma bridge nova foi implementada.

**Estado:** prova estática de parâmetros por leitura de código; habilidade de mutação por hook externo não verificada. Ars controla composição, execução, mana/Source e configurações; RPG Skill Tree controla perks/Mastery/gates; Black Arcana é autoridade somente de seu runtime próprio. [Padrão universal](../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
