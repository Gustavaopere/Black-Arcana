# Asterism Arcanum 0.1.0 — auditoria técnica

## Provenance

Autoridade local: `asterismarcanum-1.21.1-0.1.0.jar`.

Source exato: `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`. O `gradle.properties` desse commit declara Minecraft 1.21.1 e `mod_version=1.21.1-0.1.0`, correspondendo ao artefato instalado.

O source 0.1.0 compila contra Iron's 3.15.6; o pack usa 3.16.3. Contratos de Asterism são source-confirmed, mas qualquer comportamento sensível à API de Iron's permanece sob runtime QA.

## Registry e survival

`ASARSpellRegistry` registra 11 spells. A release e o próprio lang file deixam `Astral Gateway` como não totalmente implementado/não craftable e fora do survival. `Trailblaze` possui classe, mas registration comentado.

Catálogo canônico:

- registry runtime: 11;
- survival: 10/10 catalogado;
- non-survival: Astral Gateway;
- unregistered/dev: Trailblaze.

## Acquisition pipeline

O loot table `asterismarcanum:entities/astromancer` possui um pool de `irons_spellbooks:scroll` com `irons_spellbooks:randomize_spell`, quality 0.25–0.85 e filtro de escola Astral.

No Iron's 3.16.3 do pack:

- `SpellFilter` inclui somente spells enabled e `allowLooting()` quando `force=false`;
- `AbstractSpell.allowLooting()` delega para `SchoolType.allowLooting`;
- o construtor de `SchoolType` usado por Astral define `allowLooting=true`;
- `DefaultConfig.allowCrafting` default é `true`.

### QA-01 — Astral Gateway pode vazar para loot/crafting

`AstralGatewaySpell` não sobrescreve `allowLooting()` e não define `.setAllowCrafting(false)`. Portanto, apesar de ser oficialmente creative-only/unfinished, a composição estática Asterism 0.1.0 + Iron's 3.16.3 fornece um caminho para ele entrar no pool de random Astral scrolls e no Scroll Forge se não houver config/datapack adicional excluindo-o.

**Regra Black Arcana:** tratar Gateway como non-survival e fail-closed. Não usar em progressão, perks ou loot autoral até GameTest/config confirmar exclusão efetiva.

## QA-02 — Celestial Tether: tooltip e settlement divergem

A spell exibe `spellPower + 1` como hits dodged, mas inicializa `CelestialTetherEntity` com `spellLevel + 1`. A entidade só destrói quando o contador fica `< 0`, após decrementar em cada hit cancelado.

O contador sugere `spellLevel + 2` apenas em sequência nominal com tick de entidade entre eventos. Como a remoção só ocorre no tick após contador<0, vários eventos antes desse tick podem ultrapassar esse número; não é um cap rígido demonstrado. Dano sem `source.entity` também não entra no handler de cancelamento.

Não criar shield paralelo; validar com GameTest níveis 1 e 8.

## QA-03 — Silvery Barbs cancela múltiplos hits durante a janela

Silvery Barbs aplica Luck II por 20 ticks e `silvery_barbs_tag`. O handler cancela `LivingIncomingDamageEvent` sempre que ambos estão presentes. O tag não é consumido no primeiro cancelamento.

Logo, pela leitura estática, pode cancelar vários hits dentro de ~1 segundo, não apenas um. Quando o tag permanece mas Luck acabou, o próximo damage event remove o tag sem cancelar.

Também há `public static float radius`, mutado pelo cast; getUniqueInfo/getRadius apenas leem no pin auditado, estado global da singleton spell. QA multiplayer obrigatório.

## QA-04 — Starcutter radius clamp

A spell calcula radius `(level + 4) + 1.5*spellPower` e raycast range `radius*1.5`, mas `StarcutterEntity.setRadius()` aplica `Math.min(pRadius, 1)`. A explosão usa `entityRadius*10`.

Com valores normais, o entity radius fica 1 e o raio aparente de settlement fica 10, divergindo do scaling exibido/calculado pela spell.

Não compensar externamente aumentando AoE; validar antes.

## QA-05 — Starfire ricochet/friendly filtering

StarfireProjectile tem pierce level 2 e ricochet. O filtro de candidato de ricochet admite:

`(owner == null || !Utils.shouldHealEntity(owner, entity)) || entity.getClass() == hit.getClass()`.

A segunda condição pode reintroduzir uma entidade da mesma classe mesmo quando `Utils.shouldHealEntity` a trataria como friendly. Party/PvP/summon QA obrigatório.

## QA-06 — Star Swarm gate collision flag

Star Swarm usa uma única `StarSwarmProjectile`, derivada de `AbstractGateProjectile`. O gate possui 5 partes e, em ticks divisíveis por 12 ou 20, cada parte dispara 3 `PiercingLightProjectile`.

