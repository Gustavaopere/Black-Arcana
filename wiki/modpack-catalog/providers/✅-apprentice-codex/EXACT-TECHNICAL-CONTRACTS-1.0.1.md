# Evidência técnica SHA-exata — Apprentice's Codex 1.0.1 (piloto OPENCODE)

> Documento de apoio para as cinco fichas do lote piloto. Não é uma ficha de objeto, não certifica hook mutador, configuração instalada, QA físico nem universo integral do provider.

## Identidade do artefato

| Propriedade | Valor verificado |
|---|---|
| Artefato físico | `apprentice_codex-1.0.1-mc1.21.1.jar` |
| Tamanho | 11.757.447 bytes |
| SHA-256 | `47018AD8C6C6187B17C6BFC4D4F2FFF44EA2ED560719EBB6566A750715757947` |
| SHA-1 | `3077999F51299A53A0AF1B8A1AEC22F4099E36A3` |
| Mod ID | `apprenticecodex` |
| Minecraft / loader | 1.21.1 / NeoForge `21.1.250` |
| Java usado na inspeção | JDK `21.0.12` (`java`, `javac`, `jar`) |
| Instância autorizada | `MODS_PATH.txt` → pasta `mods` indicada pelo usuário; 590 JARs; somente leitura |
| Base do catálogo | `Gustavaopere/Black-Arcana@main` = `c7e8959621c318e433f7b90d5897785aa224a8c1` |

