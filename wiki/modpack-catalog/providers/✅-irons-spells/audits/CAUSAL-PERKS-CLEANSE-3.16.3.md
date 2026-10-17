# Iron's 3.16.3 — Cleanse: seleção cúbica de aliados e remoção de status

**Identidade:** `irons_spellbooks:cleanse` · escola Holy · nível único · Minecraft 1.21.1 / Iron's Spells 'n Spellbooks `1.21.1-3.16.3`. ✅ identidade já catalogada (uma das 110); 🟡 ficha causal individual suplementar; ⚠️ source pin conferido, JAR instalado e execução física NÃO VERIFICADOS nesta tranche; ⛔ perk de alcance, forma de área, categoria de efeitos e progressão por remoção sem seam/causalidade comprovados. **+0 identidades novas.**

**Proveniência e isolamento:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`; [catálogo oficial de descrição](https://iron.wiki/spells/). Documento original de interoperabilidade/clean-room, **não** implementação copiada. A modlist certificada registra NeoForge **21.1.250**; o projeto Black Arcana usa baseline de build NeoForge **21.1.248**. A diferença não demonstra incompatibilidade, mas impede substituir fingerprint físico por build de desenvolvimento.

## Cast, defaults e prévia

1. `CleanseSpell` registra `cleanse`, Holy, raridade mínima **EPIC**, `maxLevel=1`, cooldown **60 s**. Constructor: `baseManaCost=100`, `manaCostPerLevel=0`, `baseSpellPower=0`, `spellPowerPerLevel=0`, `castTime=60` ticks e `CastType.LONG`. Valores são *defaults*, não prova de custo/tempo após configs, modifiers e requisitos em servidor. [Fonte: IDs e defaults](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/CleanseSpell.java#L29-L67).
2. `checkPreCastConditions` cria `TargetedAreaEntity` na **posição do caster**, raio visual **3**, cor de targeting; registra `TargetAreaCastData` e retorna `true`. Não há raycast de bloco ou alvo remoto neste método. A entidade de prévia acompanha owner e possui lifecycle independente da resolução do efeito; **preview não é cast adicional nem confirmação de cura**. [Pré-cast](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/CleanseSpell.java#L74-L80), [previsão/owner/tick](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/entity/spells/target_area/TargetedAreaEntity.java#L68-L105).
3. O texto de apresentação informa `radius=3`, porém `onCast` chama `level.getEntitiesOfClass(LivingEntity.class, AABB.ofSize(entity.getBoundingBox().getCenter(),6,6,6))`, **sem teste adicional** `distanceTo<=3`. Resultado do código: broad phase **caixa 6×6×6**, não esfera de raio 3; a interseção de bounding boxes da entidade afeta a elegibilidade na borda. Isso deve ser medido, não corrigido por inferência no provider. [Fórmula de apresentação e seleção](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/CleanseSpell.java#L32-L36), [seleção efetiva](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/CleanseSpell.java#L82-L94).

## Effect resolution e filtros

- Para cada living selecionado na AABB, a magia exige `Utils.shouldHealEntity(caster,target)`. O helper inclui self, `ALWAYS_HEAL`, equipes e regras de player sem equipe; **não** corresponde automaticamente a squad, friendly-fire consent, regiões/claims ou PvP do modpack. O caster pode estar entre os alvos enumerados, mas a presença real depende do resultado da busca. [Filtros de aliados](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L532-L558).
- Para alvos elegíveis, consulta `getActiveEffects()` e seleciona `MobEffectCategory.HARMFUL` **desde que** o Holder do efeito **não** possua tag `ModTags.CLEANSE_IMMUNE`; chama `livingEntity.removeEffect` para cada Holder selecionado. A tag do provider existe com namespace `irons_spellbooks:cleanse_immune`. Não remove por esta seleção buffs benéficos/neutros, nem efeitos nocivos tagged immune. [Algoritmo](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/CleanseSpell.java#L84-L90), [tag](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/util/ModTags.java#L40-L48).
- Ainda no alvo elegível, `MagicManager.spawnParticles` gera **15 partículas** de `CLEANSE_PARTICLE` por chamada, independentemente de o alvo possuir efeito nocivo removível. Um efeito candidato não implica remoção bem-sucedida; a função `removeEffect` não tem seu resultado inspecionado no loop. Som, animação e FX **não** fornecem eventos estáveis de Mastery. [Seleção, efeitos e partículas](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/CleanseSpell.java#L83-L103).
- **Sem dano direto, cura de HP, projétil ou DoT neste callsite.** Não registrar `SpellHealEvent` nem HP útil curado como consequência provada deste método. Qualquer listener externo acionado por `removeEffect` exige nova observação específica. [Código de conclusão](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/CleanseSpell.java#L82-L94).

## Parâmetros para perks e limites

| Eixo | Superfície real de código | Classificação de extensão |
|---|---|---|
| Cast/cooldown/custo | `AbstractSpell` + defaults (60 ticks, 60 s, mana 100) | **A condicionado:** provider owns recurso e tempo, sem second pipeline |
| Range/forma | `AABB.ofSize(...,6,6,6)` no método | **D/⛔:** raio visual 3 não é hook mutável; +range requer alterar seleção provider-owned |
| Eligibility | `Utils.shouldHealEntity` | **C/⛔:** equipes e elegibilidade pertencem ao provider; nunca ampliar by-passando claims |
| Tipo de status | `MobEffectCategory.HARMFUL` e `CLEANSE_IMMUNE` | **C:** exceção por tag nativa do provider; integração de datapack tag não prova autorização de perk dinâmica |
| Quantidade de alvos | `getEntitiesOfClass` em AABB, sem cap local | **D/⛔:** +área tem custo dependente da densidade; exigir target/work budgets |
| Mastery | um cast pode remover vários efeitos de vários alvos | **D/⛔:** não creditar uma conjuração por effect removido ou partícula; validar cast aceito e remoções concretas |
| Overlap com outros sistemas | removals disparam lifecycle nativo dos efeitos | **C:** testar Heartstop, debuffs de terceiros, removal callbacks, interações perigosas; sem chamar cleanse um dispel universal |

**Causalidade:** intenção de cast → seleção AABB → filtro `shouldHealEntity` → coleta de holders HARMFUL fora de immune-tag → tentativas de `removeEffect` → FX por alvo. Quantidades de status selecionados e status efetivamente removidos **não são equivalentes** sem observação de antes/depois. Um listener externo não deve conceder XP por status em cascata, nem duplicar efeitos de cleanup.

## QA pendente

- [ ] Confrontar JAR instalado / metadata / SHA e métodos `CleanseSpell`, `Utils.shouldHealEntity`, `TargetedAreaEntity`, `ModTags`.
- [ ] Testar entidades a (2.9,0,0), (2.9,0,2.9) e fora da AABB, variando bounding boxes, altura, LOS, wall/claims e equipes; provar caixa versus tooltip raio.
- [ ] Casos HARMFUL removível, immune-tag, effect benéfico, alvo sem debuff, 0/muitos alvos, buff de summon; confirmar callback onRemoval (incluindo Heartstop) antes de autorizar perk de dispel.
- [ ] Validar cast/cooldown, proteção PvP, timing e custo do servidor físico NeoForge 21.1.250 e cliente modpack, comportamento após relog, ausência de contagem dupla em Mastery.

**Estado:** `SOURCE_CAUSALITY` ✅ documental · `EXACT_BINARY` ⚠️ pendente nesta tranche · `PHYSICAL_QA` PENDING · alteração externa de geometria/seleção ⛔. Stage 06.05 🟡; Stage 09 responsável por observações físicas obrigatórias.
