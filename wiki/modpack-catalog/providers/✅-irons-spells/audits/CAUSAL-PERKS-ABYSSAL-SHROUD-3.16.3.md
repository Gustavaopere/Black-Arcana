# Iron's 3.16.3 — Abyssal Shroud: mitigação defensiva e deslocamento reativo

**Estado:** ✅ `SOURCE-PINNED / CAUSAL-PARTIAL`; ⚠️ artefato JAR/config exatos, runtime real, per-attack dedup e hooks do RPG **não verificados**. Spell `irons_spellbooks:abyssal_shroud` já contabilizada nas 110 identidades; nenhuma magia nova. MC 1.21.1 / Iron's 3.16.3, código `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`. [Ficha pré-existente](../eldritch/abyssal-shroud.md).

## Pipeline causal

1. **Casting:** [`AbyssalShroudSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/eldritch/AbyssalShroudSpell.java#L23-L58) é Eldritch, `LEGENDARY`, níveis 1–3, tipo `INSTANT`/0 ticks, mana `300+20×(level−1)`, cooldown default **200 s**, `baseSpellPower=6`, `spellPowerPerLevel=6`. O `onCast` aplica **a si próprio** `MobEffectRegistry.ABYSSAL_SHROUD`, sem atingir inimigos diretamente; amplifier 0, `ambient=false`, `visible=false`, `showIcon=true`. [`onCast`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/eldritch/AbyssalShroudSpell.java#L71-L75).
2. **Duração precisa:** `new MobEffectInstance(...,(int)getSpellPower(level,caster)*20,0,...)` converte `power` para `int` **antes** de multiplicar por 20. A linha de tooltip usa `getSpellPower×20` sem a mesma truncagem intermediária. **Com defaults unitários**, níveis 1/2/3 = poderes 6/12/18 ⇒ nominalmente **6/12/18 segundos**, mas atributos fracionários/config podem produzir discrepância entre tooltip e duração real. Não confundir duração com probabilidade de evasão.
3. **Gatilho de evasão:** [`ServerPlayerEvents.onLivingIncomingDamage`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/player/ServerPlayerEvents.java#L448-L475) processa o efeito para vítimas que são `ServerPlayer` **ou** `IMagicEntity`; `FIREWARD_RING` tem guarda anterior, e `EVASION` tem precedência **`if ... else if`** sobre `ABYSSAL_SHROUD`. Quando `AbyssalShroudEffect.doEffect` retorna true, o listener cancela `LivingIncomingDamageEvent`. **Não** conclua eficácia geral para todo `LivingEntity` que possua o efeito.
4. **Bloqueios explícitos:** [`AbyssalShroudEffect.doEffect`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/AbyssalShroudEffect.java#L29-L33) retorna false no client e se o dano tiver tags `DamageTypeTagGenerator.BYPASS_EVASION`, `DamageTypeTags.IS_FALL` ou `DamageTypeTags.BYPASSES_INVULNERABILITY`. Não catalogar evasão como imunidade a todos os tipos de dano; o conteúdo e o alcance da tag custom `BYPASS_EVASION` dependem de datapack/registro real.
5. **Deslocamento lateral:** `doEffect` tenta calcular nova posição lateral, procura chão, mede AABB baseada em `entity.getDimensions(pose)`, chama `level.findFreePosition`, recua ao ponto original quando a posição sufocaria, desmonta passenger se necessário e **teleporta apenas quando o bloco abaixo do destino não é ar**. [`AbyssalShroudEffect`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/AbyssalShroudEffect.java#L37-L61). Nem a direção final nem a distância útil real têm garantia numérica até teste espacial.
6. **Crítica de causalidade:** `doEffect` retorna `true` **mesmo se o ramo condicional não executar `entity.teleportTo`**, desde que as condições de bloqueio iniciais não tenham retornado false. Assim, o evento de dano **pode ser cancelado sem deslocamento efetivo**. O código também chama `sideStep.yRot(livingEntity.getYRot())` sem reatribuir o retorno. Como `Vec3` é classe de valores, esse trecho é uma **suspeita de rotação não aplicada**, a verificar em bytecode/gameplay; não publicar correção ou comportamento espacial sem teste. [`AbyssalShroudEffect`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/AbyssalShroudEffect.java#L37-L67).
7. **Projéteis:** [`ServerPlayerEvents.onProjectileImpact`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/player/ServerPlayerEvents.java#L546-L562) também inspeciona impacto em `Player`/`IMagicEntity`, verifica `EVASION` primeiro e, alternativamente, `ABYSSAL_SHROUD`; constrói source `indirectMagic` e cancela `ProjectileImpactEvent` caso `doEffect` retorne true. Uma única tentativa de ataque pode cruzar camadas evento-de-projétil **e** evento-de-dano; é necessário provar ordem e deduplicação na execução real antes de gerar procs defensivos.
8. **Não é o mesmo seam de Teleport Spell:** este `doEffect` usa `livingEntity.teleportTo` **diretamente**, não `Utils.handleSpellTeleport`. Assim, a existência de [`SpellTeleportEvent` usado por TeleportSpell](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L167-L175) **não comprova interceptação** deste deslocamento reativo via aquele evento. Não prometer perk de redirect usando `SpellTeleportEvent` como universal.
9. **Counterspell:** `AbyssalShroudEffect extends MagicMobEffect`; no caminho em que Counterspell seleciona um `LivingEntity` e não é vetado, seu filtro de remoção por `instanceof MagicMobEffect` **inclui** este efeito. [`CounterspellSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java#L99-L107). Isso não demonstra que todos os providers consigam removê-lo.

## Matriz de mutabilidade

| Eixo | Mecanismo real | Boundary e estado |
|---|---|---|
| Duração | `(int)power ×20`, efeito no caster | ⚠️ modificação indireta por atributos/power; ⛔ sem setter per-spell estável observado |
| Probabilidade / resistência | condicional por tags + tipo de entidade + `doEffect` | ⛔ sem parâmetro probabilidade/perk identificado; não inventar chance de dodge |
| Intervalo de reativação | os dois listeners podem processar hits sucessivos | ⛔ nenhum internal cooldown desta classe comprovado; não anunciar cooldown de evasão nem procs sem dedup |
| Direção/distância | deslocamento lateral + `findFreePosition`/AABB | ⛔ sem hook de alcance/direção externo; `SpellTeleportEvent` não é evidência para esse trecho |
| Tipo de dano ignorado | bypass custom / queda / invulnerabilidade | ⚠️ custom tag precisa verificação; não contornar bypass do provider |
| Tipo de alvo | self `LivingEntity` ao cast, com listener específico | ⛔ sem aplicação global a pets/summons/habilidades do Black Arcana |
| Custos | 300/320/340 mana; 200 s default | ⚠️ provider-owned e dependentes de config; `SpellOnCastEvent` pós-gate |
| Dispel | `MagicMobEffect` | ⚠️ comprovado filtro de Counterspell, sem QA em multiplayer |

## Testes necessários

- [ ] Equivalência de JAR + config, damage-type tags e `MobEffectRegistry` carregados.
- [ ] Dano normal, fall damage, `BYPASS_EVASION`, `BYPASSES_INVULNERABILITY`, área e projetil com tags.
- [ ] Vítimas ServerPlayer, IMagicEntity e outras LivingEntity; coexistência `EVASION`+`ABYSSAL_SHROUD`.
- [ ] Ataque gerando ambos os eventos e um só crédito/proc/custo de evasão.
- [ ] Destinos com chão, em ar/água, parede, chunk não carregado, mounts, colisão, rota lateral e claims.
- [ ] Verificar hipótese de `Vec3.yRot` não aplicada, cancelamento sem teleporte e VFX/som.
- [ ] Dispel por Counterspell, reaplicação, save/restart, cast original e custos cooldown em cliente dedicado.
- [ ] Contrato real do RPG Skill Tree; não criar segunda imunidade/backlash sobre efeito provider-owned.

**Clean-room:** somente auditoria dos caminhos observados e critérios de teste, não redistribuição do código/arquivos do provider.
