# ASUtils — leitura de spells, desbloqueio e parâmetros auxiliares

**Classe:** `net.acetheeldritchking.aces_spell_utils.utils.ASUtils` · **Tipo:** helpers públicos do provider, não `AbstractSpell` nem mutating hook estável comprovado. **Estado:** ⚠️ source-pinned.

## Contratos Java observados

| API do source | Comportamento exato relevante | Limitação para perks |
|---|---|---|
| `hasCurio(Player, Item)` | Procura um Curio equipado via `CuriosApi.getCuriosHelper().findEquippedCurio` | Não inventar slot nem política de equip |
| `isLongAnimCast(AbstractSpell)` / `isContAnimCast(AbstractSpell)` | Compara `spell.getCastType()` com `LONG` ou `CONTINUOUS` | Tipo não equivale a duração ou cast bem-sucedido |
| `getSpellsFromTag(TagKey<AbstractSpell>)` | Percorre `SpellRegistry.getEnabledSpells()`, consulta holder do registry do Iron's e filtra `holder.is(tag)` | Não lista spells desabilitados nem define quem pode usá-los |
| `isValidUnlockItemInInventory(Item, Player)` | Busca identidade exata do `Item` no inventário e retorna boolean | Não desbloqueia spell por si |
| `isValidConsumableUnlockItemInInventory(Item, Player)` | Busca identidade do item; chama `ItemStack.shrink(1)` no primeiro encontrado e retorna boolean | **Mutação imediata**, sem transação/side-check visível no helper; não chamar só para consultar elegibilidade |
| `getDamageForAttributes(..., attr1[, attr2[, attr3]], modifier)` | `modifier * (spell.getSpellPower(spellLevel, entity) + soma(entity.getAttributeValue(attrN)))` | Calcula valor de conveniência, **não** dano final liquidado; risco de dupla aplicação |
| `spawnParticlesInCircle` / `spawnParticlesInRing` | Envia `count` partículas em uma circunferência, ou `3*count` em três anéis, usando `MagicManager.spawnParticles` | Geometria **visual**, sem AOE/hit ou range confirmado |
| `isUnderTheSun(Level, LivingEntity)` | Exige dia, lado não cliente, luz > 0.5, céu visível e exclusão de água/chuva/bolhas/neve | Predicado ambiental, não condição canônica de cast |
| `isBossEntity(EntityType)` | Testa tag `BOSS_LIKE_ENTITES` do provider | Tag não é diagnóstico genérico de boss |
| `basicDamageCap(amount,min,max)` | `Mth.clamp` | Não assume caps de dano aplicados automaticamente |

## Parâmetros auxiliares e condições de chamada

`spawnParticlesInCircle(count,radius,yHeight,particleSpeed,entity,particle)` usa centro `entity.position()`, plano X/Z e Y=`entity.Y+yHeight`; cada chamada pede uma partícula com deltas zero e force=false. `spawnParticlesInRing` repete isso para três raios independentes. O ângulo vem de **`Math.toRadians(360/count)*i` com divisão inteira**: counts que não dividem 360 produzem espaçamento truncado e count>360 produz ângulo zero em todas as amostras. Count≤0 não entra nos loops. Não há clamp local de count/radius/speed nem budget total; corrigir ou validar no consumidor antes de prometer circunferência uniforme ou custo máximo.

As buscas de unlock percorrem `player.getInventory().getContainerSize()` por identidade `== Item`, sem consultar Curios nem tag/NBT. A variante consumível reduz o primeiro stack correspondente e retorna imediatamente, sem grant/rollback de desbloqueio. `getEyeHeight` retorna Y mundial + eyeHeight − **0.2**; `getChunkPos` usa X/Z `>>4`; `convertTicksToTime` usa ticks/20 inteiro e formata `mm:ss`. O nome público é **`rbgToVector3F`** (grafia do source): divide r/g/b por **255F**, sem clamp 0..255. Nenhum desses métodos muda geometria ou recurso de uma spell.

## Ausências deliberadas

O helper não fornece API segura verificada para modificar distância, alvo, raio real, tempo/cooldown, mana ou tamanho de projétil de spells Iron's. `getEyeHeight`, `getChunkPos`, `convertTicksToTime`, `rainbowName` e o tooltip de casting existem como utilidades mas não são hooks autoritativos de perks. O último usa `ClientMagicData` e dados do jogador local — apresentação cliente.

**Fonte exata:** [`utils/ASUtils.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ASUtils.java). Cuidado especial: `shrink(1)` deve ser protegido por transação/side do chamador; não reutilizar esse método como validação read-only.

**Proveniência:** AceTheEldritchKing/Aces_Spell_Utils @ `a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, source `1.2.7.2-1.21.1`. O catálogo físico referencia `aces_spell_utils-1.2.7.2-1.21.1.jar`, sem prova independente de paridade classfile. Build desta revisão usa Iron's `3.16.2`, versus pack `3.16.3`.

**Gate:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não gera spell registrado, proc, atributo, perk ou adapter novo. Black Arcana preserva seu runtime mágico; Iron's controla casting/mana/cooldown dos seus spells; RPG Skill Tree controla progressão somente via contrato real.
