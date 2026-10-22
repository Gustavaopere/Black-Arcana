# Bedrock Skin

**Prova de identidade:** ✅ `COUNTED_EXACT` **somente para ID de registry estático** no JAR publicado, ver [auditoria binária 5/5](../EXACT-BINARY-SPELLS-1.1.1.md) e [run #38308575364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38308575364). Os dados funcionais abaixo continuam source-pinned; efeitos reais, configurações e Survival não foram aceitos.

- **Status:** PRESENTE — released in current 1.1.1 line
- **ID:** `paladin_spells:bedrock_skin`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 30–165
- **Cooldown:** 25 s
- **Spell power neutral:** 5–23
- **Duration neutral:** 10–28 s
- **Role:** self-rooted defensive stance

## Source 1.1.1

`duration = 5 + getSpellPower`

Source percentage reduction:

`normalized=(level-1)/(maxLevel-1)`

`exponent=1.2/(1+0.05*getSpellPower)`

`scaled=normalized^exponent`

`armorBonus=0.20*armor/(armor+100)`

`reduction=min(0.95, 0.10 + 0.50*scaled + armorBonus)`

The cast stores this value as `bedrock_skin_reduction`, applies `BEDROCK_SKIN_EFFECT` with amplifier `level-1`, creates `BedrockSkinEntity`, mounts the caster onto it and assigns the duration.

`BedrockSkinEntity` is invulnerable, disallows horizontal motion, permits vertical falling, anchors its passenger at its own coordinates and discards after duration or when it is no longer a vehicle. **Root/immobilization is therefore source-confirmed.**

`BedrockSkinEffect` independently declares an Armor modifier of `+10 ADD_VALUE` before amplifier semantics.

## Consumidor de mitigação — correção de auditoria 22/10/2026

O mesmo commit contém `BedrockSkinEvent#onLivingDamage(LivingDamageEvent.Pre)`: com o efeito ativo, lê `BedrockSkinEffect.DAMAGE_REDUCTION_KEY` e faz `event.setNewDamage(event.getNewDamage() * (1.0f - reduction))`. A antiga afirmação de consumidor ausente estava incorreta; o [catálogo agregado](../../../../../docs/catalog/PALADIN-SPELLS-1.1.1.md) já registrava esse handler. A cadeia é source-confirmada, enquanto JAR funcional, ordem de eventos e dano final seguem sem aceite físico. Não instalar outro handler de mitigação.

## Mandatory matrix

- damage/heal: none directly;
- target/range: self;
- duration/scaling: formulas above, reduction cap 95%;
- immobilization: provider entity confirmed;
- armor modifier: +10 ADD_VALUE effect declaration confirmed; final amplifier behavior follows MobEffect runtime and needs live observation for exact displayed armor;
- acquisition/focus/ritual: specific route `NÃO VERIFICADO`;
- VFX/audio: self-cast animation; additional final assets `NÃO VERIFICADO`;
- dedup: occupies rooted heavy-defense Holy stance;
- QA/fail-closed: consumidor source-confirmado; percentual efetivamente entregue no JAR instalado requer prova física.

## Source

Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`, `BedrockSkinSpell`, `BedrockSkinEffect`, `BedrockSkinEntity`.


## Dossiê por campo para perks — reauditoria 22/10/2026

**Fidelidade:** `SOURCE_PARAMETERS / SOURCE_CAUSALITY` no pin abaixo; identidade `COUNTED_EXACT` histórica conforme [JAR/SHA](../EXACT-BINARY-SPELLS-1.1.1.md), sem recompilação equivalente source→JAR ou execução física nesta reauditoria. Provider `paladin_spells`, JAR `paladin_spells-1.21.1-1.1.1.jar`, SHA-1 `e4c6f4fa70989f0b9f1819e46e29f68d414ccbaf`, Minecraft 1.21.1 / NeoForge. Source declara NeoForge 21.1.200 e Iron's 3.14.7; o pack usa host 3.16.3, por isso compatibilidade não é inferida apenas do build upstream.

**Classe:** `eu.kaufko.paladin_spells.spells.BedrockSkinSpell`; [BedrockSkinSpell](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BedrockSkinSpell.java#L22). Registro: [PaladinSpellRegistry](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/registry/PaladinSpellRegistry.java#L12).

**Notação:** n=spellLevel, P=getSpellPower(n,caster) resolvido pelo host, A=armor do caster; valores neutros não representam config implantada. Todas as cinco magias são Rare/Holy, maxLevel default 10, INSTANT. Mana segue o host; defaults de constructor não são novo recurso Black Arcana.

| Eixo | Valor, fase e limites | Fonte no commit exato | Superfície para perk |
|---|---|---|---|
| Alvo / alcance / área | Self; ancora o caster com startRiding(anchor,true), sem resolver terceiros. Não transforma terreno; o nome Bedrock não autoriza mutação de blocos. | [entity.addEffect](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BedrockSkinSpell.java#L61) | SEM_HOOK_SEGURO para trocar alvo/área. |
| Tempo | D = 5+P s, ticks = Math.round(20D); P neutro 5+2(n−1), D neutro 10–28 s. Cast 0 ticks, cooldown default 25 s. Entidade remove passageiros e descarta quando tickCount > duration ou !isVehicle(). | [int durationTicks](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BedrockSkinSpell.java#L57) | CONTRATO_CONDICIONAL: P altera duração e curva de redução, não um setter exclusivo de duração. |
| Dano / defesa / tipo | r=min(0,95; 0,1 + 0,5*((n−1)/(m−1))^(1,2/(1+0,05P)) + 0,2A/(A+100)); A=armor, m=defaultConfig.maxLevel. onCast guarda r. BedrockSkinEvent#onLivingDamage usa newDamage*(1−r) em LivingDamageEvent.Pre com o efeito ativo. Não troca DamageType. | [public float getDamageReduction](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BedrockSkinSpell.java#L73) | Hook de consumo source-confirmado; SEM_HOOK_SEGURO para perk alterar r pelo persistent data do provider. |
| Entidade / hitbox / lifecycle | Âncora, não projétil ofensivo. PaladinEntityRegistry declara width=height=0,1 bloco; fireImmune/noSummon. BedrockSkinEntity é invulnerável, move só Y, persiste Duration; positionRider mantém passageiro em sua posição. Escala visual não altera essa dimensão. | [BedrockSkinEntity anchor](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BedrockSkinSpell.java#L63) | SEM_HOOK_SEGURO para redimensionar ou duplicar a âncora. |
| Custos / ingresso / cooldown | Constructor e DefaultConfig definem mana e cooldown descritos acima; lançamento via pipeline Iron's. No ingresso jogador, castSpell debita mana após SpellOnCastEvent e antes de onCast, conforme [boundary auditado](../PERK-BOUNDARIES-1.1.1.md#evento-de-cast-callbacks-e-mastery-no-host-3163). Reserva/refund de ingressos alternativos, limites efetivos e obtenção Survival específica NÃO VERIFICADO. | [constructor](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BedrockSkinSpell.java#L39) / [DefaultConfig](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BedrockSkinSpell.java#L47) | CONFIG_NATIVE para defaults; não implica desconto por player nem pagamento paralelo. |

### Pipeline e consumidores downstream

onCast server: calcula redução e duração, grava bedrock_skin_reduction, adiciona efeito com amplifier=n−1, cria âncora, stopRiding e startRiding. O MobEffect pode existir mesmo se create retornar null; não há rollback da aplicação nesse ramo. BedrockSkinEffect declara +10 ARMOR ADD_VALUE antes da semântica de amplifier do host. BedrockSkinEvent#onLivingDamage(LivingDamageEvent.Pre) lê a chave pelo símbolo BedrockSkinEffect.DAMAGE_REDUCTION_KEY e altera newDamage. A afirmação anterior ignorava esse consumidor por constante: ele existe neste mesmo source pin. O handler não contém guard explícito de lado e possui @EventBusSubscriber; emissão efetiva/ordem de listeners exige runtime. onDismount só cancela saída se tickCount<=0: não afirmar bloqueio de desmontagem durante toda a duração. O override onCast não chama super.onCast; no ingresso jogador do host auditado, evento de cast, mana e cooldown acontecem fora de super.onCast; ver [ordem causal e Mastery](../PERK-BOUNDARIES-1.1.1.md#evento-de-cast-callbacks-e-mastery-no-host-3163). Isso não valida efeitos entregues.

[BedrockSkinEvent#onLivingDamage](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/events/BedrockSkinEvent.java#L16) · [BedrockSkinEvent#onDismount](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/events/BedrockSkinEvent.java#L33) · [BedrockSkinEffect#constructor](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/effects/BedrockSkinEffect.java#L14) · [PaladinEntityRegistry dimensions](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/registry/PaladinEntityRegistry.java#L18) · [BedrockSkinEntity#tick](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/entity/spells/BedrockSkin/BedrockSkinEntity.java#L26) · [BedrockSkinEntity#addAdditionalSaveData](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/entity/spells/BedrockSkin/BedrockSkinEntity.java#L78).

### Contratos dos três projetos e mutabilidade

RPG Skill Tree é dono de perks/atributos/Mastery; Iron's e Paladin mantêm casting, mana, cooldown e efeito. O [boundary transversal verificado](../PERK-BOUNDARIES-1.1.1.md) aponta `IronsInvestmentAttributesRuntime#refresh(ServerPlayer,AttributeRanks)` e `IronsInvestmentCooldownEvents#onCooldownPre(SpellCooldownAddedEvent.Pre)` do RPG: eles não constituem setters de alvo, DamageType, geometria ou duração isolada deste spell. A variação de P só se aplica aos consumidores explícitos desta ficha. `SEM_HOOK_SEGURO` significa que não foi demonstrada uma API mutadora segura para o eixo neste escopo, não uma prova de impossibilidade universal.

Enshrouded continua dono de Shroud/exposure; sua interface `MagicDamageClassifier#classify(DamageSource)` classifica, sem setter de tipo/dano/alvo. Black Arcana preserva world safety/causalidade próprios e não reexecuta efeitos do provider. A Factory é referência de produção, sem criar bridge runtime automaticamente.

### Aceitação ainda necessária

Testar redução real e ordem com outros LivingDamageEvent.Pre, armor/amplifier, dismount após tick 0, falha de criação/montagem, logout, morte e save/restart da âncora. Não adicionar outro handler de redução: duplicaria o consumidor existente.

**QA:** source consultado e localizadores verificados; config implantada, cliente, GameTest com provider real, Survival e modpack `PENDING`. Nenhuma perk/adapter implementada. Descrição de gameplay acima é resumo original da semântica no source, não transcrição de tooltip; [README oficial pinado](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/README.md) pode divergir do changelog. Consulta de código não autoriza copiar implementação/assets: LICENSE.txt declara CC BY-NC-SA 4.0, enquanto gradle.properties declara All Rights Reserved; preservar essa divergência e não importar source.
