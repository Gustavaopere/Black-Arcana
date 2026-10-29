# Airblast

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:airblast` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:airblast`
- Registered class: `AirblastSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new AirblastSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Evidence boundary

Estado documental: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:airblast` — Airblast.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

Os pares **base/per-level** abaixo são campos literais entregues a `AbstractSpell`; não significam `base + per-level×level`. Avaliação de nível, atributos/config e custo/cooldown efetivo pertencem ao host.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast/stats | INSTANT, level 1–5, cooldown default 0.75s, castTime 0, mana base/per-level **30/4**, power base/per-level **5/1**. | Cooldown decimal provider-host, não arredondar sem inspecionar host. |
| Geometria/scan | Busca Projectile.class na AABB do caster inflate(radius), com `radius=2+spellLevel` (3..7); depois filtra distância real `<radius`, owner != caster, e tipo não REFLECTION_IMMUNE; por fim exige ângulo entre direção do olhar e caster→proj **< getArc(level)=20+5×level graus**, isto é, 25..45° de **semiângulo**, não ângulo total de cone. | SEM_HOOK_SEGURO para radius/arc/target cap; scan per-cast sujeito a densidade. |
| Ação/owner | Para cada projétil elegível, `deflect` define owner=deflector, velocidade=normalize(deflector.look)×(0.15×getSpellPower) se Player; se não Player, usa unit look sem escala, hasImpulse=true. | Alteração owner afeta atribuição de dano/Kill credit; RPG não reatribui casts/hits sem causalidade. |
| Dano/tipo | Sem chamada hurt no corpo Airblast; trajetória resultante e dano do projétil rebatido dependem da entidade original, não são um novo spell Wind. | Não conceder Mastery ofensiva por reflexão sem hit aceito. |
| Lado de execução | onCast não possui local !isClientSide guard antes de setOwner/setDeltaMovement; verificações de host e network side precisam teste. | ⛔ client-owned perks e mutação duplicada. |

**Localizadores:** [AirblastSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airblast/AirblastSpell.java#L29-L118).

**QA pendente e fail-closed:** QA raio 3..7, ângulos exatos < e owner chain, projéteis aliados e protegidos, entity cap, Armor/Attribute scaling e sides. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**

## Contratos de suporte — 28/10/2026

Registro ativo e vínculo ao event bus: [AASpells.java L53–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L53-L78). Consumidores documentados: [tags de reflexão](../data-contracts/entity-type-tags.md). Auxiliares não criam raízes adicionais: esta ficha preserva contribuição estrita **1**, enriquecimento **+0**.
