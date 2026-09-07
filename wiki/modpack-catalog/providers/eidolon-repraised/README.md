# Eidolon: Repraised

## Estado canônico

- mod id: `eidolon_repraised`
- JAR instalado: `eidolon_repraised-1.21.1-0.5.0.2.jar`
- versão instalada: `0.5.0.2`
- Minecraft: `1.21.1`
- loader: NeoForge
- source oficial: `Alexthw46/Eidolon-Repraised`
- source pin exato da versão: `696a47333e43970be7f697790eac0af76b6a04b8`
- estado: **SOURCE-PINNED 0.5.0.2 / SPELL REGISTRY 20/20 INVENTARIADO / SEMÂNTICA PRINCIPAL AUDITADA / RITUAIS E DATA-DRIVEN CHANTS AINDA EM EXPANSÃO / RUNTIME QA PENDENTE**

O commit acima é o commit que altera `mod_version` para `0.5.0.2`; o head atual da branch 1.21.1 já está em 0.5.0.3 e não é usado como autoridade para esta auditoria.

Eidolon não deve ser modelado como um simples addon de spells. Na versão instalada ele expõe, de forma provider-native:

- capability própria de mana;
- capability de reputação/devotion por divindade;
- capability de soul;
- research/knowledge;
- um sistema de `Sign`/`SignSequence` para chants;
- `SpellCastEvent.Pre` cancelável e `SpellCastEvent.Post`;
- spells estáticos configuráveis por custo e delay;
- prayers ligadas a altar/effigy, reputação e cooldown;
- recipes data-driven de chant/command chant e conversões;
- rituais, sacrifícios e progressão teúrgica separados do spell registry.

Isso faz de Eidolon um provider de **mana + theurgy/devotion + soul + research + ritual + chant**, com autoridade própria sobre custo, gates e settlement.

## Sign registry

A build 0.5.0.2 registra 11 signs:

| Sign | ID |
|---|---|
| Wicked | `eidolon_repraised:wicked` |
| Sacred | `eidolon_repraised:sacred` |
| Blood | `eidolon_repraised:blood` |
| Soul | `eidolon_repraised:soul` |
| Mind | `eidolon_repraised:mind` |
| Flame | `eidolon_repraised:flame` |
| Winter | `eidolon_repraised:winter` |
| Harmony | `eidolon_repraised:harmony` |
| Death | `eidolon_repraised:death` |
| Warding | `eidolon_repraised:warding` |
| Magic | `eidolon_repraised:magic` |

A sequência de signs faz parte da identidade runtime do spell. Black Arcana não deve reinterpretar a combinação de signs como uma escola própria nem duplicar a resolução do provider.

## Spell registry 20/20

`Spells.init()` registra exatamente 20 entradas provider-native na versão 0.5.0.2:

| # | Spell / chant | ID canônico | Signs | Classe / função principal |
|---:|---|---|---|---|
| 1 | Dark Prayer | `eidolon_repraised:dark_prayer` | Wicked ×3 | Prayer / devoção Dark |
| 2 | Darklight Chant | `eidolon_repraised:darklight_chant` | Wicked, Flame, Wicked, Flame | Ghost light alinhada a Dark / Glowing |
| 3 | Dark Animal Sacrifice | `eidolon_repraised:dark_animal_sacrifice` | Wicked, Blood, Wicked | Sacrifício animal / reputação Dark |
| 4 | Dark Touch | `eidolon_repraised:dark_touch` | Wicked, Soul, Wicked, Soul | Conversão dark ou `NECROTIC` em equipamento |
| 5 | Frost Touch | `eidolon_repraised:frost_touch` | Wicked, Winter, Blood, Winter, Wicked | Congela water source / aplica Chilled |
| 6 | Dark Villager Sacrifice | `eidolon_repraised:dark_villager_sacrifice` | Blood, Wicked, Blood, Soul | Sacrifício de aldeão / reputação Dark |
| 7 | Zombify Villager | `eidolon_repraised:zombify_villager` | Death, Blood, Wicked, Death, Soul, Blood | Conversão para zombie villager |
| 8 | Enthrall Undead | `eidolon_repraised:enthrall_spell` | Wicked, Mind, Magic, Magic, Mind | Thrall/control de undead |
| 9 | Light Prayer | `eidolon_repraised:light_prayer` | Sacred ×3 | Prayer / devoção Light |
| 10 | Fire Chant | `eidolon_repraised:fire_chant` | Flame ×3 | Acende blocos/burners ou incendeia entidade |
| 11 | Light Chant | `eidolon_repraised:light_chant` | Sacred, Flame, Sacred, Flame | Ghost light alinhada a Light / Glowing |
| 12 | Holy Touch | `eidolon_repraised:holy_touch` | Sacred, Soul, Sacred, Soul | Conversão light ou `CONSECRATED` em equipamento |
| 13 | Lay on Hands | `eidolon_repraised:lay_on_hands` | Flame, Soul, Sacred, Soul, Sacred | Cura + limpeza de efeitos curáveis por leite |
| 14 | Cure Zombie | `eidolon_repraised:cure_zombie` | Sacred, Soul, Mind, Harmony, Flame, Soul | Cura/conversão de zombie villager |
| 15 | Smite Chant | `eidolon_repraised:smite_chant` | Flame, Magic, Sacred, Death, Magic, Sacred | Dano mágico + Weakness contra undead |
| 16 | Sunder Armor | `eidolon_repraised:sunder_armor` | Flame, Magic, Wicked, Magic, Flame | Aplica Vulnerable |
| 17 | Reinforce Armor | `eidolon_repraised:reinforce_armor` | Sacred, Warding, Sacred, Warding, Sacred | Buff/consagração defensiva de armadura |
| 18 | Create Water | `eidolon_repraised:create_water` | Winter, Winter, Flame, Flame | Criação/manipulação de água |
| 19 | Undead Lure | `eidolon_repraised:undead_lure` | Mind, Magic, Wicked | Atração/controle de undead |
| 20 | Basic Incense | `eidolon_repraised:basic_incense` | sem sequência fixa no registro | PrayerSpell dummy usada pelo sistema de incense |

