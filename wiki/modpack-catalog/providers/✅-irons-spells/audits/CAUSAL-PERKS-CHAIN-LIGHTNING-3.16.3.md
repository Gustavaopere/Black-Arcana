# Iron's 3.16.3 — Chain Lightning: causalidade para perks

**Estado:** ✅ execução estática fonte pinada analisada; ⚠️ API de mutação de branching, runtime e validação física não certificados. **Sem novos objetos mágicos.**

- Identidade: `irons_spellbooks:chain_lightning`; classe [`ChainLightningSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/lightning/ChainLightningSpell.java), entidade provider [`ChainLightning`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/ChainLightning.java), registro [`EntityRegistry.CHAIN_LIGHTNING`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/registries/EntityRegistry.java#L479-L483).
- Fonte: `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`, versão documental Iron's 3.16.3 (MC 1.21.1); bytecode, config implantada e gameplay requerem aceitação adicional.

## Causalidade

1. **Preflight de alvo inicial:** `checkPreCastConditions` chama `Utils.preCastTargetHelper(level,caster,magicData,spell,32,0.35f)`. O raycast de aquisição tem **32 blocos** e inflação de mira **0,35**, **diferentes** da distância entre saltos. O helper registra `TargetEntityCastData` na sessão. [spell](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/lightning/ChainLightningSpell.java#L54-L59), [helper](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L706).
2. **Casting:** `INSTANT`, 0 ticks base, cooldown default 20 s; mana base 25 + 7 por nível adicional, 10 níveis, base power 6 + 1 por nível adicional. `onCast` só cria entidade ChainLightning quando `TargetEntityCastData` resolve alvo real em `ServerLevel`. Não há alvo novo escolhido por evento de lançamento nesta classe. [spell](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/lightning/ChainLightningSpell.java#L33-L78).
3. **Valores de cada conjuração:** `getDamage = power`; `getMaxConnections = 3 + spellLevel`; `getRange = 1 + 0,5 × power`. Power inclui atributos da entidade e multiplicador de configuração da classe-base. No caso sem bônus externos e com multiplicador padrão 1, nível 1: dano base 6, até 4 vítimas totais por cast, saltos de 4 blocos; nível 10: dano base 15, até 13 vítimas, saltos de 8,5 blocos. Estes exemplos são **derivações matemáticas das fórmulas**, não resultados de gameplay. [spell](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/lightning/ChainLightningSpell.java#L80-L90), [power](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L211-L225).
4. **Execução no servidor:** [`ChainLightning.tick`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/ChainLightning.java#L54-L97) aplica dano inicial na primeira janela, e processa novas ondas **a cada 6 ticks**; `maxConnectionsPerWave=3`. Os candidatos são buscados ao redor de cada vítima da onda anterior, ordenados por distância e filtrados pelo raio, linha de visão, aliados e identidades já atingidas. `allVictims`/`lastVictims` impedem repetição direta da mesma vítima no encadeamento. A contagem total `hits` é incrementada em `doHurt`.
5. **Settlement por vítima:** `doHurt` usa `DamageSources.applyDamage(victim,damage,sourceDaChainLightning)` e spawn visual. Portanto `SpellDamageEvent` é um ponto de modificação de montante por aplicação em `LivingEntity` (e não um evento de seleção de saltos). [`ChainLightning`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/ChainLightning.java#L99-L114), [`DamageSources`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/damage/DamageSources.java#L44-L65).
6. **Lifetime:** `ChainLightning.shouldBeSaved()` retorna false, e o entity de efeito se descarta quando não há novas vítimas. O registro físico de entidade tem `sized(1f,1f)`, mas isso **não determina o raio entre saltos**. [entidade](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/ChainLightning.java#L136-L139), [registro](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/registries/EntityRegistry.java#L479-L483).

## Perks e limites

| Eixo | Fórmula/mecanismo | Viabilidade confirmada |
|---|---|---|
| Dano por aplicação | power, chamado por `doHurt` | ✅ `SpellDamageEvent.setAmount` altera dano-base antes de resistência; ⚠️ não implementado/testado em adapter |
| Número de vítimas | `3 + spellLevel` inclui a primeira vítima; `maxConnectionsPerWave=3` | ⛔ nenhum setter de evento do provider para limites de saltos confirmado |
| Alcance inicial | preflight raycast 32 blocos | ⛔ não confundir com `getRange`; sem evento de extensão seguro |
| Distância dos saltos | `1+0,5×power`, consulta por vítima e LOS | ⚠️ atributos de spell power alteram distância **indiretamente**, mas não comprovam capacidade de alterar somente o alcance |
| Periodicidade | ticks 1, 7, 13... da entidade enquanto há saltos | ⛔ sem seam de manipulação da frequência confirmado |
| Tipo do dano | `SPELL.get().getDamageSource(this,getOwner())` | ⛔ evento de dano não expõe substituição de DamageType |
| Recursão/duplicação | `allVictims`, `lastVictims` e cap total | ⛔ não gerar outra ChainLightning para cada evento de dano; risco de proc chain e bypass do orçamento |
| Mana/cooldown | base provider + config | ⚠️ alterar custo com `SpellOnCastEvent` ocorre após a admissão original |

**Dependências entre parâmetros:** uma modificação de nível por [`ModifySpellLevelEvent`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/ModifySpellLevelEvent.java) pode alterar **simultaneamente** dano, número total de vítimas e distância por `getMaxConnections`/`getRange`; não é uma API para modificar somente um desses eixos. Como `getLevelFor` não foi auditado em todas as origens do casting, esta possibilidade é **condicionada** até comprovação do caller e dos caps.

### QA

- [ ] Confirmar classfile do artefato do pack e config carregada.
- [ ] Medir ciclo das ondas com 1, múltiplos e nenhum alvo subsequente; verificar limites com addons e spell power extremo.
- [ ] Testar PvP, equipes, claims, bosses, descarte, target invalidado antes do cast e world unload.
- [ ] Provar contrato real do RPG para escolher cap per-player sem editar pipeline nativo.
- [ ] Teste servidor/cliente e garantir uma recompensa/proc por ação canônica, não por elo de dano quando aplicável.

Complementa [ficha existente](../lightning/chain-lightning.md); não introduz mutações não certificadas.