A versão declarada coincide com o artefato físico inspecionado. Evidência anterior `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1) **não** é reaproveitada como certificação destas fichas; ela permanece apenas como histórico documental.

## Comandos e resultados efetivamente executados

1. `Get-FileHash -Algorithm SHA256 -LiteralPath <JAR>` e hash SHA-1 — produzem os hashes acima.
2. `jar tf <JAR>` — inventário de entradas; presença das classes listadas abaixo confirmada.
3. `javap -classpath <JAR> -p -s -c <13 classes decisivas>` — saída gravada em `scratch/javap_check.txt`, `EXIT=0`, 347.597 bytes. Contém descriptors e bytecode com offsets.
4. Vineflower `1.12.0` — decompilação de apoio, saída em `scratch/vf_apprentice3/`, `EXIT=0`, 114 arquivos `.java`. Constantes e fórmulas decisivas foram confrontadas com o `javap`; quando uma constante positiva e uma aceleração negativa aparecem separadamente, o consumo real no bytecode define o efeito.
5. `javap -classpath <apprentice>;<irons>;<irons_lib> -p -s -c <7 classes de config/efeito/helper/mixin de Mist Form>` — saída em `scratch/javap_mistform.txt`, `EXIT=0`, 35.264 bytes.
6. `javap -classpath <apprentice>;<irons>;<irons_lib> -p -v <3 mixins de Mist Form>` — saída em `scratch/javap_mistform_v.txt`, `EXIT=0`, 35.173 bytes; contém `@Mixin`, `@Inject`, método-alvo, ponto `RETURN`/`HEAD` e `cancellable=true`.
7. `jar xf <apprentice> mixins.apprenticecodex.json`, com saída em `scratch/mistmix/` — `EXIT=0`, 4.832 bytes. O refmap `mixins.apprenticecodex.refmap.json` não estava presente no JAR; nenhuma inferência foi feita a partir dele.
8. `javap -classpath <irons>;<irons_lib>;<apprentice> -p -s -c io.redspace.ironsspellbooks.api.spells.AbstractSpell` — saída em `scratch/javap_irons_abstractspell.txt`, `EXIT=0`, 87.671 bytes.

Os comandos 2–4 foram executados na sessão anterior a este checkpoint; os comandos 5–8 foram executados nesta retomada. Todos os artefatos de saída permanecem em `scratch/`. Nenhum JAR foi modificado ou executado; a extração limitou-se ao JSON de mixins dentro de `scratch/`.

## Classes inspecionadas (escopo relevante ao lote)

- Registro/fluxo comum: `jp.aquafactory.apprenticecodex.registry.SpellRegistry`, `jp.aquafactory.apprenticecodex.config.ApprenticeCodexServerConfig`, `jp.aquafactory.apprenticecodex.config.DamageMultiplierServerConfig`, `jp.aquafactory.apprenticecodex.damage.DamageTypes`.
- Blood Brand: `spell.bloodbrand.BloodBrand`, `BloodBrandKunai`, `BloodBrandBurst`, `BloodBrandEvents`, `BloodBrandState`.
- Higanbana: `spell.higanbana.Higanbana`, `HiganbanaKatanaEntity`, `HiganbanaLifestealEvent`.
- Mist Form: `spell.mistform.MistForm`, `MistFormEffect`, `MistFormEvents`, `MistFormCollisionHelper`, `MistFormMovementRestrictionHelper`.
- Deep Sensor: `spell.deepsensor.DeepSensor`, `SenseSensorVibrationEvent`, `DeepSensorObservationBuffer`, `DeepSensorClientDisplay`, `effect.SenseSensor`.
- Echo Cast: `spell.echocast.EchoCast`, `effect.EchoSpell`, `item.multicastechostaff.MulticastEchoStaffCastHelper`, `MulticastEchoStaffAttackHandler`, `MulticastEchoStaffAttackProfile`, `config.item.MulticastEchoStaffServerConfig`.
- Mist Form — evidência adicional: `config.spell.MistFormServerConfig`, `mixin.BlockStateBaseMistFormCollisionMixin`, `mixin.EntityMistFormMovementRestrictionMixin`, `mixin.LivingEntityMistFormMixin` e `mixins.apprenticecodex.json`.

## Contrato herdado do Iron's — coeficientes declarados vs. fórmula efetiva

Artefato físico do host: `irons_spellbooks-1.21.1-3.16.4.jar`, 13.900.016 bytes, SHA-256 `C4DB1ACE9DC8B7440E53186C1F481D967AF23A936ABBCCA372F6317CD354F9FD`. Classe: `io.redspace.ironsspellbooks.api.spells.AbstractSpell`.

| Método | Descriptor | Offsets | Fluxo verificado no bytecode |
|---|---|---|---|
| `getManaCost(int)` | `(I)I` | 0–29 | Lê `baseManaCost` e `manaCostPerLevel`, calcula `base + per*(level-1)`, converte para `double`, multiplica por `SpellConfigParameter.MANA_MULTIPLIER` via `SpellConfigManager` e trunca com `d2i`. |
| `getSpellCooldown()` | `()I` | 0–18 | Lê `COOLDOWN_IN_SECONDS` via `SpellConfigManager`, multiplica por `20.0d` e trunca com `d2i`. |
| `getCastTime(int)` | `(I)I` | 0–16 | Retorna `0` quando `getCastType() == CastType.INSTANT`; caso contrário retorna o campo `castTime`. |
| `getSpellPower(int,Entity)` | `(ILnet/minecraft/world/entity/Entity;)F` | 0–79 | Calcula `baseSpellPower + spellPowerPerLevel*(level-1)` e multiplica por `AttributeRegistry.SPELL_POWER`, `SchoolType.getPowerFor(LivingEntity)` e `SpellConfigParameter.POWER_MULTIPLIER`. Se o caster não for `LivingEntity`, os dois fatores de atributo/escola permanecem `1.0`. |
| `getLevelFor(int,LivingEntity)` | `(ILnet/minecraft/world/entity/LivingEntity;)I` | 0–64 | Soma bônus de `CuriosApi`, posta `ModifySpellLevelEvent` em `NeoForge.EVENT_BUS` e retorna `event.getLevel()`. |
| `getMinRarity()`, `getMaxLevel()`, `getSchoolType()` | `()I`, `()I`, `()Lio/redspace/ironsspellbooks/api/spells/SchoolType;` | 108–126, 194–201 | Leem `SpellConfigManager`, não apenas o `DefaultConfig` declarado pela magia. |

Consequência para as cinco fichas: `baseManaCost`, `manaCostPerLevel`, `baseSpellPower`, `spellPowerPerLevel`, `castTime` e `cooldownSeconds` são **coeficientes declarados** pelo Apprentice Codex. O mana, o cooldown, o power, o nível efetivo, a raridade mínima, o nível máximo e a escola efetivos são produzidos pelo host e podem ser alterados por config do Iron's, atributos, Curios e eventos. Os valores instalados nesses canais não foram lidos; portanto não são afirmados.

## Callsites SHA-exatos de Mist Form

`mixins.apprenticecodex.json` registra `BlockStateBaseMistFormCollisionMixin` (linha 41), `EntityMistFormMovementRestrictionMixin` (linha 44) e `LivingEntityMistFormMixin` (linha 67), com `injectors.defaultRequire=1`.

| Mixin e alvo | Anotação verificada | Bytecode do callback | Efeito |
|---|---|---|---|
| `BlockStateBaseMistFormCollisionMixin` → `BlockBehaviour$BlockStateBase` | `@Inject(method="getCollisionShape(Lnet/minecraft/world/level/BlockGetter;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/phys/shapes/CollisionContext;)Lnet/minecraft/world/phys/shapes/VoxelShape;", at=@At("RETURN"), cancellable=true)` | `apprenticecodex$removeMistFormPassableCollision(...)`, offsets 0–33: só atua se a forma retornada não estiver vazia; chama `asState()` e `MistFormCollisionHelper.canPassThrough(BlockState,CollisionContext)`; quando verdadeiro, `setReturnValue(Shapes.empty())`. | Colisão do bloco é removida para o jogador com o efeito e bloco passável não denylisted. |
| `EntityMistFormMovementRestrictionMixin` → `Entity` | `@Inject(method="makeStuckInBlock", at=@At("HEAD"), cancellable=true)` | `apprenticecodex$ignoreMistFormMovementRestriction(BlockState,Vec3,CallbackInfo)`, offsets 0–15: chama `MistFormMovementRestrictionHelper.ignoresMovementRestriction(Entity,BlockState)` e, quando verdadeiro, `CallbackInfo.cancel()`. | A restrição de movimento do bloco é ignorada. |
| `LivingEntityMistFormMixin` → `LivingEntity` | `@Inject(method="getJumpBoostPower", at=@At("RETURN"), cancellable=true)` | `apprenticecodex$addMistFormJumpPower(CallbackInfoReturnable<Float>)`, offsets 0–44: exige `LivingEntity` com `EffectRegistry.MIST_FORM`, lê o retorno, soma literal `0.3f` e `setReturnValue(...)`. | Bônus efetivo de pulo `+0.3`. |
| `LivingEntityMistFormMixin` → `LivingEntity` | `@Inject(method="canStandOnFluid", at=@At("HEAD"), cancellable=true)` | `apprenticecodex$standOnFluidInMistForm(FluidState,CallbackInfoReturnable<Boolean>)`, offsets 0–48: ignora fluido vazio; para `Player`, aceita `MistFormEvents.canStandOnFluid` ou `LongStrideFluidMovement.canStandOnFluid` e força retorno `true`. | Suporte em fluido compartilhado com Long Stride. |

`MistFormCollisionHelper.canPassThrough` tem descriptor `(Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/world/phys/shapes/CollisionContext;)Z`; seus offsets 0–69 exigem `EntityCollisionContext` com entidade `Player`, efeito `MIST_FORM`, tag `TagRegistry.Blocks.MIST_FORM_PASSABLE` e ausência na denylist via `ApprenticeCodexServerConfig.isMistFormPassableBlockDenied(BlockState)`. `MistFormMovementRestrictionHelper.ignoresMovementRestriction` tem descriptor `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/level/block/state/BlockState;)Z`; offsets 0–37 exigem `Player` com o efeito e tag `TagRegistry.Blocks.MIST_FORM_IGNORES_MOVEMENT_RESTRICTION`.

`MistFormEffect.JUMP_POWER_ADDITION` está declarado como `float` com valor `0.3F` na fonte de apoio. Nas classes inspecionadas, o mixin consome um literal `0.3f`, não uma leitura do campo; por isso o bônus efetivo é afirmado pelo callback, e a constante é registrada separadamente como declaração auxiliar. `MistFormServerConfig.define` cria a seção `MistForm` com `passableBlockDenylist` padrão vazio e `setPassableBlockDenylistForGameTest`; o cache aceita IDs de bloco e entradas `#tag`. O valor instalado da denylist continua **NÃO VERIFICADO**.

