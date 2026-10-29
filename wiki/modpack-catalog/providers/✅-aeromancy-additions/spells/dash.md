# Dash

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:dash` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:dash`
- Registered class: `DashSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new DashSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Evidence boundary

Estado documental: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:dash` — Dash.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

Os pares **base/per-level** abaixo são campos literais entregues a `AbstractSpell`; não significam `base + per-level×level`. Avaliação de nível, atributos/config e custo/cooldown efetivo pertencem ao host.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast/stats | INSTANT, level 1–5, cooldown 2s, mana base/per-level **20/2**, power base/per-level **10/5**, castTime 0. | Sem duplicar gasto ou cooldown do host. |
| Vetor/cinemática | multiplier `(15+getSpellPower)/12`. Direção = lookAngle.multiply(2,1,2).normalize().scale(multiplier). Em onCast grava ImpulseCastData + setDeltaMovement usando lerp(1,old,vec)=vec, sobrescrevendo velocidade anterior; em onClientCast soma vetor recebido ao movimento client existente. | Risco de divergência server set vs client add, não bug medido; QA jitter/desync. |
| Proteção | onCast define invulnerableTime=20 e envia DashParticlesPacket a tracking entity + self; não cria DamageSource nem invoca hurt neste body. | Alteração de i-frames/velocity per-player ⛔ sem seam; não confundir invulnerableTime com blindagem universal. |
| Alvo/range | Self movement, sem AOE/projétil, move na direção do olhar; velocidade depende do power efetivo do caster. | Perk de distance/speed exigiria modificar vetor na origem, antes da replicação. |
| Causalidade | Um impulso e seus packets/partículas pertencem ao mesmo cast, e não a vários procs de Mastery. | Idempotência C2S e teste de cliente, fall/PvP. |

**Localizadores:** [DashSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/dash/DashSpell.java#L25-L85).

**QA pendente e fail-closed:** QA direções extremas, motion server-vs-client, 20 i-frames, speed de atributos, colisão/claims, reconnect e cost/animation. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**

## Contratos de suporte — 28/10/2026

Registro ativo e vínculo ao event bus: [AASpells.java L53–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L53-L78). Consumidores documentados: [payload de partículas](../payloads/dash-particles.md). Auxiliares não criam raízes adicionais: esta ficha preserva contribuição estrita **1**, enriquecimento **+0**.
