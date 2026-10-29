# Asphyxiate

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:asphyxiate` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:asphyxiate`
- Registered class: `AsphyxiateSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new AsphyxiateSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Evidence boundary

Estado documental: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:asphyxiate` — Asphyxiate.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

Os pares **base/per-level** abaixo são campos literais entregues a `AbstractSpell`; não significam `base + per-level×level`. Avaliação de nível, atributos/config e custo/cooldown efetivo pertencem ao host.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast/custo | CONTINUOUS, level 1–3, cooldown 20 s, mana base/per-level **9/3**, power base/per-level **3/2**; base castTime 100 mas override `getCastTime=100+100×spellLevel` → **200/300/400 ticks**. | Host controle de canal/mana/cancelamento; não duplicar DoT. |
| Target | Utils.preCastTargetHelper(...,15,0.15f); só aceita LivingEntity resolvida e não marcada em AAEntityTypeTags.ASPHYXIATION_IMMUNE. | Range do helper ≠ area em volta; nenhum retarget livre. |
| Status pulso | onServerCastTick quando `getCastDurationRemaining()%10==0` renova BREATHLESS por 10 ticks, amplifier level−1 (0..2). DoT real decorre do efeito, não do onCast. | Reaplicar MobEffect não deve contar um novo cast nem necessariamente dano a cada 10 ticks. |
| Dano/tipo | BreathlessEffect.applyEffectTick tenta `hurt(DamageSources.get(level,AADamageTypes.ASPHYXIATION), 1+0.2×amplifier)`. Frequência `duration%(6−amplifier)==0` = 6/5/4 ticks conforme nível; não checa retorno de hurt. | DamageType ASPHYXIATION do addon, não general Wind magic; Mastery requer dano realmente aceito. |
| Lifecycle | Cancelamento do channel, alvo perdido/immune e pulsos durante troca de dimensão dependem host; client particles não atribuem dano. | ⛔ sem evento per-damage validado. |

**Localizadores:** [AsphyxiateSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/asphyxiate/AsphyxiateSpell.java#L36-L96) · [BreathlessEffect.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/asphyxiate/BreathlessEffect.java#L18-L27).

**QA pendente e fail-closed:** QA immunes, channel interrompido, i-frames, 4–6 tick DoT, target unloading, death, difference nominal spell damage vs specific ASPHYXIATION, hostile PvP. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**

## Contratos de suporte — 28/10/2026

Registro ativo e vínculo ao event bus: [AASpells.java L53–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L53-L78). Consumidores documentados: [Breathless](../effects/breathless.md), [tipo de dano](../data-contracts/asphyxiation-damage.md) e [imunidade](../data-contracts/entity-type-tags.md). Auxiliares não criam raízes adicionais: esta ficha preserva contribuição estrita **1**, enriquecimento **+0**.
