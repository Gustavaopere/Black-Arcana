# Bulwark

**Prova de identidade:** ✅ `COUNTED_EXACT` **somente para ID de registry estático** no JAR publicado, ver [auditoria binária 5/5](../EXACT-BINARY-SPELLS-1.1.1.md) e [run #38308575364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38308575364). Os dados funcionais abaixo continuam source-pinned; efeitos reais, configurações e Survival não foram aceitos.

- **Status:** PRESENTE — released in Paladin Spells 1.1.1
- **ID:** `paladin_spells:bulwark`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 30–120
- **Cooldown:** 45 s
- **Spell power neutral:** 15–60 before generic/Holy/config multipliers
- **Role:** self armor amplification

## Source 1.1.1

`bonusPercent = getSpellPower(level,caster)`

`amplifier = round(bonusPercent*10)`

`durationSeconds = min(5 + 15*getSpellPower/100, 35)`

With neutral power this is 7.25–14 s. The spell applies `BULWARK_EFFECT` to self and uses the Bulwark sound plus `SELF_CAST_ANIMATION`.

## Authority / QA blocker

`BulwarkEffect` registers an `Attributes.ARMOR` modifier with operation `ADD_MULTIPLIED_TOTAL` but amount **0.0**. The audited 1.21 branch contains no separate Bulwark damage/armor handler that compensates for this.

Therefore:

- intended semantic role = confirmed;
- spell formula/amplifier/duration = confirmed;
- actual armor increase in installed gameplay = `NÃO VERIFICADO / LIVE QA REQUIRED`.

Black Arcana must not duplicate an armor multiplier to “fix” it silently; a correction belongs in an explicit provider compat/fix workstream after runtime proof.

## Mandatory matrix

- damage/heal: none directly;
- target/range: self;
- duration: formula above;
- scaling/caps: spell power multiplier; hard duration cap 35 s;
- acquisition/loot/craft/focus/ritual: specific route `NÃO VERIFICADO`;
- PvP/boss/summon: not direct targets;
- VFX/audio: sound + self-cast animation confirmed; final particles/assets `NÃO VERIFICADO`;
- dedup: occupies temporary Holy armor-amplification signature;
- fail-closed: do not treat armor gain as functioning authority until QA proves it.

## Source

- Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`.
- 1.1.1 changelog confirms Bulwark cooldown correction to 45 s and duration nerf.


## Dossiê por campo para perks — reauditoria 22/10/2026

**Fidelidade:** `SOURCE_PARAMETERS / SOURCE_CAUSALITY` no pin abaixo; identidade `COUNTED_EXACT` histórica conforme [JAR/SHA](../EXACT-BINARY-SPELLS-1.1.1.md), sem recompilação equivalente source→JAR ou execução física nesta reauditoria. Provider `paladin_spells`, JAR `paladin_spells-1.21.1-1.1.1.jar`, SHA-1 `e4c6f4fa70989f0b9f1819e46e29f68d414ccbaf`, Minecraft 1.21.1 / NeoForge. Source declara NeoForge 21.1.200 e Iron's 3.14.7; o pack usa host 3.16.3, por isso compatibilidade não é inferida apenas do build upstream.

**Classe:** `eu.kaufko.paladin_spells.spells.BulwarkSpell`; [BulwarkSpell](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BulwarkSpell.java#L24). Registro: [PaladinSpellRegistry](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/registry/PaladinSpellRegistry.java#L12).

**Notação:** n=spellLevel, P=getSpellPower(n,caster) resolvido pelo host, A=armor do caster; valores neutros não representam config implantada. Todas as cinco magias são Rare/Holy, maxLevel default 10, INSTANT. Mana segue o host; defaults de constructor não são novo recurso Black Arcana.

| Eixo | Valor, fase e limites | Fonte no commit exato | Superfície para perk |
|---|---|---|---|
| Alcance / alvo / área | Self; nenhuma seleção de terceiros ou raio. Não há limite de área a ampliar. | [entity.addEffect](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BulwarkSpell.java#L66) | SEM_HOOK_SEGURO para converter self→aliados/área. |
| Tempo / intensidade | D = min(5 + 0,15P, 35) s; ticks = (int)(20D). Amplifier = Math.round(10P). P neutro = 15+5(n−1); duração neutra 7,25–14 s, cap 35 s. Cast 0 ticks, cooldown default 45 s. | [private float getDuration](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BulwarkSpell.java#L69) | CONTRATO_CONDICIONAL: P altera duração e amplifier juntos; não equivale a duração isolada por perk. |
| Dano / defesa / tipo | Sem hurt/heal ou conversão de dano. BulwarkEffect declara ARMOR ADD_MULTIPLIED_TOTAL com amount 0.0; amplifier elevado não prova aumento de armadura. | [entity.addEffect](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BulwarkSpell.java#L66) | SEM_HOOK_SEGURO para substituir o modifier e chamar isso integração homologada. |
| Projétil / hitbox / summons | N/A: MobEffect aplicado ao caster, sem entidade de projétil ou summon. | [entity.addEffect](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BulwarkSpell.java#L66) | N/A; não redimensionar colisão por analogia com VFX. |
| Custos / ingresso / cooldown | Constructor e DefaultConfig definem mana e cooldown descritos acima; lançamento via pipeline Iron's. No ingresso jogador, castSpell debita mana após SpellOnCastEvent e antes de onCast, conforme [boundary auditado](../PERK-BOUNDARIES-1.1.1.md#evento-de-cast-callbacks-e-mastery-no-host-3163). Reserva/refund de ingressos alternativos, limites efetivos e obtenção Survival específica NÃO VERIFICADO. | [constructor](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BulwarkSpell.java#L38) / [DefaultConfig](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/spells/BulwarkSpell.java#L46) | CONFIG_NATIVE para defaults; não implica desconto por player nem pagamento paralelo. |

### Pipeline e consumidores downstream

onCast retorna no cliente; no servidor calcula P e D e adiciona BULWARK_EFFECT. Não aparece chamada super.onCast no override auditado; no ingresso jogador auditado, evento de cast, débito e cooldown acontecem fora de super.onCast, conforme [ordem causal do host](../PERK-BOUNDARIES-1.1.1.md#evento-de-cast-callbacks-e-mastery-no-host-3163). Não contar esse evento pré-efeito como dano entregue. O efeito só declara o modifier de armor 0.0; não há settlement de dano específico em BulwarkEffect. Aplicação/renovação do MobEffect e configuração efetiva continuam provider-owned.

[BulwarkEffect#constructor](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/src/main/java/eu/kaufko/paladin_spells/effects/BulwarkEffect.java#L14).

### Contratos dos três projetos e mutabilidade

RPG Skill Tree é dono de perks/atributos/Mastery; Iron's e Paladin mantêm casting, mana, cooldown e efeito. O [boundary transversal verificado](../PERK-BOUNDARIES-1.1.1.md) aponta `IronsInvestmentAttributesRuntime#refresh(ServerPlayer,AttributeRanks)` e `IronsInvestmentCooldownEvents#onCooldownPre(SpellCooldownAddedEvent.Pre)` do RPG: eles não constituem setters de alvo, DamageType, geometria ou duração isolada deste spell. A variação de P só se aplica aos consumidores explícitos desta ficha. `SEM_HOOK_SEGURO` significa que não foi demonstrada uma API mutadora segura para o eixo neste escopo, não uma prova de impossibilidade universal.

Enshrouded continua dono de Shroud/exposure; sua interface `MagicDamageClassifier#classify(DamageSource)` classifica, sem setter de tipo/dano/alvo. Black Arcana preserva world safety/causalidade próprios e não reexecuta efeitos do provider. A Factory é referência de produção, sem criar bridge runtime automaticamente.

### Aceitação ainda necessária

Medir armor antes/depois para níveis 1/10, refresh do efeito, expiração, login e diferentes P; manter aparente modifier nulo como achado de source, não bug confirmado no JAR físico. Não aplicar bônus compensatório paralelo.

**QA:** source consultado e localizadores verificados; config implantada, cliente, GameTest com provider real, Survival e modpack `PENDING`. Nenhuma perk/adapter implementada. Descrição de gameplay acima é resumo original da semântica no source, não transcrição de tooltip; [README oficial pinado](https://github.com/Kaufko/Paladin-Spells/blob/31f64ccdb39d062b21cc25d434cb62d6463b486e/README.md) pode divergir do changelog. Consulta de código não autoriza copiar implementação/assets: LICENSE.txt declara CC BY-NC-SA 4.0, enquanto gradle.properties declara All Rights Reserved; preservar essa divergência e não importar source.
