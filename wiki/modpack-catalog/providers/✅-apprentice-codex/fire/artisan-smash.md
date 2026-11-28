# Artisan Smash

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:artisan_smash` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<ArtisanSmashLauncherEntity>`) |
| Interfaces | `IMagiAgentSuitAffectedSpell`; launcher `SummonWeaponEntity`, shell `ThrowableProjectile`/`AntiMagicSusceptible`/`CombatOwnerUuidHolder` e preview de trajetória pertencem à raiz |
| Escola | `SchoolRegistry.FIRE_RESOURCE` (Fire) |
| Raridade mínima declarada | `RARE` |
| Níveis declarados | 1–3 (`setMaxLevel(3)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `8.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=40`, `manaCostPerLevel=20`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.artisansmash.ArtisanSmash` |
| Auxiliares da mesma raiz | `ArtisanSmashLauncherEntity`, `ArtisanSmashShellEntity`, `ArtisanSmashTrajectoryPreviewRenderEvent`, `DamageTypes.ARTISAN_SMASH` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("artisan_smash", ArtisanSmash::new)` |
| Config | `RARE`, nível 3, cooldown `8.0`, `FIRE_RESOURCE`, `CastType.LONG` |
| Coeficientes | <init>: `baseSpellPower=900`, `spellPowerPerLevel=400`, `baseManaCost=40`, `manaCostPerLevel=20`, `castTime=30` |
| Dano | `getDamage` → `power/100 * damageMultiplier(ARTISAN_SMASH)` |
| Raio | `getSplashRadius` → `min(2 + power/600, 8)` |
| Velocidade | `getSpeed()` → `1.5F`, passada por `setSpeed` ao launcher e ao `setup` da shell |
| Launcher | `MAX_RECOIL_TICK=10`, `FIRE_OFFSET=0.75`, pitch `owner.getXRot()-15.0F`, standby `calculateBehindPosition(owner,-0.5,-0.7,-0.25)` |
| Shell | `MAX_LIFE_TICKS=200`, `BURST_TICKS=14`, `BURST_CUBE_SIZE_SCALE=2.0F`; `FLIGHT_AIR_DRAG=0.99` é constante declarada, sem consumidor identificado no corpo examinado |
| Explosão | `AABB(center,center).inflate(splashRadius)`, `CombatTargetPolicy.ALLOW_SELF_PROTECT_ALLIES`, dedupe por `Entity.getId()`, `clip` de `COLLIDER` para oclusão |

Bytecode: scratch/fire5_evidence/javap1011_fire6.txt (`javap -classpath <JAR> -p -s -c`, 28 classes, 1.095.867 bytes, EXIT=0, SHA-256 `F5491A50DCF3A8F7EBF1E9C035EFE0723490C97475DE501FC3AF6C1580E17EDB`, SHA-1 `53C2C327705603172618C84CFFEFC41412683190`); decompilação de apoio: scratch/fire5_sources.txt (fontes Vineflower 1.12.0 das cinco raízes legadas e auxiliares, 188.994 bytes, SHA-256 `F8BE6DF48A22522FC1B23FBA362D8FD0F2637A2759D65739F25A723A2903A448`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCastNoWeapon` cria a launcher, aplica dano, raio e velocidade e a adiciona ao nível; `onCastTickWithWeapon` atualiza o dano durante o cast.
2. `prepareWeaponForRelease` chama `prepareForFire`, que segue `calculateBehindPosition(owner,-0.5,-0.7,-0.25)` e aplica pitch `owner.getXRot()-15.0F` com clamp `-90..90`.
3. `onCastCompleteWithWeapon`: cast não cancelado reaplica dano/raio, chama `fire` e retorna `KEEP_WEAPON`; cancelado retorna `RELEASE_WEAPON` sem disparar.
4. `fire` cria a shell na posição da launcher `+ direction*0.75`, chama `setup(damage, radius, direction, 1.5)` e marca `recoilTick=10`/`isReleased=true`.
5. `tickOnServer` decrementa o recuo e descarta a launcher ao chegar a zero; sem dono vivo, descarta imediatamente.
6. A shell colide com entidade válida ou bloco, entra na fase de burst, aplica dano uma única vez em AABB e é descartada após `14` ticks; sem colisão, expira em `200` ticks.
7. `onAntiMagic` descarta a shell antes do burst; `DamageTypes.ARTISAN_SMASH` e `SpellRegistry.ARTISAN_SMASH` são usados na aplicação.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo de impacto | Entidade válida ou bloco atingido pela shell em voo |
| Filtro | `canHitEntity` exclui owner e combat owner, resolve `resolutePartEntity` e exige `isValidCombatTarget` |
| Área | AABB cúbica inflada por `splashRadius = min(2 + power/600, 8)` |
| Oclusão | `isBlockedByWall` faz `clip` de `center` ao olho/centro do alvo e suprime o dano se houver bloco |
| Knockback | `KnockbackTypes.DEFAULT` no dano de área |
| Tempo | voo até `200` ticks; burst `14` ticks; launcher `10` ticks de recuo |
| Persistência | launcher e shell serializam `Damage`, `SplashRadius`, `Speed`, fase/contadores e `combatOwnerUuid` em NBT |

## 5. Resultado

- Dano de explosão em área com tipo `DamageTypes.ARTISAN_SMASH`, aplicado por `CombatTools.applySpellDamage`.
- Um mesmo alvo é atingido no máximo uma vez por explosão (`damagedIds.add(target.getId())`).
- Aliados são protegidos pela política `ALLOW_SELF_PROTECT_ALLIES`; `NO_KNOCKBACK` não é usado aqui.
- Sem cura, status, invocação múltipla ou AOE persistente (`N/A` com justificativa: a explosão é instantânea e a shell é descartada).

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `900 + 400*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Dano | `power/100 * damageMultiplier(ARTISAN_SMASH)` — config **NÃO VERIFICADA** |
| Raio | `min(2 + power/600, 8)` blocos, clamp superior `8` |
| Mana | `40 + 20*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `8.0` s declarado; efetivo **NÃO VERIFICADO** |
| Cast time | `30` ticks no construtor, com `CastType.LONG` |
| Velocidade | `1.5` blocos/tick em `setup`; `FLIGHT_AIR_DRAG=0.99` permanece sem consumidor demonstrado |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano e raio respondem a `getSpellPower`; atributos escolares reais do host permanecem **NÃO VERIFICADOS**.
- **B — evento verificado:** `ArtisanSmashTrajectoryPreviewRenderEvent` é apresentação de mira, não contrato de mutação.
- **C — adapter condicionado:** alterar raio, velocidade ou política de aliados exigiria substituir a shell/launcher com risco de duplicar explosão. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura comprovada para transformar a explosão em AOE persistente ou mudar a oclusão sem duplicar dano. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast longo → launcher em standby → shell 1.5 blocos/tick → colisão → explosão AABB com dedupe e política de aliados → burst 14 ticks e descarte`.

## 9. Concepção de nova magia

Assinatura ocupada: lançador conjurado que dispara um projétil explosivo de área com raio escalado por poder. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `900/400/40/20/30`, `RARE/3/8.0`, dano `power/100*multiplier`, raio `min(2+power/600,8)`, velocidade `1.5`, standby/pitch, NBT e burst `14`/vida `200` confirmados no bytecode 1.0.1.1.
- ✅ `DamageTypes.ARTISAN_SMASH`, dedupe por id, `ALLOW_SELF_PROTECT_ALLIES` e `clip` de oclusão confirmados.
- ⚠️ `FLIGHT_AIR_DRAG=0.99` está declarado, mas nenhum consumidor foi identificado no corpo examinado.
- ⚠️ multiplicador instalado, mana/cooldown efetivos e comportamento real da explosão permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, PvP, bloqueio real ou teste de projection preview.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: lançador conjurado que dispara um projétil explosivo de área com raio escalado por poder. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