`AbstractGateProjectile.setDealDamageActive()` define `dealDamageActive=false`, apesar do nome. Assim, o continuous cast não reativa a collision damage do gate após o primeiro settlement; a chuva de projectiles continua independentemente.

Black Arcana não deve adicionar um segundo tick de gate damage para “corrigir” isso.

## QA-07 — Luminous Beam friendly-fire

Luminous Beam cria uma única entidade persistente por cast e reativa seu damage settlement em chamadas subsequentes de onCast no canal (settlement do host, não cada onServerCastTick). O beam collision filter exclui owner e exige LOS, mas não contém filtro allied explícito antes de `DamageSources.applyDamage`.

Validar party/PvP e summons; não inferir imunidade de aliados.

## QA-08 — Summon Lunar Moth é singular

Apesar do ID plural `summon_lunar_moths`, `getSummonCount()` retorna 1 e a implementação cria um único `SummonedLunarMothEntity` por janela de recast. Duração: 10 minutos.

A entidade usa `SummonManager`, replica target do owner, possui 15 HP, 2 base attack damage, atributo Mana Rend 0.15, aplica Levitation por 40 ticks ao atacar e pode ser montada pelo summoner. Mana Rend não é bônus plano de 15% nem mana drain: o consumidor Ace’s depende dos atributos/config do atacante e mana máxima do alvo. A ficha reaudita também super.doHurtTarget seguido por outra tentativa Utils.doMeleeAttack; não prometer um único golpe nem duas perdas de HP.

Authority = Iron's `SummonManager` + entidade summon. Não criar segundo timer/owner registry.

## Authority map

| Spell | Settlement canônico |
|---|---|
| Astral Echo | Iron's teleport + `StarcutterEntity` echo anchor |
| Brightburst | server AoE em `onCast` |
| Celestial Tether | `CelestialTetherEntity` + incoming damage handler |
| Luminous Beam | uma `LuminousBeamProjectile` persistente |
| Piercing Light | `PiercingLightProjectile` instances |
| Silvery Barbs | Luck + persistent tag + incoming damage handler |
| Starcutter | `StarcutterEntity` delayed explosion |
| Starfire | `StarfireProjectile` pierce/ricochet |
| Star Swarm | uma gate entity + emitted Piercing Light projectiles |
| Summon Lunar Moth | `SummonManager` + `SummonedLunarMothEntity` |

## Dedup/fail-closed

1. Nunca reaplicar dano após provider settlement.
2. Nunca reproduzir teleport de Astral Echo ou retorno anti-magic.
3. Nunca criar shield paralelo para Tether/Barbs.
4. Nunca duplicar projectiles de Beam/Swarm/Piercing Light.
5. Nunca reescalar Starcutter externamente para mascarar o clamp.
6. Nunca criar ownership/timer paralelo para Lunar Moth.
7. Gateway permanece non-survival até QA comprovar gate efetivo.
8. Integrações devem carregar causal provenance por spell ID/owner quando premiarem XP/perks.

## Reauditoria dos 11 spells — 23/10/2026

[Índice e contratos comuns](SPELL-PERK-BOUNDARIES-0.1.0.md), com matrizes por ficha. Source3.15.6-target e host3.16.3 são provas distintas da identidade binária; Gateway continua conditional e fora das dez identidades strict. A releitura corrige frequência/cleanup, geometria e atribuição, sem implementar correções upstream.

- Brightburst chama target.hurt diretamente e o push não depende do retorno; SpellDamageEvent do helper não cobre esse caminho por analogia.
- Echo cria sombra com damage0 antes do teleporte; veto inicial não desfaz automaticamente a sombra. Anti-magic usa setPos direto e NBT da entidade não grava damage.
- Gateway itera targets mas muda dimensão do caster; consultas/loops não implementam transporte de grupo. Na entrada, XRot é passado aos dois campos de rotação; destino64 e respawn de saída não são retorno a uma âncora salva.
- Beam/Gate são descartados no reset normal de EntityCastData do host; failsafe/budget órfãos são outro caso. Clipping visual do Beam não muda por si parts de colisão.
- Constructors de PiercingLight usados no cast/filhos diferem do constructor factory/load quanto a noGravity; escala sincronizada não prova resize. Starfire precisa de QA específico de ricochet/pierce/bloco.
- Moth é singular, mas possui cadeia herdada+helper de ataque, efeito Levitation e Mana Rend dependente do consumidor; mutador SpellSummonEvent requer tipo compatível/ownership/cleanup, não replacement arbitrário.

Nenhum dado deste lote confirma JAR funcional/Survival/modpack, config implantada, proteção/multiplayer ou persistência. +0 strict, sem perk/runtime/adapter novo; QA e Stages permanecem com seus gates.
