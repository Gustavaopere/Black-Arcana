# Wind Charge

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:wind_charge` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:wind_charge`
- Registered class: `WindChargeSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new WindChargeSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Evidence boundary

Estado documental: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:wind_charge` — Wind Charge.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

Os pares **base/per-level** abaixo são campos literais entregues a `AbstractSpell`; não significam `base + per-level×level`. Avaliação de nível, atributos/config e custo/cooldown efetivo pertencem ao host.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast e custos | INSTANT, nível 1–5, cooldown default 1 s; castTime=0, mana base/per-level **20/8**; power base/per-level **10/3** (antes dos multiplicadores do caster). | Iron's authority; não instituir custo duplicado. |
| Spawn/direção | Cria um MagicWindCharge por cast em Y do olho menos metade da altura da hitbox; owner caster, direção getLookAngle, velocidade base 1.5 (getSpeed), isNoGravity=true. | Quantidade/velocity/hitbox per-caster ⛔ sem seam. |
| Força de explosão | Spell passa `D=charge.damage=0.2×sqrt(getSpellPower)/0.6324555` (aprox `0.31623×sqrt(power)`); o calculator literal é `SimpleExplosionDamageCalculator(true,false,Optional.of(1.22×D),blockTag)`, raio **1.5**, `Level.ExplosionInteraction.TRIGGER`. O terceiro argumento é **multiplicador de knockback**, e o segundo `false` desliga o dano de explosão a entidades no calculator Minecraft 1.21.1. | Power escala força, sem converter D em HP. A explosão ainda pode empurrar e interagir com blocos. [Evidência do host](../SOURCE-CONTRACTS-1.2.8.md#host-minecraft-1211); política de mundo BA não é aplicada automaticamente. |
| Impacto/tipo | Depois de `super.onHitEntity`, o override server tenta `entity.hurt(damageSources().windCharge(this,livingOwner),1.0F)` e, se true em LivingEntity, efeitos pós-ataque de enchant; então explode. Se owner for Player, marca **o owner** para ignorar fall damage do impulso atual. Bloco chama superclass, explode no server e descarta; anti-magic explode + discard sem guard de lado próprio. | A tentativa direta local é fixa **1.0**. O superclass também tem callbacks de impacto; não inferir um único hit/explosão física nem dano final total por este override. Mastery requer settlement e owner demonstrados. |
| Persistência | Save NBT escreve Damage e Age; read restaura ambos. Caster desconectado/damageSource em reload ainda precisa QA. | Sem hook seguro para escala por player. |

**Localizadores:** [WindChargeSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/WindChargeSpell.java#L22-L84) · [MagicWindCharge.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/MagicWindCharge.java#L49-L164).

**QA pendente e fail-closed:** Verificar raio/WorldEffectPolicy no modpack, blockTags WIND_CHARGE_EXPLOSIONS, anti-magic, owner/logout, PvP, callbacks de superclass/override, hit direto e força de explosão, proteção de queda do owner e diferenças lado cliente/servidor. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**

## Contratos de suporte — 28/10/2026

Registro ativo e vínculo ao event bus: [AASpells.java L53–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L53-L78). Consumidores documentados: [Magic Wind Charge](../entities/magic-wind-charge.md). Auxiliares não criam raízes adicionais: esta ficha preserva contribuição estrita **1**, enriquecimento **+0**.
