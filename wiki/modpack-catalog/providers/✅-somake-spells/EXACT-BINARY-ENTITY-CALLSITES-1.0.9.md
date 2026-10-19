# Somake Spells 1.0.9 — auditoria física de cinco entidades downstream

**Estado:** ✅ `EXACT_SHA1_ENTITY_METHOD_SYMBOLS_NOT_GAMEPLAY` / ⚠️ caminhos de execução completos, numerais e runtime condicionado / ⛔ nenhuma perk mutadora homologada.

## Fonte e verificações

- Artefato físico Somake 1.0.9: `somakespells-1.0.9-1.21.1.jar`, mod ID `somakespells`, CurseForge File `8867079`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, igual à modlist verificada no sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd` (#513).
- [Java 21 workflow #39195233005](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39195233005) — SUCCESS no HEAD de descoberta; **8 testes sintéticos**, cinco classes exatas, descritores JVM e símbolos de members; [workflow de cast #39195233020](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39195233020) — SUCCESS após o parâmetro opcional de filtro.
- Primeiro workflow [#39195002950](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39195002950) falhou na fixture de teste: o suposto método duplicado tinha descritor diferente; corrigido para nome+descriptor JVM idênticos sem enfraquecer a rejeição de duplicatas.
- [Scanner](../../../../docs/qa/somake_109_entity_method_probe.py), [testes](../../../../docs/qa/somake_109_entity_method_probe_test.py), [workflow](../../../../.github/workflows/somake-109-entity-refs.yml). O JAR, código e assets de terceiros **não** são publicados; a evidência é apenas um JSON de assinaturas e símbolos.

## Inventário exato de entidades, métodos e relações

| Spell de origem | Entidade downstream, com FQCN sob `com.somake.somakespells.entity` | Declarações / métodos de interesse | Símbolos relevantes comprovados |
|---|---|---:|---|
| `somakespells:fragmented_requiem` | `FragmentedSwordRainEntity` | **21 / 15** | `tick`, `updateServerStage`, `applyDamage(LivingEntity,Set)`, `findSpawnPoint`; `updateServerStage` referencia `applyDamage`; `applyDamage` consulta entidades em AABB, obtém `FragmentedRequiemSpell.getDamageSource` e referencia `LivingEntity.hurt(DamageSource,float)` |
| `somakespells:funeral_bloom` | `FuneralBloomControllerEntity` | **28 / 22** | `tick`, `launchWave`, `isValidTarget`, `pruneTargets`, `cancelOwnedBuds`, `onAntiMagic`; `launchWave` usa `AABB.inflate` e `ServerLevel.getEntitiesOfClass`, `isValidTarget` consulta `isSpectator`, `isAlliedTo` e distância ao quadrado; o controller referencia `FuneralBloomBudEntity` em helpers de poda/cancelamento |
| `somakespells:withered_rose_vortex` | `WitheredRoseVortexEntity` | **23 / 17** | `tick`, `pulseDamage`, `getRadius`, `setRadius`, `getTotalLifetime`, `setTotalLifetime`, `onAntiMagic`; `pulseDamage` referencia AABB, filtragem `isAlliedTo`, `WitheredRoseVortexSpell.getDamageSource`, `DamageSources.applyDamage(Entity,float,DamageSource)` e `MobEffects.WITHER` via `MobEffectInstance/addEffect` |
| `somakespells:custodia_caeli` | `CustodiaCaeliSigilEntity` | **18 / 15** | `tick`, `applyBlessing`, `getRadius/setRadius`, `getDuration/setDuration`; `applyBlessing` faz consulta em AABB e filtra `Player.isSpectator`/distância, usando `ModMobEffects.CUSTODIA_CAELI_BLESSING`, `MobEffectInstance` e `Player.addEffect` |
| `somakespells:jingle_bell` | `BellEntity` | **15 / 9** | `tick`, `pulseDamage`, `triggerFinale`, `getOwnerEntity`; `pulseDamage` referencia `AABB.inflate`, `ServerLevel.getEntitiesOfClass`, `JingleBellSpell.getDamageSource` e `DamageSources.applyDamage(Entity,float,DamageSource)` |

**Totais deste recorte:** cinco entidades compiladas presentes no JAR exato; **105 declarações** e **78 métodos de interesse** sob o filtro ampliado. São métodos, não novos feitiços/ações semânticas.

## Consequências para engenharia de perks

| Dimensão | Evidência estática | Decisão |
|---|---|---|
| Dano de Fragmented Requiem | `FragmentedSwordRainEntity.applyDamage` referencia `LivingEntity.hurt` diretamente e `FragmentedRequiemSpell.getDamageSource` | ⚠️ Não afirmar que `SpellDamageEvent` seja postado por esse caminho; requer auditoria de fluxo e coexistência de hooks |
| Dano do Vortex e Jingle Bell | `pulseDamage` referencia o helper provider-host `io.redspace.ironsspellbooks.damage.DamageSources.applyDamage` | ⚠️ Não assumir sem teste que todo overload dispara o mesmo evento, nem recompensar Mastery por cada pulso independentemente |
| Seleção e aliados | Funeral Bloom consulta `isSpectator`, `isAlliedTo`, distância; Vortex consulta `isAlliedTo`; outros consultam AABB | ⚠️ Hitbox de seleção, LOS, times, claims e número de alvos exigem flow/value proof por entidade |
| Intervalo, alcance, área e duração | Helpers `tick`, `getRadius`, `setRadius`, `setDuration`, `setTotalLifetime`, `launchWave` e `pulseDamage` existem | ⛔ A presença de setters internos **não** é evento/API per-player ou contrato de alteração por perk; valores numéricos/caps ainda não extraídos |
| Efeitos e cura | Vortex referencia Wither; Custodia referencia blessing, `Player.addEffect`; Bell tem `triggerFinale` | ⚠️ Duração de buff, stack, potencia e efeito final dependem de validação causal; `SpellHealEvent` do Comforting Lullaby pertence a outro fluxo já catalogado |
| Countermagic e cleanup | `onAntiMagic` existe em Funeral Bloom e Vortex; `cancelOwnedBuds` e `pruneTargets` existem no controller | ⚠️ Não inferir abrangência de dispel nem remoção garantida sem verificar consumidores, condições e lifecycle |
| Efeito downstream adicional | `FuneralBloomBudEntity` aparece nos métodos do controller, mas **não foi auditada nesta campanha** | ⛔ Bloquear promoção do dano/cura da Funeral Bloom até auditar o bud e possíveis rotas secundárias |

## Limites de interpretação

A auditoria prova **referências simbólicas** sob SHA-1 exata; uma chamada pode depender de branches, configurações, alvos e outros mods. Não prova frequência de tick, fórmula, dano aplicado, range real, porcentagem de scaling, retorno efetivo, hitbox mutável, loop de mundo ou aquisição em Survival. Um método ausente das categorias de referência não é prova de ausência de dano/curas delegados.

**Ownership:** Somake controla suas entidades, Iron's controla o casting/resource/damage helper quando usado, RPG Skill Tree controla progressão/Mastery/perks por contrato explícito e Black Arcana apenas seu runtime mágico. Não duplicar `hurt`, `DamageSources.applyDamage`, mana, cooldown, recasts ou contagem de Mastery. Hook seguro por jogador: **⛔ FAIL_CLOSED**.

## Próximo gate

Auditar `FuneralBloomBudEntity` e demais efeitos delegados, inspecionar dataflow de `tick`/`pulseDamage`/`applyDamage`, numerais e caps com unidades, e executar prova provider-loaded e multiplayer em ambiente real antes de qualquer adapter mutador. Nenhuma Stage promovida; 83/83 registros Somake já conhecidos continuam sem novos IDs.
