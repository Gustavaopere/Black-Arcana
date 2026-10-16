# Iron's 3.16.3 — Blessing of Life: aquisição de entidade sem filtro ally e cura proposta

**ID:** `irons_spellbooks:blessing_of_life` · Holy · 1–10 níveis · `irons_spellbooks` · ✅ inventariada; 🟡 aprofundamento causal individual desta tranche; ⚠️ source fixado, sem JAR físico ou GameTest; ⛔ mudança de target-type, alcance e Mastery por cura sem validação causal. **+0 magias.**

**Proveniência:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` · fonte para interoperabilidade clean-room; [descrições do provider](https://iron.wiki/spells/). Modlist física: `irons_spellbooks-1.21.1-3.16.3.jar`, NeoForge 21.1.250; build Black Arcana: NeoForge 21.1.248. Equivalência do JAR instalado, runtime transformado e GameTest **NÃO VERIFICADOS nesta tranche**.

## Cast, targeting e identidade do alvo

1. `BlessingOfLifeSpell` registra Holy, rarity mínima COMMON, maxLevel **10**, cooldown **10 s**, CastType LONG, `castTime=30` ticks. `baseManaCost=10`, `manaCostPerLevel=5` → **10–55 mana**; `baseSpellPower=6`, `spellPowerPerLevel=1` → cura nominal **6–15** antes de atributo/config e HP faltante. [Identidade/defaults](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/BlessingOfLifeSpell.java#L30-L68).
2. `checkPreCastConditions` retorna diretamente `Utils.preCastTargetHelper(level,caster,magicData,this,64,.35f)`. O helper de **64 blocos** usa raycast com `checkForBlocks(true)`, bounding box inflation `0.35`, e, nesta sobrecarga, `filter = x -> true`: **não** invoca `Utils.shouldHealEntity` nem impõe ally/team neste ponto. O método exige encontrar `LivingEntity` resolvível para completar o pré-cast (salvo branch `PreventDismount`), mas não garante que seja aliado. Assim, escolher uma criatura hostil é **permitido pela filtragem deste helper**, sem afirmar cura hostil realmente observada in-game. [Chamador](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/BlessingOfLifeSpell.java#L71-L74), [helper/filter](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L711).
3. Existe um método privado `findTarget(LivingEntity)` que usa raycast com range **32**, mas **não é chamado** por `checkPreCastConditions` nem `onCast` nesta classe. Portanto **32 não deve substituir o range operacional source-pinned de 64** sem verificar invocação externa/binary. [Método inativo no fluxo apresentado](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/BlessingOfLifeSpell.java#L91-L103).

## Aplicação e deduplicação de cura

- Em `onCast`, se `playerMagicData.getAdditionalCastData()` for `TargetEntityCastData` e `getTarget((ServerLevel)world)` não for nulo, calcula `healAmount = getSpellPower(spellLevel,caster)`, publica `new SpellHealEvent(caster,target,healAmount,getSchoolType())` em `NeoForge.EVENT_BUS`, então chama `target.heal(healAmount)` e envia `HealParticlesPacket`. Não há segunda verificação de ally nesta função. `super.onCast` é chamado mesmo sem alvo resolvido. **Identidade de cast admitido, evento postado e HP efetivamente restaurado são etapas distintas.** [Callsite](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/BlessingOfLifeSpell.java#L76-L89).
- `SpellHealEvent` mantém `targetEntity`, `healAmount` e escola, com getters; não declara um setter de quantidade nem cancelabilidade na classe. O comentário Java inclui nomenclatura histórica de Forge que não altera o callsite em `NeoForge.EVENT_BUS`. `SpellHealEvent.getHealAmount()` é **quantidade pretendida**, não comprovação de HP líquido; `LivingHealEvent`/Blight/outros listeners ainda podem modificar cura posterior. [Contrato do evento](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/events/SpellHealEvent.java#L18-L40), [aplicação posterior](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/BlessingOfLifeSpell.java#L79-L85).
- Quando a entidade desaparece entre targeting e resolução, esta função pode não executar heal/event/FX, apesar de uma solicitação válida ter existido. Deduplicação de Mastery por **cast raiz** vs **cura útil** precisa especificação de qual métrica se quer premiar, além de token/owner/time causal; simplesmente somar `SpellHealEvent` e `LivingHealEvent` duplica a mesma tentativa. [Resolução condicional](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/BlessingOfLifeSpell.java#L77-L88).
- Não há projétil, area, knockback ou tipo de dano neste método. O alvo é uma entidade, não bloco; range de aquisição **64** difere do delta de vida efetivamente recuperado (0 a 15 nominal por cast, sujeito a HP faltante e eventos). VFX `HealParticlesPacket` não adiciona magia e não prova efeito positivo.

## Matriz de perks e autoridade

| Eixo | Evidência 3.16.3 | Classificação |
|---|---|---|
| Mana/cooldown/channel | 10–55 / 10 s / 30 ticks | **A condicionado:** Iron's authority; não criar débito paralelo |
| Alcance e mira | `preCastTargetHelper(64,.35)`, raycast com block LOS | **C/⛔:** sem mutabilidade per-player/perk demonstrada |
| Tipo e elegibilidade | `TargetEntityCastData`; overload sem filtro ally | **C/⛔:** não substituir com política do RPG presumida; política PvP/claims/hostile precisa QA |
| Cura nominal | `getSpellPower` Holy 6–15 neutro | **A condicionado:** stats nativos, não evento de alteração de heal |
| Hook observável | `SpellHealEvent` pré-`LivingEntity.heal` | **B para observação estrutural**, não setter/métricas pós-cura comprovadas |
| Desaparecimento/invalidade do alvo | `getTarget(ServerLevel)==null` → sem `heal` | **C:** revalidar sincronização temporal e token de cast |
| Mastery | um cast aceito pode gerar 0/1 evento de cura e 0–N HP úteis | **D/⛔:** sem aprovação de HP e dedup não remunerar duas vezes por eventos |

**Cuidado de integração:** buffs de cura e perk `+healing` precisam estabelecer se a alteração ocorre em spell power nativo, pós-evento NeoForge ou heal aceito. A interface do `SpellHealEvent` aqui não prova setter de `healAmount`. Nunca atribuir heal a um caster desaparecido ou a outro mod sem correlação, nem forçar alvo hostil/aliado pela UI.

## QA físico pendente

- [ ] Confirmar JAR físico, NeoForge 21.1.250, `preCastTargetHelper(64,.35)` e comportamento real de `findTarget(32)` inativo neste fluxo.
- [ ] Testar undead/hostile, aliados, player sem equipe, player com equipe, PvP, claims, LOS e o ramo `PreventDismount`/passenger. Verificar se target hostil pode receber HP e como isso interage com normas do servidor.
- [ ] Comparar `SpellHealEvent`, `LivingHealEvent`, HP antes/depois para pleno/deficit parcial/Blight, event cancels e alvo removido durante LONG channel; custo/cooldown.
- [ ] Dedicated server, relog, interrupção de cast, modifier de Holy, Mastery unica por cast e anti-duplicação de XP.

**Estado:** source causal ✅; prova de classe exata no JAR local ⚠️; client/servidor físico PENDING; edição de target/alcance/HP útil por perk ⛔. Stage 06.05 🟡, sem implementação.
