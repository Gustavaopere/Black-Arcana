# Sworn Protector

**Prova de identidade:** ✅ `COUNTED_EXACT` **somente para ID de registry estático** no JAR publicado, ver [auditoria binária 5/5](../EXACT-BINARY-SPELLS-1.1.1.md) e [run #38308575364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38308575364). Os dados funcionais abaixo continuam source-pinned; efeitos reais, configurações e Survival não foram aceitos.

- **Status:** PRESENTE — current 1.1.1 changelog removes WIP from released spells; stale README wording is not current authority
- **ID:** `paladin_spells:sworn_protector`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 30–165
- **Cooldown:** 35 s
- **Spell power neutral:** 10–55
- **Range source:** 36–90 blocks
- **Duration neutral:** 17–26 s
- **Role:** redirect a percentage of nearby player damage to protector

## Formulas

The range helper is named `getRange(int spellPower)` but the call site passes **spellLevel**:

`range = (10 + 2*spellLevel)*3`

Redirect:

`normalized=(level-1)/(maxLevel-1)`

`scaled=normalized^(0.6/(1+0.1*getSpellPower))`

`armorBonus=0.20*armor/(armor+100)`

`redirect=min(1.0, 0.20 + 0.60*scaled + armorBonus)`

At level 1 this starts at 20% + armor bonus; at level 10 it reaches 80% + armor bonus before the 100% cap.

`duration = 15 + 0.20*getSpellPower`.

## Server settlement design

`SwornProtectorEvent` listens to `LivingIncomingDamageEvent` server-side and:

1. only protects Player victims;
2. ignores already-redirected damage to prevent recursion;
3. searches protectors with the effect in a broad 64-block box;
4. filters by each protector's stored range;
5. chooses the nearest eligible protector;
6. refuses redirect when protector is the attacker;
7. subtracts the redirected portion from victim damage;
8. hurts protector exactly once with dedicated `paladin_spells` redirect damage type.

O handler evita recursão pelo tipo REDIRECT e deve continuar provider-native. Isso não comprova identidade de cast, exatamente uma recompensa de Mastery ou ausência de interferência de outros listeners.

## Authority blocker found in exact 1.1.1 source

The current `SwornProtectorSpell.onCast` writes `sworn_protector_redirect`, `sworn_protector_range` and `SWORN_PROTECTOR_EFFECT` only inside:

`if (level.isClientSide) { ... }`

The redirection event explicitly runs server-side. Client persistent data/effects are not a valid substitute for server-authoritative state.

Therefore the semantic design/event settlement is fully documented, but **functional activation is `LIVE-JAR/GAMETEST REQUIRED`**. Black Arcana must not silently emulate the missing server state in this catalog branch.

## Mandatory matrix

- target: self as protector; protected victims are nearby Players chosen later by event;
- PvP: attacker==protector guard confirmed; broader party/team/protection semantics `NÃO VERIFICADO`;
- bosses/summons: not protected victims unless Player; damage source attacker can vary;
- acquisition/focus/ritual: specific route `NÃO VERIFICADO`;
- VFX/audio: Bulwark start sound + `CHARGE_RAISED_HAND`; tether visualization not source-confirmed;
- dedup: occupies ally-damage interception/protector-link signature;
- fail-closed: no bridge redirection until server authority is proven/corrected.

## Source

Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`, `SwornProtectorSpell` + `SwornProtectorEvent`; changelog 1.1.1.


## Dossiê por campo para perks — reauditoria 22/10/2026

**Fidelidade:** `SOURCE_PARAMETERS / SOURCE_CAUSALITY` no pin abaixo; identidade `COUNTED_EXACT` histórica conforme [JAR/SHA](../EXACT-BINARY-SPELLS-1.1.1.md), sem recompilação equivalente source→JAR ou execução física nesta reauditoria. Provider `paladin_spells`, JAR `paladin_spells-1.21.1-1.1.1.jar`, SHA-1 `e4c6f4fa70989f0b9f1819e46e29f68d414ccbaf`, Minecraft 1.21.1 / NeoForge. Source declara NeoForge 21.1.200 e Iron's 3.14.7; o pack usa host 3.16.3, por isso compatibilidade não é inferida apenas do build upstream.

**Classe:** `eu.kaufko.paladin_spells.spells.SwornProtectorSpell`; [SwornProtectorSpell](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/SwornProtectorSpell.java#L28). Registro: [PaladinSpellRegistry](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/registry/PaladinSpellRegistry.java#L12).

**Notação:** n=spellLevel, P=getSpellPower(n,caster) resolvido pelo host, A=armor do caster; valores neutros não representam config implantada. Todas as cinco magias são Rare/Holy, maxLevel default 10, INSTANT. Mana segue o host; defaults de constructor não são novo recurso Black Arcana.

| Eixo | Valor, fase e limites | Fonte no commit exato | Superfície para perk |
|---|---|---|---|
| Alvo / alcance / área | Self como protetor; vítimas do evento são Player. R=(10+2n)*3 blocos = 36–90 para n=1–10. O argumento é nível, não P. Handler primeiro busca LivingEntity na AABB da vítima inflada em 64, depois exige distanceTo≤R e efeito; não é esfera de 64 nem garantia de alcance pleno de 90. | [private float getRange](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/SwornProtectorSpell.java#L63) | SEM_HOOK_SEGURO: aumentar R armazenado não amplia a busca inicial de 64. |
| Tempo | D=15+0,2P s, ticks=(int)(20D); P neutro 10+5(n−1), D neutro 17–26 s. Cast 0 ticks, cooldown default 35 s. | [private float getDuration](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/SwornProtectorSpell.java#L67) | CONTRATO_CONDICIONAL: P afeta D e curva de redirect, mas não R. |
| Dano / tipo / caps | q=min(1; 0,2+0,6*((n−1)/(m−1))^(0,6/(1+0,1P))+0,2A/(A+100)), m=10. Handler: d=event.getAmount()*q; setAmount(original−d); protector.hurt(new DamageSource(REDIRECT,victim),d). Tipo paladin_spells:redirect, atacante atribuído à vítima original nesse construtor. | [public float getRedirectPercentage](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/SwornProtectorSpell.java#L71) | SEM_HOOK_SEGURO para conversão de tipo/duplication de redirecionamento; dano pré-settlement não é HP entregue. |
| Projétil / hitbox / summons | N/A: buff + listener, sem projétil. AABB é busca de protetores. Redirect não cria outra identidade de spell. | [public void onCast](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/SwornProtectorSpell.java#L123) | N/A; não inferir colisão ou escala mutável. |
| Custos / ingresso / cooldown | Constructor e DefaultConfig definem mana e cooldown descritos acima; lançamento via pipeline Iron's. Reserva/refund, momento exato do débito, limites efetivos e obtenção Survival específica NÃO VERIFICADO nesta reauditoria. | [constructor](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/SwornProtectorSpell.java#L87) / [DefaultConfig](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/SwornProtectorSpell.java#L95) | CONFIG_NATIVE para defaults; não implica desconto por player nem pagamento paralelo. |

### Pipeline e consumidores downstream

Bloqueio de autoridade preservado: onCast escreve sworn_protector_redirect/range e adiciona efeito apenas se level.isClientSide. SwornProtectorEvent#onLivingHurt(LivingIncomingDamageEvent) retorna no cliente, ignora REDIRECT, exige vítima Player, escolhe menor distanceToSqr entre protetores elegíveis e retorna se o escolhido for atacante (não tenta o segundo). Consulta AABB sem filtro explícito de alive/team/LOS. Exige presença de RANGE_KEY mas lê REDIRECT_KEY sem contains separado. Não há cast token; proteção anti-recursão por DamageType não equivale a deduplicação global de Mastery/procs. Não criar efeito server-side compensatório neste trabalho documental.

[SwornProtectorEvent#onLivingHurt](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/events/SwornProtectorEvent.java#L25) · [PaladinDamageTypeRegistry#REDIRECT](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/registry/PaladinDamageTypeRegistry.java#L10).

### Contratos dos três projetos e mutabilidade

RPG Skill Tree é dono de perks/atributos/Mastery; Iron's e Paladin mantêm casting, mana, cooldown e efeito. O [boundary transversal verificado](../PERK-BOUNDARIES-1.1.1.md) aponta `IronsInvestmentAttributesRuntime#refresh(ServerPlayer,AttributeRanks)` e `IronsInvestmentCooldownEvents#onCooldownPre(SpellCooldownAddedEvent.Pre)` do RPG: eles não constituem setters de alvo, DamageType, geometria ou duração isolada deste spell. A variação de P só se aplica aos consumidores explícitos desta ficha. `SEM_HOOK_SEGURO` significa que não foi demonstrada uma API mutadora segura para o eixo neste escopo, não uma prova de impossibilidade universal.

Enshrouded continua dono de Shroud/exposure; sua interface `MagicDamageClassifier#classify(DamageSource)` classifica, sem setter de tipo/dano/alvo. Black Arcana preserva world safety/causalidade próprios e não reexecuta efeitos do provider. A Factory é referência de produção, sem criar bridge runtime automaticamente.

### Aceitação ainda necessária

Testar activation server, dois protetores, escolhido==atacante, diagonal da AABB, distâncias 63/65/90, origem do DamageSource, armor/resistências e ordem de eventos; efeito/chaves ausentes e loops de terceiros. Nenhum PASS runtime derivado do source.

**QA:** source consultado e localizadores verificados; config implantada, cliente, GameTest com provider real, Survival e modpack `PENDING`. Nenhuma perk/adapter implementada. Descrição de gameplay acima é resumo original da semântica no source, não transcrição de tooltip; [README oficial pinado](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/README.md) pode divergir do changelog. Consulta de código não autoriza copiar implementação/assets: LICENSE.txt declara CC BY-NC-SA 4.0, enquanto gradle.properties declara All Rights Reserved; preservar essa divergência e não importar source.
