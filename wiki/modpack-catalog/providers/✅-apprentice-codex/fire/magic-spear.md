# Magic Spear

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:magic_spear` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | `GeoEntity`, `AntiMagicSusceptible`; `SummonedFirearmTools` e `DamageTypes.MAGIC_SPEAR` pertencem à raiz |
| Escola | `SchoolRegistry.FIRE_RESOURCE` (Fire) |
| Raridade mínima declarada | `EPIC` |
| Níveis declarados | 1–5 (`setMaxLevel(5)`) |
| Tipo de cast | `INSTANT` |
| Cooldown declarado | `0.5 s` |
| Recurso | Mana do Iron's (`baseManaCost=30`, `manaCostPerLevel=30`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.magicspear.MagicSpear` |
| Auxiliares da mesma raiz | `MagicSpearMissileEntity`, `SummonedFirearmTools`, `DamageTypes.MAGIC_SPEAR` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("magic_spear", MagicSpear::new)` |
| Config | `EPIC`, nível 5, cooldown `0.5`, `FIRE_RESOURCE`, `CastType.INSTANT` |
| Coeficientes | <init>: `baseSpellPower=600`, `spellPowerPerLevel=300`, `baseManaCost=30`, `manaCostPerLevel=30`, `castTime=0` |
| Dano | `getDamage` → `power/100 * damageMultiplier(MAGIC_SPEAR)` |
| Mira | `LOCK_ON_RANGE=64.0`, via `SummonedFirearmTools.resolveAssistedAim` e filtro `isValidCombatTarget` |
| Alternância | tag persistente `apprenticecodex.magic_spear.next_left` em `caster.getPersistentData()` |
| Spawn | `eye + forward*0.4 + side*0.75 + (0,-0.25,0)`; lados alternados `-1`/`1` |
| Fases | `RELEASE_TICKS=5`, `BOOST_SPEED=2.2`, `HOMING_TURN_DEGREES=5.0`, `MAX_LIFE_TICKS=120`, `BURST_TICKS=14` |
| velocidades de release | `RELEASE_SIDE_SPEED=0.045`, `RELEASE_FORWARD_SPEED=0.02` |
| Impacto | `BLAST_RADIUS=1.5`, `ENTITY_IMPACT_INFLATE=0.35`, burst visual `3.0` |

Bytecode: scratch/fire5_evidence/javap1011_fire6.txt (`javap -classpath <JAR> -p -s -c`, 28 classes, 1.095.867 bytes, EXIT=0, SHA-256 `F5491A50DCF3A8F7EBF1E9C035EFE0723490C97475DE501FC3AF6C1580E17EDB`, SHA-1 `53C2C327705603172618C84CFFEFC41412683190`); decompilação de apoio: scratch/fire5_sources.txt (fontes Vineflower 1.12.0 das cinco raízes legadas e auxiliares, 188.994 bytes, SHA-256 `F8BE6DF48A22522FC1B23FBA362D8FD0F2637A2759D65739F25A723A2903A448`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `onCast` chama `spawnMissile` somente em `ServerLevel` e então `super.onCast`.
2. `resolveLaunchForward` usa a visão inclinada quando o caster está voando/nadando; caso contrário usa `RotationTools.getFlatForward`.
3. `resolveLaunchRight` calcula a lateral com `worldUp.cross(forward)` e tem fallback para pose horizontal.
4. `nextSide` lê e inverte a tag persistente do caster, produzindo spawn alternado à esquerda/direita.
5. `setup` grava dano, direção, lateral e alvo opcional, e define movimento inicial `side*0.045 + forward*0.02`.
6. `tickRelease` mantém esse movimento por `5` ticks; `startBoost` troca para `movementDirection*2.2`.
7. `tickBoost` redireciona no máximo `5.0` graus por tick para o alvo válido e usa `moveWithImpactCheck`.
8. Colisão com entidade ou bloco chama `explode`, que aplica dano em AABB inflada `1.5` com dedupe por id; anti-magia chama `burstWithoutDamage`.
9. A fase de burst dura `14` ticks e o míssil é descartado se `tickCount > 120` antes do impacto.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Colisão direta do míssil ou entidades em AABB de raio `1.5` no centro da explosão |
| Filtro | `canHitEntity` exclui owner, exige `isValidCombatTarget` e bloqueia nova colisão na fase de burst |
| Mira assistida | `64.0` blocos, com `resolutePartEntity` e revalidação de alvo |
| Hitbox de busca | `getBoundingBox().expandTowards(movement).inflate(0.35)` |
| Knockback | `KnockbackTypes.DEFAULT` no dano de área |
| Tempo | release `5`, boost até `120`, burst `14` ticks |
| Persistência | NBT com dano, fase, contadores, direções e `Target` UUID; geometria de colisão não é persistida separadamente |

## 5. Resultado

- Dano de impacto explosionário em AABB, tipo `DamageTypes.MAGIC_SPEAR`.
- O homing é limitado a `5` graus/tick e exige alvo vivo, mesmo nível e válido contra o owner.
- A explosão não verifica oclusão de bloco no método `applyBlastDamage` examinado; isso não prova comportamento em runtime modificado.
- Sem queima, cura ou invocação persistente (`N/A` com justificativa: o míssil é descartado após o burst).

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `600 + 300*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Dano | `power/100 * damageMultiplier(MAGIC_SPEAR)` — config **NÃO VERIFICADA** |
| Mana | `30 + 30*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `0.5` s declarado; efetivo **NÃO VERIFICADO** |
| Cast time | `0` ticks, coerente com `CastType.INSTANT` |
| Lock-on | `64.0` blocos; não é o alcance de voo do míssil |
| Velocidade | release `0.045` lateral + `0.02` avante; boost `2.2` blocos/tick |
| Explosão | raio `1.5`, burst `14` ticks, vida máxima `120` ticks |

## 7. Possibilidades de perks

- **A — atributo nativo:** dano responde a `getSpellPower`; mira/help de mira depende de utilitário do provider.
- **B — evento verificado:** `EventHooks.onProjectileImpact` pode cancelar um impacto, mas não há hook para alterar parâmetros em voo.
- **C — adapter condicionado:** mudar homing, raio de explosão ou alternância de lado exigiria substituir `MagicSpear` e a entidade com risco de duplicar míssil. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para converter o míssil em área persistente ou alterar o lock-on sem duplicar dano. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`cast instantâneo → míssil alternado em release 5 ticks → boost 2.2 com homing 5 graus/tick → impacto → explosão AABB 1.5 com dedupe → burst 14 ticks e descarte`.

## 9. Concepção de nova magia

Assinatura ocupada: míssil de mira assistida, disparo alternado e explosão em área. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `600/300/30/30/0`, `EPIC/5/0.5`, dano `power/100*multiplier`, `LOCK_ON_RANGE=64`, tag alternada, constantes de release/boost/homing/burst e NBT confirmados no bytecode 1.0.1.1.
- ✅ `applyBlastDamage` com AABB `1.5`, dedupe por id e `KnockbackTypes.DEFAULT` confirmado.
- ⚠️ multiplicador instalado, mana/cooldown efetivos e lock-on real em cliente permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, PvP, mira real, colisão ou anti-magia.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: míssil de mira assistida, disparo alternado e explosão em área. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
