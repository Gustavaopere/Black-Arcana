# Auto Magnet

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:auto_magnet`
- **Iron's school:** Ender
- **Levels:** 1–5
- **Minimum rarity:** Common
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 25`
- `baseManaCost = 40`
- `manaCostPerLevel = 10`
- `castTime = 0`
- collection range: `8 + 4 * (spellLevel - 1)` = **8 / 12 / 16 / 20 / 24 blocks**
- collection mana charge: `10` by default, or `0` when the provider server config disables collection mana cost

## Provider behavior

The cast toggles `AutoMagnetFamiliarManager` on the server. Crouching selects **REVERSE** collection mode; normal casting selects **NORMAL** mode. The provider sends the resolved mode back as action-bar presentation.

The public guide describes an owner-following magnet that gathers dropped items/XP while respecting inventory behavior. Exact per-entity collection cadence and inventory insertion rules remain provider-manager authority.

## Resource authority

The ongoing collection mana cost is provider-owned. Black Arcana must not impose an additional mana/strain payment merely because Auto Magnet collected an item, nor infer a cast/progression event from each collected stack or XP orb.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **toggleable owner-following item/XP magnet with normal/reverse modes** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CAST+RANGE+COLLECTION-MANA CONFIG / INVENTORY INSERTION+ENTITY CADENCE+RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:auto_magnet` → `SpellRegistry.reg("auto_magnet", AutoMagnet::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.automagnet.AutoMagnet`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/automagnet/AutoMagnet.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — 0.9.7.1 (audit de source, 2026-10-13)

**Prova rastreável:** [`automagnet/AutoMagnet.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/automagnet/AutoMagnet.java) · [`automagnet/AutoMagnetFamiliarManager.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/automagnet/AutoMagnetFamiliarManager.java) · [`automagnet/AutoMagnetFamiliarEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/automagnet/AutoMagnetFamiliarEntity.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, mod ID `apprenticecodex`. Identidade e versão do JAR são da modlist física; **não há prova de equivalência de cada corpo de método com o JAR compilado**.

### Automação do familiar e liquidação de mana

- **Toggle com dono:** `AutoMagnetFamiliarManager.toggle(ServerPlayer,range,collectMana,mode)` mantém `AutoMagnetState` e UUID da entidade gerenciada. Recaste no mesmo modo pode desativar; mudança de modo provoca ativação/normalização. `maintainActive` e `normalizeOwnedFamiliars` revalidam owner e descartam cópias duplicadas do mesmo familiar.
- **Cadência:** `AutoMagnetFamiliarEntity.tickOnServer` consulta `getCollectionMode().canCollect(owner.isCrouching())`; quando habilitado e `tickCount % COLLECT_INTERVAL_TICK == 0`, com `COLLECT_INTERVAL_TICK=2`, chama `collectNearbyDrops`.
- **Itens:** o scanner usa AABB do owner, distância ao quadrado e filtros de `MagneticStabilityAnchorProtection`, `BotaniaSolegnoliaCompatBridge` e itens recentemente largados pelo próprio dono. Também exige possibilidade de encaixe no inventário **normal** do player, sem promessa de inventários extensíveis. Para o primeiro item ainda não marcado numa rodada, `tryConsumeCollectMana` consulta o mana de `MagicData`; só prossegue se houver saldo, cobrando **uma vez para o lote de itens daquela rodada**, não por cada stack transferido.
- **XP:** a busca de `ExperienceOrb` ocorre em uma passagem separada e movimenta os orbes para os pés do owner; **não há chamada de `tryConsumeCollectMana` dentro desse loop de XP**. Isso não prova aquisição final do XP ou bypass de quaisquer eventos de pickup.
- **Recepção:** a entidade usa `setPos(ownerFeet)`, `setDeltaMovement(Vec3.ZERO)` e `setNoPickUpDelay()` para os itens; não faz `Inventory.add` no caminho examinado. A inserção/pickup posterior é responsabilidade do Minecraft/host.
- **Boundary:** cast-toggle, duas passagens de coleta e eventual pickup não são magias distintas. Não cobrar mana, Strain ou Mastery por item/XP; testar full inventory, múltiplos familiares, chunk unload, player logout, compat Botania e retorno de mana após stop.

### Perfil para integração de perks e QA

- **A / stats e rank:** ler apenas os atributos declarados no host Iron's e os state objects que o addon expõe; stat dinâmica e duração efetiva exigem ambiente, item e configuração. Nenhuma alteração de mana/cooldown do Iron's por Black Arcana.
- **B / causalidade:** uma ação primária `apprenticecodex:auto_magnet`; filhos, efeitos retardados, limpeza ou automação pertencem à raiz do provider. Sem `cast UUID`/contrato de retorno validado, o BA e RPG não devem inferir reward do resultado observado.
- **C/D / segurança:** ⛔ adapter de Mastery/perks enquanto inexistir contrato seguro. ⚠️ QA: servidor real, replay, NBT/relog, cross-dimension, compat opcional, ordenação e anti-double-processing. Não houve GameTest do provider nesta auditoria.
- **Clean-room:** análise factual e documentação próprias; código upstream não foi incorporado.

[Matriz causal desta etapa](../PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md).