### Observação sobre `basic_incense`

O próprio source marca `CENSER` como `// dummy`. Ele é um `PrayerSpell` registrado sem sign sequence fixa. Portanto ele pertence ao spell registry técnico, mas **não deve ser apresentado ao jogador como um chant convencional** sem validação da superfície de gameplay do incense.

## Custos, delay e autoridade de cast

`StaticSpell` define:

- `cost` por spell, sobreponível por config server;<br>
- `delay` em ticks, também configurável por spell;<br>
- gate de mana antes do cast;<br>
- `SpellCastEvent.Pre` cancelável;<br>
- `SpellCastEvent.Post` após o efeito.

Quando `getCost() > 0`, o cast falha para jogador não criativo se a capability de mana do Eidolon estiver abaixo do custo. O provider é a autoridade de custo e do momento de settlement. Black Arcana deve observar o cast causal já validado e **não debitar mana novamente**.

O delay default de `StaticSpell` é 10 ticks salvo override. `FireTouchSpell`, por exemplo, usa delay base 5 ticks.

## Spells com semântica e números verificados

### Lay on Hands — `lay_on_hands`

- custo base: **15 mana**;
- alvo: LivingEntity não-undead sob ray trace; fallback para o próprio caster;
- cura base: **5**;
- scaling: `+ 0.05 × reputação Light`;
- remove efeitos não benéficos curáveis por `EffectCures.MILK`;
- ao curar outra entidade que estava abaixo da vida máxima, concede research `HEAL_VILLAGER` e **+3 reputação Light** por default;
- todos esses parâmetros de cura/reputação possuem config server.

### Fire Chant — `fire_chant`

- custo base: **10 mana**;
- delay base: **5 ticks**;
- requer research `FIRE_SPELL`;
- acende Candle/Campfire compatível;
- inicia `IBurner` compatível;
- em entidade, aplica **200 fire ticks**;
- settlement de mana é provider-native após um alvo válido.

### Frost Touch — `frost_touch`

- custo base: **20 mana**;
- requer research `FROST_SPELL`;
- transforma water source atingida em Ice;
- em LivingEntity aplica `CHILLED_EFFECT` por **200 ticks**.

### Darklight Chant / Light Chant

- custo base: **3 mana**;
- exigem pelo menos **3 reputation** com a divindade correspondente;
- em bloco, criam `GhostLight` alinhada à divindade;
- em LivingEntity aplicam **Glowing por 200 ticks**.

### Dark Touch — `dark_touch`

- custo base fallback: **20 mana**;
- exige pelo menos **10 reputation Dark**;
- trabalha sobre exatamente um ItemEntity próximo ao ponto alvo;
- primeiro tenta `ChantConversionRecipe` compatível com devoção Dark ou deity dummy;
- a receita pode declarar custo próprio; caso contrário usa o custo do spell;
- converte a maior quantidade que a mana atual consegue pagar;
- se não houver recipe e o item for damageable com stack size 1, aplica componente `NECROTIC = 50` pagando o custo;
- enquanto `NECROTIC > 0`, ataques com o item convertem parte do dano original em Wither damage e decrementam uma carga em hit bem-sucedido.

### Holy Touch — `holy_touch`

- usa a mesma arquitetura de conversão do Dark Touch;
- exige pelo menos **10 reputation Light**;
- quando não existe conversion recipe e o item é elegível, aplica `CONSECRATED = 50` pagando o custo;
- contra alvo undead, uma arma consecrated multiplica o dano corrente por **1.5** e consome uma carga;
- o provider também força o bônus de Smite em entidades tratadas como undead por sua lógica de Undeath quando necessário.