## Âncoras determinísticas por objeto

| Objeto | Métodos/constantes verificados no bytecode ou fonte correspondente |
|---|---|
| Blood Brand | `BloodBrand.<init>()`: `baseSpellPower=100`, `spellPowerPerLevel=75`, `baseManaCost=35`, `manaCostPerLevel=10`, `castTime=0`; `DefaultConfig`: `maxLevel=5`, `cooldown=4.0`, `minRarity=RARE`, escola BLOOD; `CastType.INSTANT`; `getDamage()` = `(1 + spellPower/100) * damageMultiplier(BLOOD_BRAND)`; `getExplodeDamage()` = `(8*spellPower/100) * damageMultiplier(BLOOD_BRAND)`; `getExplodeRange()` = `5`; `onCast()` semeia `BloodBrandKunai` apenas em `ServerLevel`. |
| Higanbana | `DefaultConfig`: `COMMON`, `maxLevel=5`, `cooldown=4.0`; `baseSpellPower=100`, `spellPowerPerLevel=100`, `baseManaCost=40`, `manaCostPerLevel=20`, `castTime=0`; `getSlashCount()=4`; `getRange()` delega a `HiganbanaKatanaEntity.getAttackDepth()`; `ATTACK_HALF_WIDTH=2.5`, `ATTACK_DEPTH=2.5`, `getAttackDepth()=3.4`; `getDamage()` = `(1 + spellPower/100) * damageMultiplier(HIGANBANA)`. |
| Mist Form | `DefaultConfig`: `EPIC`, `maxLevel=3`, `cooldown=30.0`, `CastType.LONG`; `baseSpellPower=50`, `spellPowerPerLevel=15`, `baseManaCost=150`, `manaCostPerLevel=30`, `castTime=30`; duração `Math.round(200*spellPower/100)`; raio de supressão `32.0`; `MOVEMENT_SPEED_BONUS=0.2`, `STEP_HEIGHT_ADDITION=0.5`, `SCHOOL_RESIST_WEAKNESS=-1.0`, `JUMP_POWER_ADDITION=0.3F`. |
| Deep Sensor | `DefaultConfig`: `LEGENDARY`, `maxLevel=3`, `cooldown=100.0`, `CastType.INSTANT`; `baseSpellPower=100`, `spellPowerPerLevel=50`, `baseManaCost=60`, `manaCostPerLevel=20`, `castTime=0`; listener raio `24`; duração `Math.round(spellPower*6)`; buffer `40` ticks / `64` registros / `8` exibidos. |
| Echo Cast | `DefaultConfig`: `LEGENDARY`, `maxLevel=1`, `cooldown=0.0`, `CastType.LONG`, `setAllowCrafting(false)`, `requiresLearning=false`, `allowLooting=false`; `baseSpellPower=0`, `baseManaCost=50`, `castTime=20`; `EchoSpell.DURATION_TICKS=300`; staff obrigatório em mainhand ou offhand. |

