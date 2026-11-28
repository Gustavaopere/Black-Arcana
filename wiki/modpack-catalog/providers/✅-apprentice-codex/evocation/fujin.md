# Fujin

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:fujin` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<FujinKatanaEntity>`) |
| Interfaces | sem interface adicional declarada |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `UNCOMMON` |
| Níveis declarados | 1–10 (`setMaxLevel(10)`) |
| Tipo de cast | `CONTINUOUS` |
| Cooldown declarado | `12.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=5`, `manaCostPerLevel=1`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.fujin.Fujin` |
| Auxiliares da mesma raiz | `FujinKatanaEntity`, `FujinSlashProjectileEntity`, `FujinKatanaRenderer` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("fujin", Fujin::new)` |
| Config | `UNCOMMON`, nível 10, cooldown `12.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=100`, `spellPowerPerLevel=75`, `baseManaCost=5`, `manaCostPerLevel=1`, `castTime=100` |
| Dano | `getDamage` → `(1 + power/200) * damageMultiplier(FUJIN)` |
| Alcance | `Fujin.getRange()=10.0` blocos |
| Katana | `FIRST_SLASH_TICK=10`, `SLASH_INTERVAL_TICKS=5`, `SLASH_ANIMATION_SPEED=3.0F` |
| Projétil | `SPEED=3.0`, `SLASH_WIDTH=5.0`, `HITBOX_HEIGHT=1.5`, sweep com `victimUuids`, descarte em `1.25*range`, `AntiMagicSusceptible` |
| Dano do projétil | `CombatOwnerResolver.createDamageSourcePreservingCurrentOwner(...,DamageTypes.FUJIN)` + `applySpellDamage(...,NO_KNOCKBACK)` |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCastNoWeapon` cria `FujinKatanaEntity`, aplica `setDamage(getDamage(...))` e `setProjectileRange(getRange())`, e a adiciona ao nível.
2. A katana agenda o primeiro slash no tick `10` e os seguintes a cada `5` ticks, alternando animações `slash0to1`/`slash1to2`/`slash2to1`.
3. Cada slash cria `FujinSlashProjectileEntity`, copia dano, alcance máximo e `combatOwnerUuid`, e dispara com velocidade `3.0`.
4. O projétil varre `AABB` de largura `5.0` e altura `1.5` expandida pelo movimento; usa `victimUuids` para não acertar o mesmo alvo duas vezes e exige `hasClearPathToTarget` (clip de bloco).
5. `damageEntities` aplica `DamageTypes.FUJIN` com `KnockbackTypes.NO_KNOCKBACK`; `AntiMagicSusceptible` descarta o projétil sob anti-magia.
6. `getDamageMovement` limita o dano ao alcance restante; o descarte ocorre em `1.25 * maxTravelDistance` e o achatamento visual começa em `0.75`.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alcance | `10.0` blocos (dano até `10`, descarte em `12.5`) |
| Hitbox do corte | `5.0` de largura × `1.5` de altura, varrida por passos de `0.125` |
| Velocidade | `3.0` blocos/tick |
| Dedup | `Set<UUID> victimUuids` por projétil |
| Oclusão | `ClipContext` de bloco entre origem e alvo |
| Cadência | Primeiro slash no tick `10`, intervalo `5` ticks |

## 5. Resultado

- Cada corte é um projétil de varredura, não um ataque automático da katana.
- `victimUuids` impede dano duplo por projétil; novos slashes criam novos conjuntos.
- A katana e o corte pertencem à mesma raiz semântica.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 75*(level-1)` | float declarado |
| Dano | `(1 + power/200) * damageMultiplier(FUJIN)` | config **NÃO VERIFICADA** |
| Alcance | `10.0` fixo | blocos |
| Mana/cooldown/cast | `5+1*(level-1)` / `12.0` s / `100` ticks | host + config **NÃO VERIFICADA** |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano responde ao poder; mana/cooldown ao `AbstractSpell`.
- **B — evento verificado:** anti-magia descarta o corte; não é ponto de alteração de parâmetros.
- **C — adapter condicionado:** mudar largura/altura, cadência ou alcance exigiria substituir katana e projétil. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há hook seguro para transformar o corte em AOE radial persistente ou remover a oclusão de bloco. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast contínuo → katana → slashes periódicos → projéteis de varredura com dedup → dano `FUJIN` sem knockback`.


## 9. Concepção de nova magia

Assinatura ocupada: "lâmina conjurada com cortes varridos". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, coeficientes 100/75/5/1/100, dano `(1+power/200)`, alcance 10, constantes 10/5/3.0 e geometria 5.0/1.5/1.25 confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador instalado, DPS real e comportamento com partes de entidade não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- `10` é o alcance de dano; `12.5` é o descarte do projétil.
- `victimUuids` é por projétil, não global.
- A katana e o corte são uma única raiz.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
