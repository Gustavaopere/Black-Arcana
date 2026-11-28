# Manifestation Grimoire

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:manifestation_grimoire` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.LEGENDARY` |
| Níveis | 1 (`DefaultConfig.setMaxLevel(1)`) |
| Tipo de cast | `CastType.LONG` |
| Cooldown declarado | `60.0` s |
| Recurso | Mana do Iron's (`baseManaCost=100`, `manaCostPerLevel=0`) |
| Aquisição | `setAllowCrafting(false)`, `allowLooting()=false` |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.manifestationgrimoire.ManifestationGrimoire` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("manifestation_grimoire", ManifestationGrimoire::new)` |
| Config | `ManifestationGrimoire.config` (`LEGENDARY`, nível 1, cooldown `60.0`, `setAllowCrafting(false)`) |
| Coeficientes | `ManifestationGrimoire.<init>()`: `baseSpellPower=0`, `spellPowerPerLevel=0`, `baseManaCost=100`, `manaCostPerLevel=0`, `castTime=50` |
| Spawn | `onCast(...)`: `entity.getEyePosition(1.0F).add(RotationTools.getFlatForward(entity).scale(1.5))` |
| Item | `new ItemStack(ItemRegistry.ENDER_GRIMOIRE.get(), 1)` → `ItemEntity` |
| Estado do item | `setNoGravity(true)`, `setDeltaMovement(0,0,0)`, `setPickUpDelay(20)` |
| Partículas | `ParticleTypes.END_ROD` (4), `FIREWORK` (6), `PORTAL` (32), spreads `0.2`, speed `0.01` |
| Som/animação | `SoundRegistry.BLACK_HOLE_CAST` (start), provider `VANILLA_SUMMON_MAGICAL_ENTITY` (finish), `ANIMATION_CONTINUOUS_CAST_ONE_HANDED` / `ANIMATION_INSTANT_CAST` |

Bytecode: `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`); decompilação: `scratch/ender10_sources.txt` (SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `AbstractSpell` resolve mana/cooldown/nível; `castTime=50`, `CastType.LONG`.
2. `onCast` calcula posição na frente do casador: olhos com `getFlatForward()*1.5` — direção horizontal achatada, não o vetor de visão completo.
3. Cria `ItemEntity` com um `ENDER_GRIMOIRE`, sem gravidade, velocidade zero e `pickUpDelay=20` ticks.
4. Em `ServerLevel`, emite partículas `END_ROD`, `FIREWORK` e `PORTAL` na posição.
5. Chama `super.onCast`.

Não há parâmetro de spell power aplicável; o resultado é a criação de um item provider-owned.

## 4. Geometria e estado do item

| Propriedade | Valor e consumidor |
|---|---|
| Deslocamento | `1.5` blocos à frente, plano horizontal (`RotationTools.getFlatForward`) |
| Origem | `getEyePosition(1.0F)` |
| Gravidade | desligada (`setNoGravity(true)`) |
| Velocidade inicial | `Vec3.ZERO` |
| Pickup delay | `20` ticks |
| Item | `apprenticecodex:ender_grimoire`, quantidade 1 |
| Partículas | 4 `END_ROD`, 6 `FIREWORK`, 32 `PORTAL` |

A descrição pública fala em grimoire vinculado com spells compartilhadas entre manifestações; essa persistência/link pertence ao sistema de item do provider e **não foi estendida** além do que esta classe mostra.

## 5. Resultado

- O item criado é consequência direta do cast; não é uma entidade semântica independente para contagem de magias.
- Não há dano, alvo, AOE ou debuff nesta spell.
- Black Arcana não deve reprocessar o spawn do item nem converter o grimoire em familiar sem contrato real.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `0 + 0*(level-1)` | sem escalonamento |
| Mana | `100 + 0*(level-1)` | Iron's mana |
| Cast time | `50` ticks | fixo |
| Distância de spawn | `1.5` | blocos, plano horizontal |
| Pickup delay | `20` | ticks |
| Cooldown | `60.0` s | `DefaultConfig` |

## 7. Possibilidades de perks

- **A — atributo nativo:** mana/cooldown/cast time via `AbstractSpell`; não há spell power aplicável.
- **B — evento verificado:** `onCast` é o único ponto de criação; não há evento de spawn reutilizável como hook seguro.
- **C — adapter condicionado:** alterar distância, pickup delay ou quantidade exigiria substituir `ManifestationGrimoire.onCast` e o contrato do `ItemEntity`. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API comprovada para manifestar múltiplos grimoires ou alterar o link de spells sem risco de duplicação. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → um ItemEntity de grimoire → partículas`.

O item é o efeito terminal da raiz `manifestation_grimoire`; não é cast adicional nem fonte automática de Mastery.

## 9. Concepção de nova magia

Assinatura ocupada: "manifestação de item de grimoire persistente à frente do casador". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash, coeficientes, posição de spawn, estado do item e partículas confirmados no bytecode 1.0.1.1.
- ⚠️ Sistema de link/persistência do `ENDER_GRIMOIRE` e aquisição efetiva não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, multiplayer, pickup ou reload de item.
- ⚠️ Universo integral do provider não encerrado.

## Localizadores para Codex — resumo operacional

- O deslocamento é horizontal (`getFlatForward`), não o `lookAngle` 3D.
- `pickUpDelay=20` é do item entity; não confundir com cooldown da spell.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
