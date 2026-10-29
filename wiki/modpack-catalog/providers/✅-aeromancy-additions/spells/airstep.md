# Airstep

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:airstep` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:airstep`
- Registered class: `AirstepSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new AirstepSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Evidence boundary

Estado documental: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:airstep` — Airstep.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

Os pares **base/per-level** abaixo são campos literais entregues a `AbstractSpell`; não significam `base + per-level×level`. Avaliação de nível, atributos/config e custo/cooldown efetivo pertencem ao host.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast/atributos | LONG, 1–7, cooldown 90 s, castTime 30, mana base/per-level **60/10**, power base/per-level **30/10**; duração `(int)(getSpellPower×30)` ticks, amplifier=level−1. | Power multipliers alteram duração: config base não é duração efetiva. |
| Counter / slots | onCast aplica AIRSTEPPING e grava AeromancySpellData.airStepHitsRemaining=1+level, isto é, **2..8** saltos; a attachment sync usa AASyncPlayerDataPacket; NBT save escreve Float, load lê Int para a chave homônima. | ⚠️ divergência de tipo NBT source-only; não editar attachment de outro provider. QA save/reload obrigatório. |
| Pacote C2S | AirstepPacket contém deltaX, deltaZ inteiros sem clamp visto no decoder, usa IPayloadContext.enqueueWork e chama `airstepJump(packet,ctx.player())`; o método de salto checa effect, contador>0 e !onGround, normaliza input e usa move Y=JUMP_STRENGTH+getJumpBoostPower. | ⚠️ input bounds/rate-limit/forged packet necessitam QA; sem perk manipulando rede host. |
| Fall / reset | LivingFallEvent com effect ativo e distância>=SAFE_FALL_DISTANCE cancela multiplicador de dano (setDamageMultiplier(0)) se restar salto; o handler **recarrega contador em todo LivingFallEvent com efeito**, independentemente do gate de distância. Remoção/expiração do MobEffect limpa contador. | Evento pré-resultado e recarga por evento ≠ novo cast, não atribuir Mastery por tick. |
| Dano/target | Self locomotion, sem projectile/damageSource/radius de ataque. O movimento pode interagir com fall damage e Epic Fight. | ⛔ per-user jump cap/speed sem boundary real. |

**Localizadores:** [AirstepSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L41-L145) · [AirstepPacket.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepPacket.java#L11-L37) · [AeromancySpellData.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L42-L124).

**QA pendente e fail-closed:** Testar NBT Float→Int, reload/logout, replay de packet e inputs extremos, fall hooks, PvP, knockback/latência, sprint/Epic Fight e server-authoritative contador. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**

## Contratos de suporte — 28/10/2026

Registro ativo e vínculo ao event bus: [AASpells.java L53–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L53-L78). Consumidores documentados: [Airstepping](../effects/airstepping.md), [payload C2S](../payloads/airstep.md) e [estado/attachment](../systems/aeromancy-spell-data.md). Auxiliares não criam raízes adicionais: esta ficha preserva contribuição estrita **1**, enriquecimento **+0**.
