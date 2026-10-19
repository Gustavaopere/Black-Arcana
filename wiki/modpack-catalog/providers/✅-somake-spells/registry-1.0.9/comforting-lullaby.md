# `somakespells:comforting_lullaby`

- Provider: **Somake Spells** (`somakespells`)
- Artifact: `somakespells-1.0.9-1.21.1.jar`
- Physical / publisher SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`
- Substrate: **Iron's Spells 'n Spellbooks**
- Registry identity: `somakespells:comforting_lullaby`
- Registration gate: **Unconditional**
- Current composition registration: **ADMITTED**
- State: `EXACT_PHYSICAL_REGISTRY / CURRENT_REGISTRATION_ADMITTED / STRICT_COUNT_CONDITIONAL`

## Registration evidence

The exact physical 1.0.9 `ModSpells` topology registers this identity without an optional-provider registration predicate.

The exact current artifact has 83 unique Somake spell registry IDs, and the present mod composition satisfies all optional registration predicates. This card records one of those **83/83 currently admitted registrations**.

## Host / progression boundary

Exact 1.0.9 structural evidence found no provider `isEnabled()` override among the 83 spell classes. That does **not** substitute for the effective deployed Iron's spell configuration.

Exact structural audit identifies a provider `allowCrafting()` override for this spell that is constant-false. That blocks ordinary crafting through that provider method, but it does not by itself prove the absence of every provider-owned loot/equipment/progression route.

Still unresolved for strict semantic promotion:

- effective Iron's per-spell/global/datapack `enabled`;
- effective Iron's `allow_crafting` where applicable;
- deployed Somake `enableSpellLockSystem` COMMON value;
- object-level or bounded-set survival acquisition/reachability;
- assembled-pack progression/runtime settlement.

## Counting boundary

This is an exact current registry identity, not yet an independently strict-counted semantic action. Registration presence alone does not add this card to the strict numerator while the host/provider config and reachability gates above remain open.

Do not infer display name, school, level, rarity, mana cost, cooldown, damage, duration, targeting, recipe, loot source or formulas from the registry path.

## Authority

Iron's owns host casting/resource/cooldown settlement. Somake owns this spell identity and its provider progression. Black Arcana catalogs and may observe supported provider state; it does not recreate either runtime.

Sources: `../EXACT-1.0.9-REGISTRY-AUDIT.md`, `../EXACT-1.0.9-REGISTRATION-GATE-MAP.md`, `../SPELL-CATALOG-1.0.9.md`.

**Gate deste spell — `CONSTANT_FALSE`:** a auditoria do método `allowCrafting()` do provider encontrou retorno constante `false`. **Não tratar como indisponível para casting**; rastrear outras rotas de aquisição separadamente. Não atribuir a uma perk externa um mecanismo de desbloqueio de crafting não provado.

## Dossiê técnico para perks — gate de aquisição (18/10/2026)

**Escopo da prova:** presença do ID na registry e classificação do override `allowCrafting()` no JAR físico 1.0.9. Não é prova de execução de cast, atributos, alvo ou integrabilidade em produção. A linha física está fixada pelo SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` (CurseForge File `8867079`). A árvore de código fonte público exato para o release não foi localizada.

| Dimensão para perk | Fato verificável / limite |
|---|---|
| Registrar | `com.somake.somakespells.registries.ModSpells`, ID deste documento no `DeferredRegister<AbstractSpell>` |
| Classe/método de seleção ou efeito | **NÃO VERIFICADO** em nível de método individual / FQCN; somente classe `*Spell` e `allowCrafting()` identificados na auditoria estrutural |
| Admissão de casting | `isEnabled()` **não é sobrescrito** pela classe no provider; Iron's host, config e datapack efetivos **NÃO VERIFICADOS** |
| Targeting e LOS | Tipo de alvo, distância de aquisição, alcance do efeito e linha de visão **NÃO VERIFICADOS** |
| Geometria | Raio/ângulo/altura da área, hitbox, velocidade/quantidade de projéteis e multiplicidade de alvos **NÃO VERIFICADOS** |
| Dano/cura | Damage source, tipo/elemento, fórmulas, status, buffs/debuffs, knockback e eventuais procs **NÃO VERIFICADOS** |
| Tempo e recursos | Tempo de cast, cooldown, custos, duração/ticks, scaling e caps **NÃO VERIFICADOS** |
| Causalidade | Cast → efeito secundário → acertos/procs e identidade para deduplicação **NÃO VERIFICADOS**; não atribuir Mastery por evento sem correlação |
| Mutabilidade por perk | **⛔ FAIL_CLOSED** para alterar disponibilidade, geometria, dano, custos ou cast: nenhum hook/adapter mutador foi demonstrado nesta ficha |
| Autoridades | Somake: identidade/gate específico; Iron's: host de casting/custos/cooldowns; RPG Skill Tree: progressão por boundary comprovado; Black Arcana: somente runtime mágico próprio e observação permitida |

**Separar fatos:** `allowCrafting()` decide uma superfície de *craftability* e não comprova proibição de cast nem ausência de loot, comando, equipamento, transferência ou qualquer via especial de obtenção. Um possível gate de perk não pode simplesmente reabrir essa rota sem contrato verificável do host/provider. O code default `enableSpellLockSystem=false` não representa a configuração COMMON implantada.

**Testes pendentes:** comparar os métodos de admissão e as classes de efeito do JAR exato com a config/Datapack do perfil real; medir parâmetros com unidades; inspecionar API/eventos do host 3.16.3; validar fallback, aquisição em Survival, mudança de perk/equipamento, servidor/cliente, deduplicação e ausência de dupla cobrança. Nenhum destes testes é declarado PASS nesta atualização.

**Provas imutáveis:** [auditoria 1.0.9](https://github.com/Gustavaopere/Black-Arcana/blob/511ec03f0da62ebfc1722825def50354594976c3/wiki/modpack-catalog/providers/%E2%9C%85-somake-spells/EXACT-1.0.9-REGISTRY-AUDIT.md) e [gate map](https://github.com/Gustavaopere/Black-Arcana/blob/511ec03f0da62ebfc1722825def50354594976c3/wiki/modpack-catalog/providers/%E2%9C%85-somake-spells/EXACT-1.0.9-REGISTRATION-GATE-MAP.md).
