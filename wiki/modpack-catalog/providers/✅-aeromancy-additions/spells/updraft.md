# Updraft

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:updraft` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:updraft`
- Registered class: `UpdraftSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new UpdraftSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Evidence boundary

Estado documental: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:updraft` — Updraft.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

Os pares **base/per-level** abaixo são campos literais entregues a `AbstractSpell`; não significam `base + per-level×level`. Avaliação de nível, atributos/config e custo/cooldown efetivo pertencem ao host.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast e stats | INSTANT, níveis 1–7, cooldown 30 s, mana base/per-level **80/20**, power base/per-level **3/2**, castTime 0. | Sem dupla cobrança de mana; host controla recast. |
| Target/precast | Utils.preCastTargetHelper(64,0.15f) e rejeita UUID já adicionado no mesmo MultiTargetEntityCastData. getRecastCount=2+level, logo 3–9 slots de recast por nível, sujeito a execução real do host. | Target type/LOS dependem helper Iron's; range=64 é parâmetro do helper, não knockback. |
| Finalização/tempo | No primeiro onCast instala RecastInstance(...,80 ticks, MultiTargetEntityCastData(target)); recasts posteriores adicionam UUID. Só `onRecastFinished` percorre targets, soma Y+0.9 ao movimento e aplica MOVEMENT_SLOWDOWN 100 ticks amplifier 3; cria UpdraftEntity visual (descarta tickCount>8). | Não considerar cada entidade visual spell independente; XP por finalização/efeito real, não por target registrado. |
| Divergência de tooltip | getStunDuration(level)=100+20×level ticks, usado na UI; porém onRecastFinished aplica **100 ticks fixos de MOVEMENT_SLOWDOWN**, sem StunEffect naquele método. Não confundir tooltip com status aplicado. | ⚠️ source discrepancy, não bug runtime confirmado. |
| Dano | Não chama hurt no método de finalização; dano por queda após lançamento pode acontecer pelo motor vanilla, mas atribuição/causalidade não demonstradas. | ⛔ não prometer damageType nem XP on-hit sem settlement. |

**Localizadores:** [UpdraftSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/updraft/UpdraftSpell.java#L29-L138) · [UpdraftEntity.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/updraft/UpdraftEntity.java#L26-L38).

**QA pendente e fail-closed:** QA 3–9 target recasts, UUID duplicado, expiração, alvo unload/morto, diferença tooltip versus duração 100, fall damage e perf de multi-alvos. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**

## Contratos de suporte — 28/10/2026

Registro ativo e vínculo ao event bus: [AASpells.java L53–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L53-L78). Consumidores documentados: [entidade visual](../entities/updraft-visual.md) e [Stunned separado](../effects/stunned.md). Auxiliares não criam raízes adicionais: esta ficha preserva contribuição estrita **1**, enriquecimento **+0**.
