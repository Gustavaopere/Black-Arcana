# Evidência técnica SHA-exata — Apprentice's Codex 1.0.1.1 (lote OPENCODE de dez fichas)

> Documento de apoio às dez fichas reancoradas do lote. Não é uma ficha de objeto. Não certifica hook mutador, configuração instalada, QA físico, universo semântico integral do provider nem implementação na `main`.

## Identidade do artefato

| Propriedade | Valor verificado |
|---|---|
| Artefato físico | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| Tamanho | 11.870.671 bytes |
| SHA-256 | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| `LastWriteTimeUtc` | `2026-11-27T18:13:26Z` |
| Mod ID | `apprenticecodex` |
| Versão declarada no `neoforge.mods.toml` | `1.0.1.1` |
| Nome exibido | `Apprentice's Codex` |
| Autor | `Aquid` |
| Minecraft / loader | 1.21.1 / NeoForge (dependência declarada `[21.1.249,)`) |
| Iron's dependency range | `[1.21.1-3.16.3,1.21.1-4.0.0)` |
| Java usado na inspeção | JDK `21.0.12` (`java`, `javac`, `jar`, `javap`) |
| Instância autorizada | `MODS_PATH.txt` → pasta `mods` indicada pelo usuário; somente leitura |
| Base remota do lote | `Gustavaopere/Black-Arcana@main` = `d42a3763ab5fbbb1458c38d668713e29b8d071ec` |
| Branch de trabalho | `catalog/opencode-apprentice-codex-1011-ten-20261127` |

