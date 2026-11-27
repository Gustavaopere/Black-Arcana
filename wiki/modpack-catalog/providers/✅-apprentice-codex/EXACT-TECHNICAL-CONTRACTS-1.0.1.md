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
4. Vineflower `1.12.0` — decompilação de apoio, saída em `scratch/vf_apprentice3/`, `EXIT=0`, 114 arquivos `.java`. Toda constante decisiva foi confrontada com o `javap`; quando há divergência, o bytecode prevalece.

Os comandos 2–4 foram executados na sessão anterior a este checkpoint e seus artefatos de saída permanecem em `scratch/`; nenhum deles foi reexecutado nesta retomada. Nenhum JAR foi modificado, extraído dentro da pasta autorizada ou executado.

## Classes inspecionadas (escopo relevante ao lote)

- Registro/fluxo comum: `jp.aquafactory.apprenticecodex.registry.SpellRegistry`, `jp.aquafactory.apprenticecodex.config.ApprenticeCodexServerConfig`, `jp.aquafactory.apprenticecodex.config.DamageMultiplierServerConfig`, `jp.aquafactory.apprenticecodex.damage.DamageTypes`.
- Blood Brand: `spell.bloodbrand.BloodBrand`, `BloodBrandKunai`, `BloodBrandBurst`, `BloodBrandEvents`, `BloodBrandState`.
- Higanbana: `spell.higanbana.Higanbana`, `HiganbanaKatanaEntity`, `HiganbanaLifestealEvent`.
- Mist Form: `spell.mistform.MistForm`, `MistFormEffect`, `MistFormEvents`, `MistFormCollisionHelper`, `MistFormMovementRestrictionHelper`.
- Deep Sensor: `spell.deepsensor.DeepSensor`, `SenseSensorVibrationEvent`, `DeepSensorObservationBuffer`, `DeepSensorClientDisplay`, `effect.SenseSensor`.
- Echo Cast: `spell.echocast.EchoCast`, `effect.EchoSpell`, `item.multicastechostaff.MulticastEchoStaffCastHelper`, `MulticastEchoStaffAttackHandler`, `MulticastEchoStaffAttackProfile`, `config.item.MulticastEchoStaffServerConfig`.

## Âncoras determinísticas por objeto

| Objeto | Métodos/constantes verificados no bytecode ou fonte correspondente |
|---|---|
| Blood Brand | `BloodBrand.<init>()`: `baseSpellPower=100`, `spellPowerPerLevel=75`, `baseManaCost=35`, `manaCostPerLevel=10`, `castTime=0`; `DefaultConfig`: `maxLevel=5`, `cooldown=4.0`, `minRarity=RARE`, escola BLOOD; `CastType.INSTANT`; `getDamage()` = `(1 + spellPower/100) * damageMultiplier(BLOOD_BRAND)`; `getExplodeDamage()` = `(8*spellPower/100) * damageMultiplier(BLOOD_BRAND)`; `getExplodeRange()` = `5`; `onCast()` semeia `BloodBrandKunai` apenas em `ServerLevel`. |
| Higanbana | `DefaultConfig`: `COMMON`, `maxLevel=5`, `cooldown=4.0`; `baseSpellPower=100`, `spellPowerPerLevel=100`, `baseManaCost=40`, `manaCostPerLevel=20`, `castTime=0`; `getSlashCount()=4`; `getRange()` delega a `HiganbanaKatanaEntity.getAttackDepth()`; `ATTACK_HALF_WIDTH=2.5`, `ATTACK_DEPTH=2.5`, `getAttackDepth()=3.4`; `getDamage()` = `(1 + spellPower/100) * damageMultiplier(HIGANBANA)`. |
| Mist Form | `DefaultConfig`: `EPIC`, `maxLevel=3`, `cooldown=30.0`, `CastType.LONG`; `baseSpellPower=50`, `spellPowerPerLevel=15`, `baseManaCost=150`, `manaCostPerLevel=30`, `castTime=30`; duração `Math.round(200*spellPower/100)`; raio de supressão `32.0`; `MOVEMENT_SPEED_BONUS=0.2`, `STEP_HEIGHT_ADDITION=0.5`, `SCHOOL_RESIST_WEAKNESS=-1.0`, `JUMP_POWER_ADDITION=0.3F`. |
| Deep Sensor | `DefaultConfig`: `LEGENDARY`, `maxLevel=3`, `cooldown=100.0`, `CastType.INSTANT`; `baseSpellPower=100`, `spellPowerPerLevel=50`, `baseManaCost=60`, `manaCostPerLevel=20`, `castTime=0`; listener raio `24`; duração `Math.round(spellPower*6)`; buffer `40` ticks / `64` registros / `8` exibidos. |
| Echo Cast | `DefaultConfig`: `LEGENDARY`, `maxLevel=1`, `cooldown=0.0`, `CastType.LONG`, `setAllowCrafting(false)`, `requiresLearning=false`, `allowLooting=false`; `baseSpellPower=0`, `baseManaCost=50`, `castTime=20`; `EchoSpell.DURATION_TICKS=300`; staff obrigatório em mainhand ou offhand. |

## Divergências detectadas

- **Gravidade do kunai:** a decompilação exibe `private static final double GRAVITY = 0.03;`, mas o `javap -c` mostra, em `BloodBrandKunai.tick()`, `Vec3.add(0.0, -0.03d, 0.0)` aplicado somente quando `!isNoGravity()`. O valor efetivo documentado é **-0.03 bloco/tick²**; a ficha registra a divergência de sinal.
- **Profundidade do Higanbana:** `ATTACK_DEPTH = 2.5` e a caixa construída é `2.5 × 0.75 × 2.5`, porém `getAttackDepth()` retorna `3.4`; `Higanbana.getRange()` consome o getter, não a constante. Ambos os valores são registrados com seus consumidores distintos.
- 0.9.7.1 vs 1.0.1: todas as afirmações numéricas foram reancoradas no JAR 1.0.1; nenhum valor antigo foi promovido sem confirmação no artefato atual.

## Limites da prova

- Grau: `SHA_EXACT_BINARY_BEHAVIOR` no escopo das classes/métodos listados. Não equivale a equivalência integral de todos os métodos do mod.
- `mutating_hook = NOT_VERIFIED`: nenhum evento, setter, mixin ou adapter foi demonstrado como ponto seguro e autorizado de mutação por perk. Onde não há contrato demonstrado, aplica-se `NO_MUTATION` e fail-closed.
- `physical_qa = NOT_TESTED`: nenhum teste em cliente, servidor dedicado, Survival, PvP ou modpack foi executado.
- Configuração efetiva do pack (multiplicadores de dano, delay/caps do echo, lista de blocos phasing) não foi lida; apenas defaults de código são afirmados.
- Universo semântico integral do provider não foi encerrado. O recorte observado é de cinco fichas.
