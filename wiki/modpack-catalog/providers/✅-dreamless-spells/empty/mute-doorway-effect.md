# Mute / Doorway Effect

**Status do registro:** ✅ `COUNTED_EXACT` para ID estático no JAR físico — [evidência](../EXACT-BINARY-SPELLS-1.1.9.md) ([run #38302406303](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38302406303)). As fórmulas, efeitos, gate, custos e duração abaixo continuam source-pinned, sem QA física de execução/Survival.

- ID runtime: `dreamless_spells:doorway_effect`
- classe: `MuteSpell`
- escola: Empty (`dreamless_spells:empty`)
- rarity: Legendary
- níveis: 1–5
- cast: LONG
- cast time base: 60 ticks = 3 s
- mana: 0
- cooldown: 10 s
- target range: 32
- target-area visual: raio 3
- neutral spell power: 5 / 10 / 15 / 20 / 25

## Gate

Exige `dreamless_spells:emptied` no caster antes do cast.

## Descrição provider

O guide de `doorway_effect` diz que o alvo esquece por um instante o que iria lançar. O changelog de 1.1.8 registra que “Doorway effect changed to mute”.

## Efeito

A spell aplica `dreamless_spells:mute` ao LivingEntity alvo.

O settlement real do bloqueio ocorre em `ServerEvents#onPlayerCastEvent`, subscriber de `SpellPreCastEvent`:

1. se a entidade que tenta castar é `ServerPlayer`;
2. e possui Mute;
3. o evento é cancelado;
4. o player recebe `I can't seem to cast this` e um som de fire extinguish.

Assim, enquanto Mute estiver ativo, o handler bloqueia casts independentemente da escola/spell.

O handler só executa o cancelamento para `ServerPlayer`; um mob/non-player caster com o MobEffect não é bloqueado por esse código.

## Divergência crítica de duração

Tooltip (`getUniqueInfo`):

`spellPower × 5 ticks`

Neutralmente:

- nível 1: 25 ticks = 1.25 s;
- nível 2: 50 = 2.5 s;
- nível 3: 75 = 3.75 s;
- nível 4: 100 = 5 s;
- nível 5: 125 = 6.25 s.

Settlement:

`(int)(spellPower × 0.1)`

Neutralmente:

- nível 1: 0 tick;
- nível 2: 1 tick;
- nível 3: 1 tick;
- nível 4: 2 ticks;
- nível 5: 2 ticks.

O comportamento esperado pelo guide e o comportamento estático do source divergem fortemente.

## Registry/lang mismatch

O `ResourceLocation` é `dreamless_spells:doorway_effect`, então Iron's deriva o component name `spell.dreamless_spells.doorway_effect`.

O lang 1.1.9 possui `spell.dreamless_spells.mute = Mute`, mas não a chave de nome `spell.dreamless_spells.doorway_effect`. Existe apenas `spell.dreamless_spells.doorway_effect.guide`.

Resultado player-facing: **QA obrigatório**; não renomear o ID runtime.

## Obtenção

Crafting permitido por default e escola Empty lootável por default. Empty Gem é focus. Cast em survival depende de `Emptied` e, portanto, da progressão Empty documentada em `PROGRESSION.md`.

## Authority / exactly-once

Authority de status = `DSSEffects.MUTE_EFFECT`.

Authority de bloqueio = cancellation do `SpellPreCastEvent` no `ServerEvents` do provider.

Black Arcana não deve cancelar o mesmo cast novamente, nem aplicar um segundo silêncio. Para perks/progressão, observar cast falho/sucesso em uma camada que não altere settlement.

## QA

- nome exibido da spell;
- duração exata níveis 1–5;
- cancelamento de spells de todas as escolas;
- comportamento em mobs caster;
- se 0-tick no nível 1 produz qualquer janela de cancelamento;
- interação com Counterspell e outros sistemas de cancelamento.

## Atualização de ABI exata 1.1.9 — 27/10/2026

A [auditoria do JAR físico dreamless_spells-1.1.9.jar](../EXACT-1.1.9-SPELL-CAST-AND-COUNTERSPELL-ABI-20261027.md) (SHA-1 `d51960bfb8af1aafa5d716ef9a48c3135f36b956`, run [#40499150605](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40499150605)) confirmou estas relações de código **sem importar corpos de método**:

O classfile `MuteSpell` confirma `onCast` referenciando `getDuration`, `getAmplifier`, `DSSEffects.MUTE_EFFECT` e `LivingEntity.addEffect`; `checkPreCastConditions` referencia `DSSEffects.EMPTIED_EFFECT`. O método binário `ServerEvents.onPlayerCastEvent` referencia `DSSEffects.MUTE_EFFECT` e `SpellPreCastEvent.setCanceled`. Isso **não** demonstra que todo cast seja cancelado ou que o cast já negado tenha sido cobrado; condição de player, duração, ordem e feedback aguardam teste.

**Status:** `EXACT_BINARY_METHOD_REFERENCES` (estático) · `SOURCE_ALIGNED_NUMBERS_NOT_BINARY_PROVEN` · `physical_qa=NOT_TESTED` · `mutating_hook=NOT_VERIFIED`. Nenhum registro novo, certificação de perk, custo adicional ou segundo pipeline Black Arcana. O provider permanece autoridade do efeito, e Iron's da transação de casting.