A versão declarada coincide com o artefato físico inspecionado. O dossiê `EXACT-TECHNICAL-CONTRACTS-1.0.1.md` e o source pin `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1) permanecem como histórico documental; **não** são reaproveitados como certificação destas dez fichas. A modlist canônica mais recente contendo `1.0.1.1` não foi localizada no repositório `neoforge-rpg-skilltree`; o pivot foi decidido pelo usuário com base na presença física verificada e na identidade do JAR.

## Comandos e resultados efetivamente executados

1. `Get-Item -LiteralPath <JAR>` + `Get-FileHash -Algorithm SHA256`/`SHA1 -LiteralPath <JAR>` — tamanho, timestamps e hashes acima; saída preservada em `scratch/identity_1011.txt`.
2. `java -version`, `javac -version`, `jar --version`, `javap -help` — JDK `21.0.12`; `javap --version` não é suportado, mas `javap -help` concluiu sem erro.
3. `jar tf <JAR>` — inventário de entradas; saída em `scratch/jar1011_classes.txt` (417.647 bytes). As classes listadas abaixo foram confirmadas no inventário.
4. Extração restrita de `META-INF/neoforge.mods.toml` para `scratch/extract1011/`; mod ID, versão, nome, autor, mixins e dependências lidos sem executar o JAR.
5. `javap -classpath <JAR> -p -s -c <classes decisivas>` — saída em `scratch/javap1011.txt` (1.280.505 bytes), `EXIT=0`.
6. `javap -classpath <JAR> -p -v <classes decisivas>` — saída em `scratch/javap1011_v.txt` (913.844 bytes), `EXIT=0`; contém `ConstantValue` e anotações de mixin quando aplicáveis.
7. Vineflower `1.12.0` (SHA-256 `1DFCFE974395734FA467CE620661C7623D05BA83670DE0529B1FBD63FF548B9D`) — decompilação de apoio em `scratch/vf_apprentice1011/`, `EXIT=0`, 4.118 arquivos `.java`. Constantes e fórmulas decisivas foram confrontadas com `javap`; quando decompiler e bytecode divergem, o bytecode define o efeito.
8. Host: `irons_spellbooks-1.21.1-3.16.4.jar`, 13.900.016 bytes, SHA-256 `C4DB1ACE9DC8B7440E53186C1F481D967AF23A936ABBCCA372F6317CD354F9FD`; `AbstractSpell` inspecionado em `scratch/javap_irons_abstractspell.txt`, `EXIT=0`.

Nenhum JAR foi modificado, renomeado, extraído dentro da pasta autorizada ou executado. As extrações e saídas ficaram apenas em `scratch/`. A extração foi limitada a entradas nomeadas e tratadas como dados.

## Classes inspecionadas

- Registro/comum: `jp.aquafactory.apprenticecodex.registry.SpellRegistry`, `jp.aquafactory.apprenticecodex.config.ApprenticeCodexServerConfig`, `jp.aquafactory.apprenticecodex.config.DamageMultiplierServerConfig`, `jp.aquafactory.apprenticecodex.damage.DamageTypes`, `io.redspace.ironsspellbooks.api.spells.AbstractSpell`.
- Mana Transcription: `spell.manatranscription.ManaTranscription`, `ManaTranscription$ManaTranscriptionCastData`, `ManaTranscriptionLogic` (com `Mode`, `Resolution`, `Candidate`, `Failure`) e JEI helpers.
- Moonlight: `spell.moonlight.MoonLight`, `MoonLightKatanaEntity`, `MoonLightChargeCutEntity`, `MoonLightCounterspellEffect`, `model.MoonLightKatanaModel`.
- Otherworld Lens: `spell.otherworldlens.OtherworldLens`, `OtherworldLensSessionManager`, `OtherworldLensTargetSafety`, `OtherworldLensEvents`, `OtherworldLensBlock`, `OtherworldLensClientController`.
- Palette Shift: `spell.paletteshift.PaletteShift`, `PaletteShiftReceptionEvent`.
- Spectral Wing: `spell.spectralwing.SpectralWing`, `SpectralWingFlightEvent`, `SpectralWingLayer`, `effect.SpectralWingEffect`, `mixin.LivingEntitySpectralWingMixin`.
- Anchor Blink: `spell.anchorblink.AnchorBlink`, `AnchorBlinkDaggerEntity`, `AnchorBlinkEvents`, `network.packet.ClientAnchorBlinkPacket`, `event.client.AnchorBlinkClientInputEvent`.
- Arcane Beam: `spell.arcanebeam.ArcaneBeam`, `ArcaneBeamEntity`, `ArcaneBeamRenderer`. O pacote correto é `spell.arcanebeam`; `spell.arcanabeam` não existe no artefato.
- Arcane Blast: `spell.arcaneblast.ArcaneBlast`.
- Assist Wings: `spell.assistwings.AssistWings`, `AssistWingsWingEntity`, `capability.codexspelldata.spellstates.AssistWingsState`, `network.packet.SyncAssistWingsJumpPacket`, `network.packet.HoverrideBroomAssistWingsJumpPacket`.
- Auto Magnet: `spell.automagnet.AutoMagnet`, `AutoMagnetFamiliarManager`, `AutoMagnetFamiliarEntity`, `AutoMagnetCollectionMode`, `AutoMagnetFamiliarEvents`, `config.spell.AutoMagnetServerConfig`, `capability.codexspelldata.spellstates.AutoMagnetState`.

## Contrato herdado do Iron's — coeficientes declarados vs. fórmula efetiva

Artefato do host indicado acima; classe `io.redspace.ironsspellbooks.api.spells.AbstractSpell`.

| Método | Descriptor | Fluxo verificado no bytecode |
|---|---|---|
| `getManaCost(int)` | `(I)I` | Lê `baseManaCost`/`manaCostPerLevel`, calcula `base + per*(level-1)`, multiplica por `SpellConfigParameter.MANA_MULTIPLIER` via `SpellConfigManager` e trunca. |
| `getSpellCooldown()` | `()I` | Lê `COOLDOWN_IN_SECONDS` via `SpellConfigManager`, multiplica por `20.0d` e trunca. |
| `getCastTime(int)` | `(I)I` | Retorna `0` para `CastType.INSTANT`; caso contrário retorna o campo `castTime`. |
| `getSpellPower(int,Entity)` | `(ILnet/minecraft/world/entity/Entity;)F` | Calcula `base + per*(level-1)` e multiplica por atributo de spell power, escola e `SpellConfigParameter.POWER_MULTIPLIER`. |
| `getLevelFor(int,LivingEntity)` | `(ILnet/minecraft/world/entity/LivingEntity;)I` | Soma bônus de Curios, posta `ModifySpellLevelEvent` e retorna `event.getLevel()`. |
| `getMinRarity()`, `getMaxLevel()`, `getSchoolType()` | `()I`, `()I`, `()Lio/redspace/ironsspellbooks/api/spells/SchoolType;` | Leem `SpellConfigManager`, não apenas o `DefaultConfig` declarado pela magia. |

Consequência: os valores numéricos nas fichas são **coeficientes declarados ou constantes lidas no JAR 1.0.1.1**. Mana efetivo, cooldown efetivo, spell power efetivo, nível efetivo, raridade mínima efetiva, nível máximo efetivo e escola efetiva são produzidos pelo host e podem mudar por config, atributos, Curios e eventos. Os valores instalados nesses canais **não foram lidos** e permanecem `NÃO VERIFICADOS`.

## Âncoras determinísticas por objeto

| Objeto | Constantes, fórmulas e consumidores verificados no JAR 1.0.1.1 |
|---|---|
| Mana Transcription | `DefaultConfig`: LEGENDARY, nível 1, cooldown `4.0`, CastType LONG; construtor: `baseSpellPower=0`, `spellPowerPerLevel=0`, `baseManaCost=500`, `manaCostPerLevel=0`, `castTime=100`. `getEffectiveCastTime` força o próprio `castTime`; dois modos provider-owned (`EXTRACTION`/`RESET`); XP, anti-swap e mutação de itens resolveram no fluxo do próprio provider. |
| Moonlight | `DefaultConfig`: LEGENDARY, nível 3, cooldown `8.0`; `baseSpellPower=1200`, `spellPowerPerLevel=900`, `baseManaCost=120`, `manaCostPerLevel=30`, `castTime=40`; dano `spellPower/100 * MOON_LIGHT`; alcance `8+(level-1)*8`; uninterruptible; standby `max(0, ceil(10/max(1,scale)))` como delay inicial `STANDBY_START_DELAY_TICK=10` escalado pela duração efetiva. Katana + `MoonLightChargeCutEntity` + counterspell pertencem à mesma raiz. |
| Otherworld Lens | `DefaultConfig`: LEGENDARY, nível 1, cooldown `5.0`; `baseManaCost=35`, `castTime=300`, targeting range `8`; `OtherworldLensSessionManager.KEEP_RANGE_SQ=144.0` (`12²`); sessão UUID server-owned, validação de bloco/face/ar e raycast de revalidação. Temp view surface, não portal persistente. |
| Palette Shift | `DefaultConfig`: LEGENDARY, nível 1, cooldown `30.0`, `allowCrafting=false`; `baseManaCost=50`, `castTime=0`; `requiresLearning()=false`; `PALETTE_RECEPTION` por `600` ticks; exige Pastel Staff em mão principal ou secundária; `PaletteShiftReceptionEvent` em `HIGHEST` consome o próximo cast ao modificar staff. |
| Spectral Wing | `DefaultConfig`: LEGENDARY, nível 1, cooldown `2.0`; `baseManaCost=150`, `castTime=0`; `LAUNCH_HORIZONTAL_SPEED=0.75`, `LAUNCH_VERTICAL_SPEED=1.05`, `BOOST_SPEED=2.75`, `BOOST_UPWARD_SPEED=0.22`, `BOOST_SPIN_TICKS=10`, `VISUAL_EFFECT_DURATION_TICKS=20`, `START_GRACE_TICKS=10`; `WATER_DEACTIVATE_GRACE_TICKS=4`. Launch/glide/recast boost são uma raiz. |
| Anchor Blink | `DefaultConfig`: EPIC, nível 1, cooldown `30.0`, `allowCrafting=false`, `allowLooting=false`; `baseSpellPower=400`, `spellPowerPerLevel=200`, `baseManaCost=80`, `castTime=10`, `getEffectiveCastTime` ignora redução; dano da daga `power/100*multiplier`; velocidade `1.8`; alcance `min(128,16*power/100)`; dagger `MAX_FLIGHT_TICKS=160`, `IMPACT_LIFETIME_TICKS=60`, `POST_BLINK_PROTECTION_TICKS=40`. |
| Arcane Beam | `DefaultConfig`: RARE, nível 5, cooldown `12.0`; `baseSpellPower=200`, `spellPowerPerLevel=100`, `baseManaCost=5`, `manaCostPerLevel=5`, `castTime=60`; range `32`, raio `0.25`; dano base `(1+power/100)*multiplier`; bônus por charge `round((power-100)/30)*(amplifier+1)`; `ArcaneBeamEntity.tick` usa `tickCount % 5 != 0` → 4 ticks de dano em cada 5 ticks, sem dedup de vítima por cast no método examinado. |
| Arcane Blast | `DefaultConfig`: COMMON, nível 10, cooldown `1.0`; `baseSpellPower=40`, `spellPowerPerLevel=5`, `baseManaCost=20`, `manaCostPerLevel=4`, `castTime=30`; `RAYCAST_WIDTH=0.1`; dano `power/10*ARCANE_BLAST`; alcance `16+4*power/10`; `ARCANE_CHARGE` `200` ticks, amp cap `2`; charge não é novo cast. |
| Assist Wings | `DefaultConfig`: RARE, nível 3, cooldown `0.0`; `baseSpellPower=100`, `spellPowerPerLevel=100`, `baseManaCost=20`, `castTime=0`; saltos `1+level` (2/3/4); impulso vertical `0.6+jumpBoostPower`; gate de montaria Hoverride Broom; wing entity com `REMOVAL_GRACE_TICKS=10`. |
| Auto Magnet | `DefaultConfig`: COMMON, nível 5, cooldown `0.0`; `baseSpellPower=100`, `spellPowerPerLevel=25`, `baseManaCost=40`, `manaCostPerLevel=10`, `castTime=0`; range `8+(level-1)*4`; `getCollectMana()` `0.0` ou `10.0` conforme `AutoMagnetServerConfig.disableCollectManaCost` (default `false`); familiar órbita `1.4`, altura `1.2`, velocidade angular `0.06981317007977318`, `COLLECT_INTERVAL_TICK=2`. Coleta de XP é passagem separada, sem chamada de `tryConsumeCollectMana` nela. |

## Correções, divergências e limites

- O pacote de Arcane Beam no artefato é `jp.aquafactory.apprenticecodex.spell.arcanebeam`; a forma `spell.arcanabeam` não existe. As fichas foram corrigidas para o pacote real.
- A cadência de Arcane Beam é afirmada pelo bytecode (`tickCount % 5 != 0`), não pelo comentário de código. QA de DPS real continua pendente.
- Otherworld Lens conserva o alcance de placement `8` e o raio de manutenção `12` (`KEEP_RANGE_SQ=144.0`) como grandezas distintas, com consumidores distintos.
- Mana Transcription mantém XP/anti-swap/mutação de itens como transação provider-owned. O source 0.9.7.1 é histórico; a análise atual é do JAR 1.0.1.1.
- Auto Magnet: o custo de coleta é uma cobrança por rodada de itens, não por stack; a passe de XP não chama `tryConsumeCollectMana` no caminho examinado. Isso não prova pickup final nem eventos externos.
- Fórmulas de mana/cooldown/cast time/spell power herdadas de `AbstractSpell` não são valores efetivos instalados. Configuração efetiva do pack e multiplicadores de dano instalados permanecem `NÃO VERIFICADOS`.
- Nenhuma afirmação de QA física, hook mutador seguro, universo semântico encerrado ou implementação na `main` foi promovida. Onde não há contrato mutador demonstrado, aplica-se `NO_MUTATION` e fail-closed.

## Reavaliação dos certificados

As dez fichas deste lote permanecem estritamente `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, com `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`. A reancoragem substitui afirmações source-level 0.9.7.1 por evidência bytecode/decompilação do JAR físico 1.0.1.1, mas **não aumenta** o grau de certificação. Os cinco certificados do dossiê 1.0.1 foram preservados como histórico; o pivot deste lote não os reescreve.

## Estado explícito dos gates

- `STATIC_TECHNICAL_CATALOG_ONLY`: **SIM**, no recorte das dez raízes e classes listadas.
- `SHA_EXACT_BINARY_BEHAVIOR`: **SIM**, no escopo das classes/métodos/constantes listados.
- `mutating_hook=NOT_VERIFIED`: **SIM**; nenhum ponto seguro de mutação por perk foi demonstrado.
- `physical_qa=NOT_TESTED`: **SIM**; nenhum teste em cliente, servidor dedicado, Survival, PvP ou modpack foi executado.
- `implementation_in_main=NOT_APPLICABLE`: **SIM**; este lote não implementa magias, perks nem adapters.