### Smite Chant — `smite_chant`

- custo configurado no spell: **40 mana**;
- só aceita LivingEntity na tag vanilla `EntityTypeTags.UNDEAD`;
- dano base configurável: **10 magic damage**;
- em hit bem-sucedido aplica **Weakness III** (`amplifier 2`) por **200 ticks**;
- concede research `SMITE_UNDEAD`.

> Nota de auditoria: a implementação de `SmiteSpell.cast()` não chama `IMana.expendMana` diretamente. Como o framework base apenas checa mana em `canCast` e o gasto normal é feito por cada implementação concreta, o custo efetivamente liquidado de Smite precisa de **runtime QA**. Black Arcana não deve “corrigir” isso debitando por fora, pois isso alteraria authority e poderia causar double-charge caso outro path do provider faça o settlement.

### Sunder Armor — `sunder_armor`

- custo declarado: **50 mana**;
- aplica `VULNERABLE_EFFECT` por **1200 ticks**, amplifier 0, a um LivingEntity atingido.

> Nota de auditoria: `ApplyPotionSpell.cast()` apenas aplica o efeito e não chama `IMana.expendMana`. Assim como Smite, o settlement efetivo do custo precisa de runtime QA antes de qualquer integração econômica.

## Prayer / devotion loop

`PrayerSpell` não é um spell comum de dano:

- exige uma `EffigyTileEntity` pronta próxima;
- verifica cooldown/reputation via capability provider-native;
- ao concluir, chama `effigy.pray()`;
- calcula `AltarInfo` e adiciona reputação da divindade;
- atualiza mana máxima e mana atual com base em reputação, altar capacity e altar power;
- registra o momento da oração na capability de reputation.

Defaults do PrayerSpell:

- base reputation: **1**;
- altar power multiplier: **0.25**;
- cooldown default retornado pelo provider: **21000 ticks** (~17m30s em 20 TPS), configurável por server config.

Isso prova que mana e devotion do Eidolon são um loop econômico próprio. Não devem ser fundidos automaticamente com Ars Source, Iron's mana, Goety Soul Energy ou recursos do Black Arcana.

## Progressão / gates

Gates confirmados no source incluem pelo menos:

- research/knowledge para Fire Chant e Frost Touch;
- reputation mínima Dark para Dark Touch;
- reputation mínima Light para Holy Touch;
- deity/effigy/cooldown para prayers;
- target/type gates específicos para Smite, conversões, cura e outros chants;
- recipes data-driven para conversões e chants externos.

O inventário de research e a cadeia survival completa de desbloqueio ainda precisam ser documentados em profundidade antes de declarar a progressão Eidolon fechada.

## Deduplicação / integração Black Arcana

### Provider-native first

Black Arcana pode observar `SpellCastEvent.Pre/Post`, resultados do mundo e progressão para perks/quests, mas não deve:

- debitar Eidolon mana uma segunda vez;
- recalcular reputation/devotion de prayer;
- aplicar de novo `NECROTIC`, `CONSECRATED`, `CHILLED`, `VULNERABLE` ou outros efeitos;
- substituir SignSequence por heurística própria;
- reproduzir ChantConversionRecipe fora do provider;
- conceder research que o Eidolon não concedeu;
- tratar prayer como cast genérico sem altar;
- fundir soul/reputation/mana do Eidolon com recursos de outros providers sem contrato explícito.

### Authority e causalidade

Um cast Eidolon deve gerar uma única identidade causal. Se uma perk Black Arcana reagir ao evento provider-native, a reação deve ser deduplicada contra efeitos observados subsequentemente no mundo para não contar o mesmo cast duas vezes.

### Fail-closed

Spells cujo gasto de mana aparente não é liquidado diretamente na implementação concreta — pelo menos `SmiteSpell` e `ApplyPotionSpell`/`SunderArmorSpell` no source auditado — permanecem **fail-closed para integrações econômicas** até runtime QA. Não se presume “cast grátis” nem se injeta correção externa.

## Próximas etapas da auditoria Eidolon

1. extrair e catalogar os demais parâmetros concretos dos 20 spells;
2. inventariar `RitualRegistry` separadamente do spell registry;
3. inventariar recipes data-driven de chant/command chant/conversion;
4. mapear `Researches` e gates survival;
5. mapear soul capability e seus consumers/producers;
6. executar runtime QA dos settlements e dos eventos Pre/Post;
7. só então promover o provider para `CATÁLOGO GRANULAR COMPLETO`.

## Proveniência

- presença/JAR/versão: modlist 612 + Auditoria Mestre do Notion, reconciliadas em 2026-09-07;
- source version pin: commit `696a47333e43970be7f697790eac0af76b6a04b8`, cujo `gradle.properties` declara `mod_version=0.5.0.2`;
- spell registry/signs/framework: source oficial pinado;
- números acima: classes concretas da mesma versão;
- runtime behavior ainda não foi testado nesta etapa.