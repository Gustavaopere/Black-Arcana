# Feather Fall

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:feather_fall` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:feather_fall`
- Registered class: `FeatherFallSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new FeatherFallSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Naming boundary

O source pin registra literalmente `aero_additions:feather_fall` através de `FeatherFallSpell`. O dossiê histórico registra discrepância de apresentação entre “Feather Fall” e “Feather Flight”; esta ficha usa o registry ID exato e não normaliza display-name por inferência.

## Evidence boundary

Estado documental: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:feather_fall` — Feather Fall.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

Os pares **base/per-level** abaixo são campos literais entregues a `AbstractSpell`; não significam `base + per-level×level`. Avaliação de nível, atributos/config e custo/cooldown efetivo pertencem ao host.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast/custo | LONG, níveis 1–5, cooldown 90 s, mana base/per-level **50/20**, power base/per-level **30/30**, castTime=50; duração `(int)(getSpellPower×20)` ticks. | Valores base sujeitos ao school power real. |
| Alvo/área | Precast usa Utils.preCastTargetHelper(...,32,0.35,false) e faz fallback para self; visual TargetedArea radius=3. onCast varre `target.getBoundingBox().inflate(3)` e filtra distância esférica `<9` e Utils.shouldHealEntity. | Geometria broadphase AABB + sphere, nunca raio AOE de ataque. Nenhuma capacidade de trocar target via API comprovada. |
| Máximo alvos | Constante MAX_TARGETS=5; cada LivingEntity qualificada recebe MobEffect FLIGHT amplifier 0 por duration. A seleção é ordem da iteração, não priority targeting comprovada. | ⛔ aumento de caps/limites sem hook e testes de custo. |
| Atributos nativos | O registro FLIGHT adiciona **WATER_MOVEMENT_EFFICIENCY +1 ADD_VALUE** e **MOVEMENT_SPEED +0.15 ADD_MULTIPLIED_BASE**, ID `aero_additions:effect.flight` em cada atributo. O produtor sempre usa amplifier 0. | Valores base de modifier, não velocidade final garantida; não são concessão de `mayfly`/voo criativo. |
| Efeito de gravidade | FlightEffect a cada 20 entity ticks remove modifier `aero_additions:flight.gravity`, calcula weightScore por equipamento (0 light/empty, 4 heavy, 10 anvil, 2 demais), aplica `ADD_VALUE=(weightScore/4)-0.08` na GRAVITY quando score!=0; remove modifier no fim do efeito. | Perk de gravidade interage diretamente com AttributeInstance; não sobrescrever ID e não assumir que sempre reduz gravidade. |
| Outros handlers | AAServerEvents registra PlayerSwimEvent para entidade com FLIGHT como SUCCESS; o comportamento real de natação/queda deve ser observado. | FLIGHT effect provider-owned; sem duplicação por Black Arcana. |

**Localizadores:** [FeatherFallSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/feather_fall/FeatherFallSpell.java#L29-L106) · [AASpells.java — modifiers L165–167](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L165-L167) · [FlightEffect.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/feather_fall/FlightEffect.java#L23-L69) · [AAServerEvents.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L120-L124).

**QA pendente e fail-closed:** QA raio exato 3 e max5, buffs hostis/aliados, gravity weights com armor, equipment changes, modifier removal e compat Epic Fight. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**

## Contratos de suporte — 28/10/2026

Registro ativo e vínculo ao event bus: [AASpells.java L53–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L53-L78). Consumidores documentados: [Flight](../effects/flight.md) e [tags de peso](../data-contracts/item-tags.md). Auxiliares não criam raízes adicionais: esta ficha preserva contribuição estrita **1**, enriquecimento **+0**.
