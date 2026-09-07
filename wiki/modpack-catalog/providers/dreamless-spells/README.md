# Dreamless Spells

## Estado canônico

- mod id: `dreamless_spells`
- JAR instalado: `dreamless_spells-1.1.9.jar`
- versão instalada: `1.1.9`
- Minecraft: 1.21.1
- loader: NeoForge
- release CurseForge: 2026-04-10
- source oficial: `stikbug/Neoforge-Dreamless-Spells-N-Spellbooks`
- source pin release-aligned: `71f7befa81f618d07bfa023c5c82d32fdb10077a`
- estado: **RELEASE-ALIGNED SOURCE 1.1.9 / REGISTRY 4/4 / CATÁLOGO 4/4 COMPLETO / EMPTY PROGRESSION + COUNTERSPELL MIXIN QA-BLOCKED**

O SHA acima é o último commit oficial do dia da release 1.1.9 e contém apenas um rename interno posterior ao commit de receitas da mesma data. Ele é tratado como `release-aligned`, não como prova criptográfica de que o JAR do CurseForge foi compilado exatamente desse commit.

Dreamless é principalmente um addon de Iron's Spells voltado a equipamento, Curios e ferramentas anti-mago. A parte mágica relevante cria a escola própria **Empty**, adiciona três spells Empty, uma spell Ice e aplica um mixin sobre o Counterspell do Iron's.

## Inventário ativo de spells

`SpellRegistries` registra exatamente quatro spells:

| Spell | ID canônico | Escola | Rarity | Níveis |
|---|---|---|---:|---:|
| Jadeskin | `dreamless_spells:jadeskin` | Ice | Legendary | 1–3 |
| Drained | `dreamless_spells:drained` | Empty | Legendary | 1–3 |
| Dullard | `dreamless_spells:dullard` | Empty | Legendary | 1–3 |
| Mute / Doorway Effect | `dreamless_spells:doorway_effect` | Empty | Legendary | 1–5 |

A classe da última spell se chama `MuteSpell`, mas seu `ResourceLocation` continua sendo `doorway_effect`. A Wiki usa o ID runtime como autoridade.

## Escola Empty

A escola runtime registrada é `dreamless_spells:empty`. Ela possui:

- `dreamless_spells:empty_spell_power`, base 1.0, range 0–10;
- `dreamless_spells:empty_magic_resist`, base 1.0, range 0–10;
- damage type próprio `dreamless_spells:empty_magic`;
- focus tag `dreamless_spells:empty_focus`;
- focus concreto `dreamless_spells:empty_gem`;
- cast sound configurado como Iron's Evocation Cast.

O construtor de `SchoolType` usado mantém os defaults do Iron's: `requiresLearning=false` e `allowLooting=true`.

## Progressão e obtenção

### Jadeskin

Jadeskin pertence à escola Ice do Iron's e não possui gate `Emptied`. Seu `DefaultConfig` mantém crafting habilitado por default e, por pertencer a uma escola lootável, é elegível para os pipelines normais de scroll/loot que selecionam spells Ice ou spells globais. Fonte garantida específica do próprio Dreamless: **NÃO VERIFICADO**.

### Empty spells

Drained, Dullard e Doorway Effect têm custo de mana base **0** e só passam `checkPreCastConditions` se o caster possuir o efeito `dreamless_spells:emptied`.

O focus Empty é craftável:

`Arcane Gem + Pavarium Nugget -> Empty Gem`

O source também registra `dreamless_spells:empty_rune` e o adiciona à tag `irons_spellbooks:inscribed_runes`. As armaduras Empty dependem dessa rune em smithing. Porém nenhuma receita ou loot de aquisição para a própria Empty Rune foi localizada no source 1.1.9, e o Iron's usa receitas explícitas por escola para criar suas runas. Portanto a aquisição survival da Empty Rune permanece **NÃO VERIFICADA / BLOQUEADOR DE PROGRESSÃO** até teste do pack completo.

Qualquer set completo Empty Priest, Empty Brawler ou Empty Hunter aplica `Emptied` por 200 ticks com amplifier 3 quando o efeito está ausente. Isso habilita as três spells Empty.

Ver `empty/PROGRESSION.md` para o pipeline completo e os riscos de swap de armadura.

## Overlay em Counterspell

`dreamless.mixins.json` ativa `CounterspellSpellMixin`, que sobrescreve `CounterspellSpell#getSchoolType()` para retornar uma escola Empty declarada em `DSSSpells.Schools.EMPTY`.

Esse holder pertence a um **segundo DeferredRegister** que não é registrado pelo entrypoint; o runtime oficial registra `DSSSchoolRegistry.EMPTY`. A identidade/validade desse override é, portanto, um blocker estático e precisa de runtime QA. Black Arcana não deve aplicar um segundo override para esconder o problema.

Ver `overlays/counterspell-empty-school.md`.

## Regra de integração Black Arcana

**Provider-native first.** Debuffs, cancelamento de `SpellPreCastEvent`, school identity, MobEffects e gates de equipamento pertencem a Dreamless/Iron's. Black Arcana pode observar resultados para progressão/perks, mas não deve:

- cancelar casts uma segunda vez;
- reaplicar Drained/Dullard/Mute;
- criar uma escola Empty paralela;
- forçar Counterspell para Empty;
- contornar o gate `Emptied`;
- fabricar uma rota de Empty Rune sem decisão explícita de design.

As divergências de 1.1.9 estão detalhadas em `TECHNICAL-AUDIT.md`.