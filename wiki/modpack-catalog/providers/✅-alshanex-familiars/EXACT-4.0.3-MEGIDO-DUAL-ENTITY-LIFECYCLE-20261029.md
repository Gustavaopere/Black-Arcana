# Megido — contratos exatos de lifecycle/targeting no Alshanex 4.0.3 e Iron's 3.16.3

Estado: `EXACT_DUAL_JAR_ABI_AND_DIRECT_CALLS_VERIFIED / EFFECTIVE_TARGET_CAP_NOT_VERIFIED / NO_MUTATOR / NO_PHYSICAL_QA`.

## Autoridades físicas e proveniência

- **Alshanex's Familiars**, `alshanex_familiars-1.21.1_v4.0.3.jar`, mod ID `alshanex_familiars`, SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686` — físico da modlist do `neoforge-rpg-skilltree`.
- **Iron's Spells 'n Spellbooks**, `irons_spellbooks-1.21.1-3.16.3.jar`, mod ID `irons_spellbooks`, SHA-1 `017fd8140c477f9ae602cf95594f1c23bef1d6e3` — físico reconfirmado na modlist. CurseForge [File ID 8680204](https://www.curseforge.com/minecraft/mc-mods/irons-spells-n-spellbooks/files/8680204).
- Execução exata: [GitHub Actions run 40973406416](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40973406416), job `exact_dual_entity_abi` (`123795466882`), **SUCCESS** e seis testes sintéticos **PASS**. Artifact JSON textual `12941052062`, com apenas nomes de métodos, descritores e agregados de chamadas.
- Auditor reproducível: `docs/qa/alshanex_403_megido_entity_dual_provider.py`; regressões `docs/qa/alshanex_403_megido_entity_dual_provider_test.py`; workflow `.github/workflows/alshanex-403-megido-dual-entity-abi.yml`.

**Limite clean-room:** ambos os JARs tiveram hashes verificados antes da leitura das classes. `javap -p -s -c` foi utilizado apenas para inspeção transitória; nenhum bytecode, corpo de método, ordem de instruções, código ou asset de terceiros foi versionado ou anexado. Relatórios expõem contratos de interoperabilidade, não implementação proprietária. As análises anteriores de `MegidoSpell.onCast` em [ABI do cast](EXACT-4.0.3-MEGIDO-ONCAST-TARGET-ENTITY-ABI-20261029.md) comprovam **referências** às duas entidades, não o número efetivo de spawns.

## MegidoEntity — classe exata de Alshanex

Classe observada: `net.alshanex.alshanex_familiars.entity.misc.MegidoEntity`. Foram detectados **21 corpos de métodos declarados** (incluindo overloads, construtores e métodos sintéticos).

| Método compilado | ABI e dependências diretamente verificadas | Teto da prova |
|---|---|---|
| `tick(): void` | **180 instruções, 11 branches**, referência a `getClosestEntity(Entity,double):Entity` **1 vez**, `doHurt(Entity):void` **2 vezes**, e `AbstractMagicProjectile.tick():void` **1 vez** | Dois callsites de dano **não** implicam dois hits por tick; controle de fluxo, condições e loops não foram recompostos |
| `getClosestEntity(Entity,double):Entity` | **49 instruções, 2 branches**, **2 referências** a `Stream.filter(Predicate)` | Há filtros simbólicos, mas predicados, prioridades, bounds, exclusões e cardinalidade **não** foram certificados |
| `getRandomBall(Entity,double):Entity` | **45 instruções, 1 branch**, **2 referências** a `Stream.filter(Predicate)` | Não comprova disparos, busca global ou seleção real de entidades |
| `canHitEntity(Entity):boolean` | **23 instruções, 6 branches**; invoca `AbstractMagicProjectile.canHitEntity(Entity):boolean` | O predicado final e regras de owner/equipe/imunidade exigem inspeção adicional |
| `doHurt(Entity):void` | **61 instruções, 1 branch**; invoca `AbstractSpell.getDamageSource(Entity,Entity)` e `DamageSources.applyDamage(Entity,float,DamageSource)`, do Iron's, uma vez cada | Existe uma referência de dano; valor real, repetição, guarda e dano aplicado **não** comprovados |
| `shouldBeSaved():boolean` | **2 instruções**, nenhuma chamada registrada | O valor booleano **não** foi auditado como constante |

As rotinas `lambda$getClosestEntity$...` e `lambda$getRandomBall$...` existem no binário; elas **não** foram utilizadas para declarar o conteúdo dos filtros.

## BallLightning — classe exata de Iron's

Classe observada: `io.redspace.ironsspellbooks.entity.spells.ball_lightning.BallLightning`. Foram detectados **12 corpos de métodos declarados**.

| Método compilado | ABI e dependências diretamente verificadas | Teto da prova |
|---|---|---|
| `tick():void` | **23 instruções, 2 branches**; chama `AbstractMagicProjectile.tick():void` e contém **1 referência** a `discard():void` | O caminho que descarta a entidade, prazo de vida e condição de ativação permanecem `NOT_VERIFIED` |
| `canHitEntity(Entity):boolean` | **12 instruções, 3 branches**; referencia `canHitVictim(Entity):boolean` e `AbstractMagicProjectile.canHitEntity(Entity)` | Filtros finais e direitos de ataque não homologados |
| `canHitVictim(Entity):boolean` | **20 instruções, 3 branches** | Sem interpretação certificada da condição de vítima |
| `handleHitDetection():void` | **68 instruções, 4 branches**; contém **2 referências** a `onHit(HitResult):void` | Não demonstra dois hits reais; handlers, colisões e regiões de efeito precisam de QA |
| `onHitEntity(EntityHitResult):void` | **36 instruções, 1 branch**; referencia `getDamage():float`, `AbstractSpell.getDamageSource(Entity,Entity)` e `DamageSources.applyDamage(Entity,float,DamageSource)` **1 vez cada** | Pipeline de aplicação de dano identificado; quantidade, valor e casos de bloqueio pendentes |
| `onHitBlock(BlockHitResult):void` | **9 instruções, 1 branch**; chama `AbstractMagicProjectile.onHitBlock(BlockHitResult)` | Efeito sobre bloco, descarte e proteção de mundo não homologados |

## Matriz de responsabilidade e riscos de perks

| Superfície | Owner observável no binário | Implicação |
|---|---|---|
| Casting e `MegidoSpell.onCast` | Alshanex, estendendo Iron's | Nenhum segundo lançamento/custo deve ser criado pelo Black Arcana |
| `MegidoEntity`, busca e chamadas `doHurt` | Alshanex com utilitário de dano do Iron's | Perks de alvo/dano exigem comprovar predicates e limites reais |
| `BallLightning` e sua colisão/dano | Iron's Spells | Alterar apenas `getMaxConnections` de Megido não comprova mutação do comportamento da entidade Iron's |
| `Integer.MAX_VALUE` retornado pelo `getMaxConnections` de `MegidoSpell` | Alshanex 4.0.3, auditoria anterior | **Não é número de alvos reais**; somar conexões pode ser redundante ou provocar overflow |
| RPG Skill Tree | Sibling de progressão | Não assume casting, cooldown, targeting ou liquidação de dano |

**Gates não fechados:** fluxo dinâmico dos filtros, seleção e cardinalidade de alvos, budgets/loops/limites de busca, caso de falha de `applyDamage`, dano por alvo, deduplicação, persistência, chunks carregados, world-safety, custo/cooldown e validação em servidor real com os dois providers. O CI de inspeção binária **não** é GameTest de comportamento externo nem QA física do modpack.

**Estados:** `COMPLETE_PERK_READY=0`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; identidade do catálogo Alshanex permanece **7 spells + 11 rituais = 18**. Não promover status alfabético/Stage, não criar entidades adicionais ou hooks por inferência.
