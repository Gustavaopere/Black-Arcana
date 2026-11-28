# Precision Jack

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:precision_jack` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSummonWeaponSpell<PrecisionJackKnifeEntity>`) |
| Interfaces | `GeoEntity`, `ISwordTrailEntity` na faca; `PrecisionJackLootingEvent` é callback da mesma raiz |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `UNCOMMON` |
| Níveis declarados | 1–4 (`setMaxLevel(4)`) |
| Tipo de cast | `configurado pelo host (`castTime=40`)` |
| Cooldown declarado | `1.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=60`, `manaCostPerLevel=30`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.precisionjack.PrecisionJack` |
| Auxiliares da mesma raiz | `PrecisionJackKnifeEntity`, `PrecisionJackLootingEvent`, `DamageTypes.PRECISION_JACK` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("precision_jack", PrecisionJack::new)` |
| Config | `UNCOMMON`, nível 4, cooldown `1.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=100`, `spellPowerPerLevel=50`, `baseManaCost=60`, `manaCostPerLevel=30`, `castTime=40` |
| Dano | `getDamage()` → `6.0F * ApprenticeCodexServerConfig.damageMultiplier(DamageMultiplierKey.PRECISION_JACK)` |
| Looting | `getLootingBonus` → `min(5, max(1, round(power/100)))`; `getDuplicateDropChancePercent` → `min(30, max(0, round(power/10)))` |
| Faca | `STAY_SLASHED_TICK=10`, `UNPREPARED_TIMEOUT_TICKS=5`, `PREPARED_TIMEOUT_TICKS=80`, `SLICE_RANGE=1.25` |
| Ataque | `slice`: `hitsAabb(position + look*0.75, 1.25, e != owner && isValidCombatTarget)` |
| Dano aplicado | `createCombatDamageSource(DamageTypes.PRECISION_JACK)` + `CombatTools.applySpellDamage(...,DEFAULT)` |
| Loot | `PrecisionJackLootingEvent.onLivingDrops`: `LivingDropsEvent`, `source.is(PRECISION_JACK)`, vítima não `Player`, `directEntity` faca, rolagem extra e `PLAYER_LEVELUP` |
| NBT | `Damage`, `LootingBonus`, `DuplicateDropChancePercent`, `LifeTick`, `UnresolvedCastTick`, `IsPrepared` |

Bytecode: scratch/javap1011_evocation7.txt (`javap -classpath <JAR> -p -s -c`, 94 classes, EXIT=0, SHA-256 `AF225F42FA1A0295D7339542D49620FBA0D0BE6599147EEDF69B75744730DB41`); decompilação de apoio: scratch/evocation7_sources.txt (46 fontes Vineflower 1.12.0, SHA-256 `05090319D9206171C8C4C38ED1A33479F0F1313F9135B5D70146F5559EB80DB1`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCast` cria uma `PrecisionJackKnifeEntity` e entrega os parâmetros calculados; a faca segue o dono em `getStandbyPosition` (`calculateBehindPosition(owner,0,0,-0.75)`).
2. `prepare()` ativa trail, dispara animação `prepare`, marca `isPrepared` e zera `unresolvedCastTick`.
3. `slice()` exige `isPrepared`: dispara `slice`, define `lifeTick=10`, desmarca preparo e usa `RaycastTools.hitsAabb` com raio `1.25` a partir de `position + look*0.75`.
4. Cada alvo válido recebe `this.damage` via `DamageTypes.PRECISION_JACK` e `KnockbackTypes.DEFAULT`.
5. `tickUnresolvedCast` descarta a faca ao atingir `80` ticks preparada ou `5` ticks sem preparo; `lifeTick` expira após o corte.
6. `onLivingDrops` exige fonte `PRECISION_JACK`, vítima não jogador e faca como entidade direta; rola `nextInt(100) < chance` para drop extra e soma `nextInt(lootingBonus+1)` por item.
7. A notificação `PLAYER_LEVELUP` só ocorre se a rolagem extra produzir item e o dono for `ServerPlayer`.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Entidades em AABB de raio `1.25`, centrada em `position + look*0.75`, exceto o dono |
| Filtro | `CombatTools.isValidCombatTarget(e, owner)` |
| Geometria | AABB isotrópica; `SLICE_RANGE=1.25` é raio, não diâmetro |
| Tempo | `10` ticks de `lifeTick` após o corte; `80`/`5` ticks de timeout de cast não resolvido |
| Projétil | Nenhum; dano aplicado diretamente no `slice` |
| Persistência | NBT com dano/looting/chance/contadores; faca é entidade supervisionada pelo dono |

## 5. Resultado

- Dano direto por corte em AABB; tipo de dano `DamageTypes.PRECISION_JACK`, knockback padrão.
- `LootingBonus` e `DuplicateDropChancePercent` são parâmetros da raiz, transportados na faca e consumidos somente no evento de drops.
- O drop extra é uma rolagem adicional da loot table com contexto de jogador e dano; a notificação sonora é feedback, não efeito de dano.
- Nenhum status, cura, teleporte, AOE persistente ou projétil independente (`N/A` com justificativa).

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 50*(level-1)` (declarado); efetivo **NÃO VERIFICADO** |
| Dano | `6.0F * damageMultiplier(PRECISION_JACK)` — config **NÃO VERIFICADA** |
| Looting | `min(5, max(1, round(power/100)))`; setter da faca aplica `max(0, ...)`, evento reaplica `min(5, ...)` |
| Chance de drop extra | `min(30, max(0, round(power/10)))`%; setter clamp `0..100`, evento reaplica `min(30, ...)` |
| Mana | `60 + 30*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `1.0` s declarado |
| Cast time | `40` ticks no construtor |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano e mana respondem ao poder via `AbstractSpell`; looting e chance já derivam de `getSpellPower`.
- **B — evento verificado:** `PrecisionJackLootingEvent` é callback de drops, mas não expõe mutador de parâmetros.
- **C — adapter condicionado:** mudar AABB, timeout ou número de rolagens exigiria substituir `PrecisionJackKnifeEntity`/evento com risco de duplicar drops e XP. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para transformar o corte em AOE persistente ou alterar a chance sem duplicar loot. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast → faca preparada → slice em AABB 1.25 → dano PRECISION_JACK → evento de drops com looting/chance → limpeza por timeout`.


## 9. Concepção de nova magia

Assinatura ocupada: faca conjurada com corte#AABB e loot aprimorado. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `100/50/60/30/40`, dano `6.0*multiplier`, looting `min(5,max(1,round(power/100)))`, chance `min(30,max(0,round(power/10)))`, AABB `1.25`, timeouts `80`/`5` e NBT confirmados.
- ✅ eventos `LivingDropsEvent`, rolagem extra e `PLAYER_LEVELUP` confirmados no bytecode/decompilação 1.0.1.1.
- ⚠️ multiplicador instalado, mana/cooldown efetivos e drops reais em servidor permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, PvP, loot tables personalizadas ou duplicação observada.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: faca conjurada com corte#AABB e loot aprimorado. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
