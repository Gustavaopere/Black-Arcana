# Iron's 3.16.3 — Haste: alvo assistido, fallback self e quatro atributos

**Identidade:** `irons_spellbooks:haste` · Holy · níveis 1–4 · Iron's 1.21.1-3.16.3. ✅ identidade inventariada; 🟡 este dossiê causal é novo; ⚠️ análise da fonte exata, **não** prova binária nova nem GameTest; ⛔ redirecionamento de alvo/atributo por bridge não validada. **+0 novo spell.**

**Source pin:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`. [Descrição do provider](https://iron.wiki/spells/). Minecraft 1.21.1, modlist física NeoForge 21.1.250 vs baseline de build Black Arcana 21.1.248; a equivalência do JAR instalado segue pendente. Conteúdo técnico de clean-room.

## Dados de cast / routing

1. `HasteSpell` declara `HOLY_RESOURCE`, raridade mínima `EPIC`, máximo **4 níveis**, cooldown-default **80 s**, `CastType.LONG` e `castTime=30` ticks nominais. Constructor: `baseManaCost=50`, `manaCostPerLevel=10` → **50–80 mana**; `baseSpellPower=30`, `spellPowerPerLevel=5` → duração neutra **600–900 ticks = 30–45 s**. [Classe e defaults](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HasteSpell.java#L34-L68).
2. `checkPreCastConditions` chama `Utils.preCastTargetHelper` com **range 32**, margem `.35f`, `checkForBlocks(true)` pelo helper, `sendFailureMessage=false` e filtro `Utils.shouldHealEntity(caster,target)`. **Se o helper retorna false**, grava `TargetEntityCastData(caster)`, envia action bar somente para player e **retorna true**: erro de aquisição de alvo elegível converte o cast em self, não em falha. [Haste targeting](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HasteSpell.java#L80-L90), [raycast do helper](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L711).
3. `onCast` recupera `TargetEntityCastData`, resolve via `getTarget((ServerLevel)world)` e aplica `HASTENED` somente quando há `LivingEntity` resolvida. **Um sucesso de pré-cast não prova aplicação posterior**: target pode não estar resolvível no instante do efeito. Não transformar packet/sync/partículas em nova ativação. [Aplicação](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HasteSpell.java#L92-L110).
4. `Utils.shouldHealEntity` **não é sinônimo simples de amigo**: permite self; possui casos `ALWAYS_HEAL`, `isAlliedTo`, equipes e, para player sem equipe, retorna true para outro player; isso **não** prova consentimento, same-party ou política PvP. No helper, o ramo `PreventDismount` inspeciona o primeiro passenger sem executar literalmente `filter.test` naquele ramo: potencial exceção de filtro a ser testada, **não** bypass demonstrado no pack. [Critério de elegibilidade](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L532-L558), [ramificação](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L674-L693).

## Potência, atributos e duração

- `getAmplifier(level,caster)` retorna `(int)(7 * getEntityPowerMultiplier(caster))`: no multiplicador neutro, amplifier **7**, sem ganho automático por nível neste método. `getDuration(level,caster)` retorna `(int)(getSpellPower(level,caster)*20)`. São eixos distintos: **duração** vinculada a spell power e **amplifier** vinculado ao multiplicador da entidade. [Métodos](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/HasteSpell.java#L103-L110).
- `HastenedEffect.getPercentForAmplifier` retorna `(amplifier+1) * .025f`, ou **20%** no amplifier neutro 7. Esta função é usada no texto descritivo e a constante é consumida pelos attribute modifiers. [Efeito](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/HastenedEffect.java#L11-L26).
- `MobEffectRegistry.HASTENED` aplica `ADD_MULTIPLIED_TOTAL` com `0.025` por nível de amplifier nos atributos **MOVEMENT_SPEED**, **ATTACK_SPEED** e **CAST_TIME_REDUCTION**; para `IronsLibRegistries.AttributeRegistry.MINING_SPEED` usa **0.05** por nível (dobro). No amplifier neutro 7, os valores nominais de modifiers são **+20%** nos três primeiros e **+40%** em mineração, antes de composição com outros atributos/caps. [Registro versionado](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/registries/MobEffectRegistry.java#L51-L56).
- Raridade, mana, duração e cooldown são **defaults**; configurações, resistências, atributos e aplicação servidor-real podem divergir. A documentação player-facing resume `20% Magical Haste`, não especifica a composição efetiva de todos esses atributos.

## Superfícies de perk / deduplicação

| Eixo | Superfície comprovada | Tratamento |
|---|---|---|
| Cast time próprio | `castTime=30` e CastType LONG | **A condicionado**, não alterar via segundo input pipeline |
| Duração | `getSpellPower * 20` | **A:** potência nativa; garantir limites e não somar um segundo effect |
| Haste %, ataque e movimento | `HASTENED` / atributos | **A:** modifiers nativos, nunca duplicar via RPG; effect/modifier API para mutação custom **não verificada** |
| Mineração | `MINING_SPEED` com dobro da fração | **A:** eixo distinto, não assumir 20% |
| Range / target type | `preCastTargetHelper(32,.35f)` + self fallback | **C/⛔:** código do provider não expõe aqui extensão segura de range, AoE ou alvo inimigo |
| Causalidade / Mastery | 1 cast → 0 ou 1 alvo efetivamente resolvido → buff temporário | **D/⛔:** não premiar a intenção de pré-cast sem cast aceito e efeito observado conforme regra de Mastery |

**Ponto de atenção:** `checkPreCastConditions` retorna true também depois do fallback self. Eventos de targeting, partículas, ticks de efeito e modificações contínuas de atributos não correspondem a casts adicionais. Não abrir second mana/cooldown owner e não atribuir autoria de buff ao RPG sem provenance do provider.

## QA pendente

- [ ] Verificar classfiles do JAR instalado e o `TargetEntityCastData` real no NeoForge 21.1.250.
- [ ] Cast sem alvo, player sem equipe, membro de equipe, summon, boss, `PreventDismount`/passenger, alvo desaparecido entre pre-cast e onCast, bloqueio LOS.
- [ ] Medir duração/multiplicadores/atributos em server; relog, reaplicação/remoção, caps e sobreposição com perks do RPG.
- [ ] Confirmar custo e cooldown reais; não liberar perk de área/range/filtro ou XP automático sem boundary estável + validação.

**Estado:** source-pinned ✅, classfile e live modpack ⚠️, extensão de targeting ⛔; Stage 06.05 🟡 sem alteração de runtime.
