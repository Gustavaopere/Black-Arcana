# Silent Assassin

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:silent_assassin` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<SilentAssassinRifleEntity>`) |
| Interfaces | `IMagiAgentSuitAffectedSpell` (interrompibilidade); `DamageTypes.SILENT_ASSASSIN` e `GunSpellTracerPacket` pertencem à raiz |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `EPIC` |
| Níveis declarados | 1–3 (`setMaxLevel(3)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `16.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=100`, `manaCostPerLevel=40`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.silentassassin.SilentAssassin` |
| Auxiliares da mesma raiz | `SilentAssassinRifleEntity`, `SummonedFirearmTools`, `DamageTypes.SILENT_ASSASSIN`, `SoundRegistry.SUPPRESS_RIFLE` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("silent_assassin", SilentAssassin::new)` |
| Config | `EPIC`, nível 3, cooldown `16.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=40`, `spellPowerPerLevel=60`, `baseManaCost=100`, `manaCostPerLevel=40`, `castTime=50` |
| Dano base | `getDamage()` → `15 * ApprenticeCodexServerConfig.damageMultiplier(DamageMultiplierKey.SILENT_ASSASSIN)` |
| Headshot | `getHeadshotPercent(power)` → `min(1000, 100 + round(power))` |
| Vida quase cheia | `ALMOST_FULL_HEALTH_RATIO=0.995F`; `getFullHealthDamageBonusPercent()=200` |
| Alcance | `getRange()=128`; `resolveAssistedAim(entity,128,isValidCombatTarget)` |
| Supressão | `AWARENESS_SUPPRESSION_RADIUS=16.0`; `suppressNearbyAwareness` somente em headshot que matou com bônus |
| Rifle | `MAX_RECOIL_TICK=10`, tracer `32.0` blocos/tick e comprimento `16.0`; NBT `RecoilTick` |
| Dano aplicado | `createCombatDamageSource(DamageTypes.SILENT_ASSASSIN)` + `CombatTools.applySpellDamage(...,DEFAULT)` |

Bytecode: scratch/javap1011_evocation7.txt (`javap -classpath <JAR> -p -s -c`, 94 classes, EXIT=0, SHA-256 `AF225F42FA1A0295D7339542D49620FBA0D0BE6599147EEDF69B75744730DB41`); decompilação de apoio: scratch/evocation7_sources.txt (46 fontes Vineflower 1.12.0, SHA-256 `05090319D9206171C8C4C38ED1A33479F0F1313F9135B5D70146F5559EB80DB1`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCastNoWeapon` cria a `SilentAssassinRifleEntity` e a adiciona ao mundo.
2. `onCastTickWithWeapon` usa `resolveAssistedAim` em `128` blocos para atualizar o retículo (`setCastingReticleEffect`).
3. `onCastCompleteWithWeapon`: cancelamento devolve `RELEASE_WEAPON`; sem cancelamento, refaz `resolveAssistedAim` e calcula `isHeadShot`.
4. Com `hitEntity`, resolve parte via `CombatTools.resolutePartEntity`, aplica `getDamage()`, multiplica por `headshot%/100` se headshot e por `200/100` se headshot com vida ≥ `maxHealth*0.995`.
5. `weapon.damageTarget` aplica `DamageTypes.SILENT_ASSASSIN` com knockback padrão; se o alvo morre com o bônus, `suppressNearbyAwareness` atinge `16.0` blocos.
6. `weapon.fire` envia tracer `32.0/16.0`, partículas de muzzle/smoke/hit/crit e som `VANILLA_CRITICAL_SHOT` em headshot; o resultado é `KEEP_WEAPON`.
7. O rifle segue `getStandbyPosition` (`calculateBehindPosition(owner,-0.8,1.1,0.1)`) e mantém estado sincronizado por `EntityDataAccessor`.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Entidade resolvida por `SummonedFirearmTools.resolveAssistedAim`, filtrada por `isValidCombatTarget` |
| Alcance | `128` blocos para mira assistida |
| Headshot | `min(1000, 100 + round(spellPower))`% de multiplicador; `getSpellPower` efetivo **NÃO VERIFICADO** |
| Bônus | `×2.0` somente se headshot e alvo vivo com saúde ≥ `99.5%` do máximo |
| Supressão | Raio `16.0` blocos, somente após morte com o bônus ativo |
| Projétil | Nenhum; `GunSpellTracerPacket` é feedback visual com `32.0` blocos/tick e comprimento `16.0` |
| Persistência | Rifle com NBT `RecoilTick` e data accessors de mira/casting; sem dano persistente |

## 5. Resultado

- Dano direto no alvo com `DamageTypes.SILENT_ASSASSIN`; headshot e vida cheia são multiplicadores em cascata, não fontes de dano separadas.
- `suppressNearbyAwareness` é efeito secundário condicionado a headshot letal com bônus; não altera dano.
- `HitTypes` (`MISS`/`BLOCK`/`ENTITY`) controla apenas partículas; `canBeInterruptedWithMagiAgentSuit` altera interrompibilidade, não dano.
- Sem AOE de dano, cura, invocação múltipla ou status (`N/A` com justificativa).

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `40 + 60*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Dano base | `15 * damageMultiplier(SILENT_ASSASSIN)` — config **NÃO VERIFICADA** |
| Headshot | `min(1000, 100 + round(power))`% |
| Vida quase cheia | `200/100 = ×2.0` quando `health >= maxHealth*0.995` |
| Mana | `100 + 40*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `16.0` s declarado |
| Cast time | `50` ticks (`CastType.LONG`) |

## 7. Possibilidades de perks

- **A — atributo nativo:** poder altera headshot; dano base depende só da config de multiplicador.
- **B — evento verificado:** `IMagiAgentSuitAffectedSpell` apenas modifica interrompibilidade; não é hook de dano.
- **C — adapter condicionado:** alterar multiplicadores, raio de supressão ou mira exigiria substituir `SilentAssassin` e `SilentAssassinRifleEntity` com risco de duplicar dano. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para transformar tiro único em AOE ou editar headshot sem duplicar casting. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast long → rifle segue o dono → mira assistida em 128 → headshot ×multiplicador → bônus ×2 se vida ≥99.5% → dano SILENT_ASSASSIN → supressão em 16 blocos se letal`.


## 9. Concepção de nova magia

Assinatura ocupada: rifle de tiro único com headshot escalado e bônus contra alvo saudável. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `40/60/100/40/50`, dano `15*multiplier`, headshot `min(1000,100+round(power))`, bônus `200%`, limiar `0.995`, alcance `128`, supressão `16.0`, tracer `32/16` e `KEEP_WEAPON` confirmados no bytecode 1.0.1.1.
- ❌ correção crítica: a ficha legada 0.9.7.1 afirmava incremento `100`, teto `500` e `50*power/100`; o JAR 1.0.1.1 usa incremento `60`, teto `1000` e `100+round(power)`.
- ⚠️ multiplicador instalado, mana/cooldown efetivos e comportamento de supressão em combate real permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, PvP, headshot real ou supressão observada.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: rifle de tiro único com headshot escalado e bônus contra alvo saudável. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
