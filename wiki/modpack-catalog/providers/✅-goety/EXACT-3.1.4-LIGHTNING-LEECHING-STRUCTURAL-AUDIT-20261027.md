# Goety 3.1.4 — Lightning, LIFE_LEECH e consumidores de cura

**27/10/2026 · auditoria documental e estrutural.** Continuação da [análise de Lightning/Leeching](SOURCE-ADJACENT-LIGHTNING-LEECHING-3.1.1-20261027.md) integrada na PR #928. A lógica descrita como fonte pertence exclusivamente a **Goety 3.1.1**, commit **`6c41a04f2d712097c4461f969a6bb8ee277149ef`**. A prova **3.1.4** confirma descritores, referências diretas de campos/métodos e presença de anotações nos classfiles selecionados. Não comprova equivalência de fórmulas, branches, ordem de eventos, configuração ou gameplay.

## Artefato e método de auditoria

- Publisher: [CurseForge 8689429](https://www.curseforge.com/minecraft/mc-mods/goety/files/8689429), projeto `586095`; [download reproduzível](https://cursemaven.com/curse/maven/goety-586095/8689429/goety-586095-8689429.jar).
- `goety-3.1.4.jar`: **78708199 bytes**, SHA-1 **`a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`**, SHA-256 **`5158b9df105827f8c3f800396bcfce19076ec98ee9c4bd7a0d656b58cf28701e`**; fingerprints revalidados no arquivo publisher, iguais à autoridade histórica do [inventário exato](EXACT-3.1.4-SEMANTIC-INVENTORY.md). Não houve nova medição do perfil físico original.
- JDK 21, `javap -p -s -c` para referências de instruções dentro de cada método, e inspeção de anotações delimitadas por método. **49 verificações passaram**, cobrindo **15 métodos de 6 classes**. O relatório guarda símbolos/descritores, não corpos, offsets, caminhos de branches, operandos numéricos ou assets.
- O parser separa overloads por descritor e termina métodos antes do inicializador estático. Ausências declaradas são **locais ao método selecionado**: não excluem helpers, herança, outros listeners, mixins ou comportamento dinâmico. Dono omitido pelo `javap` é registrado como dono simbólico da classe atual, sem afirmar a classe declarante da implementação.

## Execução reproduzível e evidência permanente

[GitHub Actions #40542506434](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40542506434) concluiu **SUCCESS** no commit **`7b1a302c3e0fc6305e2ed01c402f9b2e6d183575`**: **49/49 verificações**, 15 métodos, 6 classes. O artefato `goety-314-lightning-leech-symbolic-report`, ID **`12751217982`**, tem digest **`sha256:3385499e2125d30d43717a77d1d932797b7246703017c31a023cfce8c1c010c1`**; o download do ZIP foi reconferido por esse hash e seu JSON conferido após a execução. Retenção configurada: **30 dias**; a tabela deste documento preserva o alcance factual depois da expiração do artefato.

O [workflow pinado](https://github.com/Gustavaopere/Black-Arcana/blob/7b1a302c3e0fc6305e2ed01c402f9b2e6d183575/.github/workflows/goety-314-lightning-leech-symbolic-temporary.yml) contém o probe completo para repetição com JDK 21 e download sujeito aos dois hashes. Ele fica na branch isolada `audit/goety-314-lightning-leech-symbolic-20261027`, **fora da main documental e do runtime**. Não carrega o mod em jogo nem executa seu JAR; inspeciona classfiles e publica somente JSON delimitado. O parser foi conferido contra contaminação por constant pool, inicializador estático e atributos da classe; workflow e script foram revisados independentemente. CI verde deste probe não homologa a semântica de gameplay.

## Relações presentes no JAR SHA-exato

Prefixo das classes Goety abaixo: `com.Polarice3.Goety.`.

| Método inspecionado | Relações estruturais comprovadas | Limite da afirmação |
|---|---|---|
| `common.magic.spells.necromancy.LeechingSpell#SpellResult(ServerLevel,LivingEntity,ItemStack,SpellStat)` | Referencia `ModDamageSource.lifeLeech`, `LivingEntity.hurt`, `rightStaff` e `LivingEntity.addEffect`; não há referência direta a `LivingEntity.heal` ou ao campo `SpellConfig.LeechingPercent` nesse método | Ausência local não é ausência de cura no pipeline; não certifica condições, números ou cadência |
| `utils.ModDamageSource#lifeLeech(Entity,Entity)` e `#noKnockbackDamageSource(...)` | A primeira referencia `LIFE_LEECH` e a factory de fonte; esta referencia o construtor de `NoKnockBackDamageSource` | Não comprova identidade de cast raiz ou resultado de dano |
| `common.events.ModEvents#DamageEvent(LivingDamageEvent.Pre)` | Anotação `SubscribeEvent`; referências a `LIFE_LEECH`, `LeechingPercent`, `DamageSource.getEntity`, `Pre.getNewDamage`, `LivingEntity.heal`, `Pre.setNewDamage` e `getReducedDamage`; classe com `EventBusSubscriber` | Confirma o consumidor estrutural no artefato. Não transfere a fórmula/ordem da fonte 3.1.1 para o binário nem prova registro/execução do subscriber no pack |
| `ModEvents#onLivingHeal(LivingHealEvent)` | Anotação `SubscribeEvent`; referências a `CURSED`, `hasEffect`, `getLastDamageSource`, `hellfireAttacks`, `getAmount` e `setCanceled` | São referências ao caminho de controle da cura; condições, amount final e cura efetiva continuam pendentes |
| `common.magic.spells.storm.LightningSpell#SpellResult(...)` | Referencia `rayTrace`, `BlockFinder.findLightningRod`, `getTarget`, `SpellLightningBolt.setDamage/setOwner` e `ServerLevel.addFreshEntity` | Presença das chamadas não prova prioridade de branches, alcance, quantidade por cast ou spawn aceito |
| `utils.BlockFinder#findLightningRod` | Overload de dois argumentos referencia o de três; este referencia `PoiManager.findClosest` | Não certifica raio numérico ou proteção de mundo |
| `common.entities.projectiles.SpellLightningBolt#tick()` | Referencia strike hook, `Entity.thunderHit`, `LivingEntity.hurt`, `ModDamageSource.lightning`, `hitEntities`, `Set.addAll` e triggers de advancement de lightning | Não prova relação de cancelamento entre todos esses caminhos, ordem ou número de tentativas de dano |
| `SpellLightningBolt#canHitEntity(Entity)` e `#lambda$tick$0(Entity)` | No primeiro não há referência direta a `hitEntities`/`Set.contains`; a lambda separada referencia ambos | Não estabelece dedup global ou ausência de dedup em outros caminhos; a semântica da fonte é analisada abaixo |
| `SpellLightningBolt#setOwner/getOwner/getCause/powerLightningRod` | Métodos presentes com referências de resolução de owner e `LightningRodBlock.onLightningStrike` | Owner da entidade não substitui token de cast/proc nem prova chegada/ativação física |

## Leeching — causalidade localizada na fonte pública 3.1.1

1. [`LeechingSpell.SpellResult` L75–100][leech] escolhe um alvo e chama `hurt(lifeLeech(caster,caster),potency)`. A fonte [`lifeLeech`][life-source] usa `NoKnockBackDamageSource`; nesse produtor, entidade direta e causadora são o caster. `LIFE_LEECH` é distinto de `SOUL_LEECH` e não demonstra ganho de Soul Energy.
2. O consumidor antes não rastreado está em [`ModEvents.DamageEvent` L1198–1223][heal-consumer], evento **`LivingDamageEvent.Pre`**. Se o dano atual do evento é positivo, a fonte é `LIFE_LEECH` e a entidade causadora é Living, pede cura a essa entidade por **`getNewDamage() × (LeechingPercent / 100.0F)`**. A [config da fonte][percent] declara default **100**, faixa **1..100**; não é config implantada.
3. Esse consumer não exige localmente Player, Focus, staff, `rightStaff` ou root cast deste Focus. Também não tem guarda explícita de lado nesse ramo. O produtor server-typed e o contexto normal do dispatcher são fatos separados; não declarar uma superfície mutadora segura para todos os emissores de `LIFE_LEECH`.
4. A solicitação ocorre em **Pre**, antes das [reduções locais posteriores][later-reduction] do mesmo handler. O valor lido não é delta de HP final nem quantidade garantida depois de absorção/outros listeners. Alterar amount antes ou depois desse ponto pode produzir relações diferentes entre dano e cura pedidos; não compensar com outra cura numa bridge.
5. [`onLivingHeal` L1283–1288][heal-veto] cancela amount positivo quando o **receptor** tem `CURSED` ou seu último damage source satisfaz `hellfireAttacks`. O [helper][hellfire] é null-safe. Não há teste de Hex nessa condição. O caminho demonstra outra razão pela qual chamada a `heal` não comprova HP restaurado; o binário confirma referências correspondentes, sem homologar equivalência das condições.
6. No cast, [`hurt == true`][leech] permite o ramo de sucesso. **Weakness** ainda exige `rightStaff`, mas o **som** está fora desse teste interno de staff. A cura não é uma operação posterior nesse bloco: o consumer dela está no pipeline do dano. Não tratar a ordem do bloco de som/status como ordem do settlement da cura.

Como referência separada do host, a [API NeoForge 21.1.250][damage-pre] define Pre antes de mudanças de saúde/absorção; [Post][damage-post] vem após a mudança de saúde. Essa referência de source não é uma observação do pack. É necessário medir dano final, solicitação de cura e HP realmente restaurado separadamente.

## Lightning — correção do contrato de deduplicação na fonte 3.1.1

A [query ativa de impacto][bolt-impact] adiciona as entidades encontradas a `hitEntities`, mas o [`canHitEntity`][bolt-filter] dessa fonte **não consulta esse conjunto**. A consulta que usa `contains` pertence ao [ramo terminal de criteria][bolt-criteria]; `getHitEntities` também o expõe para relato. Portanto a frase anterior de que o conjunto “reduz repetições” não sustentava uma garantia de uma tentativa por vítima. Não converter essa correção em defeito físico confirmado ou em promessa de múltiplas perdas de HP.

`EventHooks.onEntityStruckByLightning` envolve o `thunderHit` correspondente; o caminho adicional de `LivingEntity.hurt` tem condições próprias e fica fora desse teste de retorno na fonte. O `GameEvent.LIGHTNING_STRIKE`, os triggers de advancement e o strike hook são superfícies diferentes. Cancelar um deles não demonstra supressão de todos os danos, modificações de cobre, fogo ou rod. Não usá-los como API de conclusão de cast nem como prova de interceptação pelo WorldEffectPolicy do Black Arcana.

## Perks, autoria e aceitação pendente

**Dano, cura solicitada, Weakness, cadência/custo, aquisição de alvo, volume de impacto e efeitos de mundo são eixos separados.** A identificação do consumer permite projetar testes, sem homologar setters/adapters. Conversão de DamageType para `LIFE_LEECH`, multialvo ou múltiplos relâmpagos pode reentrar em consumers existentes; manter **⛔ fail-closed** até provar ordem, autoria e dedup.

QA necessário: registrar cast/origem, entidade direta/causadora, damage Pre/Post, absorção/reduções, heal solicitado/aceito, CURSED/hellfire e demais vetos; dano negado, PvP/aliados/claims, duas pessoas conjurando, múltiplos ticks/bolts/vítimas, interrupção/custo/cooldown e ausência de segunda aplicação de Soul, dano ou cura. Para Lightning, medir separadamente strike hook, `thunderHit`, dano custom e alterações de mundo. **Nenhum desses casos físicos foi executado.**

`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. **+0 identidades/+0 certificados**; Goety permanece **0/361**, global observado **138/2075**, providers integrais **0/164**. O manifesto, os índices, runtime e Stage 06.05 permanecem inalterados. MFTE/RPG/Enshrouded não recebem novas integrações por esta auditoria.

[leech]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/magic/spells/necromancy/LeechingSpell.java#L75-L100
[life-source]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/ModDamageSource.java#L264-L266
[heal-consumer]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/events/ModEvents.java#L1198-L1223
[percent]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/config/SpellConfig.java#L853-L854
[later-reduction]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/events/ModEvents.java#L1224-L1258
[heal-veto]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/events/ModEvents.java#L1283-L1288
[hellfire]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/utils/ModDamageSource.java#L211-L213
[damage-pre]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/LivingDamageEvent.java#L34-L44
[damage-post]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/LivingDamageEvent.java#L86-L94
[bolt-impact]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/SpellLightningBolt.java#L226-L259
[bolt-filter]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/SpellLightningBolt.java#L348-L365
[bolt-criteria]: https://github.com/Vivideru/Goety-3/blob/6c41a04f2d712097c4461f969a6bb8ee277149ef/src/main/java/com/Polarice3/Goety/common/entities/projectiles/SpellLightningBolt.java#L188-L223