## Relações de valores e escopo

- **Gravidade do kunai:** `GRAVITY = 0.03` é uma magnitude positiva declarada. Em `BloodBrandKunai.tick()`, o movimento é escalado por `0.99` e, quando `!isNoGravity()`, recebe `Vec3.add(0.0, -0.03d, 0.0)`. A aceleração vertical efetiva é, portanto, **-0.03 bloco/tick²**; a constante positiva e a aceleração negativa são grandezas distintas, não uma divergência comprovada entre decompiler e bytecode. Nenhum consumo de `GRAVITY` foi demonstrado nas classes inspecionadas; o literal negativo é o que produz o efeito.
- **Profundidade do Higanbana:** `ATTACK_DEPTH = 2.5` e a caixa construída é `2.5 × 0.75 × 2.5`, porém `getAttackDepth()` retorna `3.4`; `Higanbana.getRange()` consome o getter, não a constante. Ambos os valores são registrados com seus consumidores distintos.
- 0.9.7.1 vs 1.0.1: todas as afirmações numéricas foram reancoradas no JAR 1.0.1; nenhum valor antigo foi promovido sem confirmação no artefato atual.
- **Mist Form:** os três mixins e seus alvos foram verificados no JAR 1.0.1; são contratos provider-owned de leitura/mutação do vanilla, não hooks externos seguros para perk. O bônus de pulo é aplicado por callback, sem consumer demonstrado da constante `JUMP_POWER_ADDITION`.

## Reavaliação dos certificados

Os cinco certificados `COMPLETE_PERK_READY` foram reavaliados contra a semântica canônica. Todos permanecem estritamente `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, com `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`. Nenhum foi promovido a homologação de hook, QA física, configuração efetiva, universo integral do provider ou implementação na `main`. As correções desta etapa reduzem afirmações indevidas (gravidade e pendências de Mist Form) e acrescentam o contrato herdado do Iron's; não aumentam o grau de certificação.

## Limites da prova

- Grau: `SHA_EXACT_BINARY_BEHAVIOR` no escopo das classes/métodos listados. Não equivale a equivalência integral de todos os métodos do mod.
- `mutating_hook = NOT_VERIFIED`: nenhum evento, setter, mixin ou adapter foi demonstrado como ponto seguro e autorizado de mutação por perk. Onde não há contrato demonstrado, aplica-se `NO_MUTATION` e fail-closed.
- `physical_qa = NOT_TESTED`: nenhum teste em cliente, servidor dedicado, Survival, PvP ou modpack foi executado.
- Configuração efetiva do pack (multiplicadores de dano, delay/caps do echo, lista de blocos phasing) não foi lida; apenas defaults de código são afirmados.
- Universo semântico integral do provider não foi encerrado. O recorte observado é de cinco fichas.
