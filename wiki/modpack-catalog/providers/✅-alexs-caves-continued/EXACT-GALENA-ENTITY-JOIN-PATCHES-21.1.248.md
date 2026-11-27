# Galena Gauntlet — patches de entrada de entidades (NeoForge 21.1.248)

**Estado:** ⚠️ **subcontrato estático read-only restrito aos patches `userdev` oficiais**. Este dossiê identifica superfícies de instrumentação e tokens de chamadas, mas **não certifica o comportamento transformado** de `Level.addFreshEntity`, rollback do item, ausência de conflitos ou hooks. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · `provider_universe_closed=false`.

## 1. Motivação, autoridade e proveniência

A [ficha individual da Galena](equipment/galena-gauntlet.md), o [dossiê de retorno/drop 1.0.10](EXACT-GALENA-GAUNTLET-RETURN-DROP-1.0.10.md) e a [auditoria ACCompat 1.0.10](EXACT-GALENA-ACCOMPAT-COMBAT-BRIDGES-1.0.10.md) já registram que o provider solicita `ItemStack.setCount(0)` **antes** da criação da entidade e de `Level.addFreshEntity`, cujo retorno booleano é descartado. Isso é uma **sequência de chamadas**, não evidência de perda efetiva da arma, fraude, duplicação ou mutação admissível.

A [auditoria ABI da versão-alvo 21.1.248](EXACT-GALENA-ENTITY-JOIN-ABI-21.1.248.md) demonstrou que `EntityJoinLevelEvent` declara `ICancellableEvent`; sua existência, por si só, não prova disparo na rota Galena. Este recorte avança ao inspecionar **os patches upstream exatos** do engine:

- Minecraft **1.21.1**; NeoForge **21.1.248** (versão `neo_version` pinada nos `gradle.properties` de Black Arcana/RPG Skill Tree; instalação transformada não verificada).
- Provider Alex's Caves Continued **1.0.10**; JAR publisher SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Modlist sibling: `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; novo dump físico continua **NÃO VERIFICADO**.
- [Maven oficial NeoForge 21.1.248 — `userdev`](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.248/neoforge-21.1.248-userdev.jar): **3.983.248 bytes**, SHA-256 **`9278d08154a82927391ed5257481f56d6d0fcb147822c6a79ec9b5129799e79a`**, verificado contra o arquivo `.sha256` oficial e pinado na sonda.
- ZIP `userdev`: **963 entradas**, das quais **753** patches `patches/net/minecraft/**/*.java.patch`; SHA-256 do roster de paths lexicograficamente ordenados com newline final: `22046c708c5774e479f335fcef95a0c526670fbc9dde01fc29281c94102a640f`.
- [Execução inicial de descoberta #45186275044](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45186275044), job `137732591187`, concluída com sucesso, HEAD observacional `01bfa33698acbb1918f357a3f19ebb1661a51367`.
- Relatório JSON de descoberta: **7.298 bytes**, SHA-256 **`a1a2df01b3537a534d26d9121fbd0103368f82135c1b291c3843a89aaad12114`**. A [sonda](../../../../docs/qa/alexscaves_1010_galena_neoforge_211248_entity_join_patches_probe.py), o [manifesto de selagem](EXACT-GALENA-ENTITY-JOIN-PATCHES-21.1.248.json), o [checker adversarial](../../../../docs/qa/alexscaves_1010_galena_neoforge_211248_entity_join_patches_checks.py) e a [CI específica](../../../../.github/workflows/alexscaves-1010-galena-neoforge-211248-entity-join-patches.yml) permitem reexecutar. **A execução do checker na HEAD final precisa ser consultada separadamente**: o resultado de descoberta inicial não substitui o gate SHA-exato posterior.

A inspeção **não copia o texto nem a implementação dos patches**: os registros contêm somente classificação ADD/DELETE/CONTEXT, índice de linha, índice de hunk, tokens relevantes, tamanho e SHA-256 de cada linha selecionada.

## 2. Censo de quatro candidatos upstream

| Patch no `userdev` exato | Disposição e SHA-256 do patch | Hunks | Linhas com símbolos (ADD/DELETE/CONTEXT) |
|---|---|---:|---|
| `server/level/ServerLevel.java.patch` | presente · `d9dc7428b5467f35b42e9f972b3eb9079312e660755b77b6be1f880ed88e6249` | 21 | **11** (9/2/0) |
| `world/level/entity/PersistentEntitySectionManager.java.patch` | presente · `a2a5ef2bdbf3fec5b7db2f7cc4674338358011b3b738622a7f180faeeb2a56a0` | 5 | **4** (1/0/3) |
| `world/level/Level.java.patch` | presente · `a98a50aae07408798c12cdacf25489a86acd3d910943f03e88d7a042781200e6` | 17 | **1** (1/0/0) |
| `world/level/LevelWriter.java.patch` | **ausente no roster de patches** | N/A | 0 |

Prefixo comum: `patches/net/minecraft/`. A ausência de um arquivo `.patch` **não comprova** ausência da interface, métodos, corpo vanilla, outros transformers ou alterações indiretas.

### 2.1. Linhas de evento com cancelamento — duas fontes concretas

| Patch | Linha da patch | Hunk | Tipo | Tokens observados na mesma linha | SHA-256 da linha |
|---|---:|---:|---|---|---|
| `ServerLevel` | **139** | **13** | **ADD** | `EVENT_BUS`, `EntityJoinLevelEvent`, `isCanceled` | `eeab97afd0dff7a75cc14b2593061a29135e63a5bae9f472846fc11b860d5d51` |
| `PersistentEntitySectionManager` | **12** | **1** | **ADD** | `EVENT_BUS`, `EntityJoinLevelEvent`, `isCanceled` | `431d5741436fdce83409d407893a129638695ca0bc04cc27cdb630caf7ebd91e` |

**Fato comprovado:** em cada um desses dois arquivos de patch upstream, há uma **linha adicionada** que contém, conjuntamente, os símbolos de publicação no event bus, o nome do evento e uma consulta de cancelamento. Isso é mais específico que a identificação de uma interface `ICancellableEvent`.

**Fatos ainda não comprovados:** a posição exata dessa condição em relação aos efeitos do `ServerLevel.addFreshEntity` e ao retorno da chamada; o significado de cada ramo de retorno; as condições de bypass; a cobertura completa de todos os callsites; se a rota `GalenaGauntletItem.onUseTick` efetivamente atinge o mesmo caminho; e se a arma já consumida seria restituída após um cancelamento. Sem observar o corpo final transformado e testar o lifecycle, não declarar hook seguro, garantias de claims ou bug reproduzido.

### 2.2. Outras linhas e limites

- `ServerLevel` linhas **147** e **157** (`DELETE`) e **158** (`ADD`) mencionam `addNewEntity`: mostram substituição de chamadas em janelas adjacentes, **sem comprovação do efeito semântico da substituição**.
- `ServerLevel` linhas **117, 172, 185, 205, 213** (`ADD`) contêm `isCanceled`, mas **não** o identificador `EntityJoinLevelEvent` na mesma linha. Não atribuir essas condições ao evento da Galena sem seguir o contexto da função/hunk.
- `ServerLevel` linhas **128** e **252** (`ADD`) contêm `EVENT_BUS`, mas não `EntityJoinLevelEvent` na mesma linha; nenhum comportamento específico foi extrapolado.
- `PersistentEntitySectionManager` linhas **49, 67 e 68** são `CONTEXT` com o nome do manager, não alterações introduzidas pelo patch.
- `Level` linha **80** (`ADD`) contém `isCanceled`, mas sem identificação do evento e do consumer no mesmo registro. Não confundir cancelamentos de outros eventos.

**16 registros selecionados** no total, todos com hash da linha e tipo de diff selados no manifesto. O relatório não pretende ser um índice integral dos 753 patches nem da engine vanilla. O conjunto foi selecionado por pertinência à fronteira Galena.

## 3. Estado técnico e fronteiras de autoridade

| Eixo | Estado |
|---|---|
| Presença de linhas de patch `EntityJoinLevelEvent` + `isCanceled` | ✅ **demonstrada** em dois patches exatos |
| Correspondência de versão/JAR `userdev` publisher | ✅ **demonstrada**, SHA-exato, **somente upstream** |
| Runtime transformado do Minecraft/NeoForge instalado | ⚠️ **NÃO VERIFICADO** |
| Ordem, retorno, side e aceitação em `Level.addFreshEntity` para Galena | ⚠️ **NÃO VERIFICADO** |
| Reversão de `ItemStack.setCount(0)`, inventário e persistência | ⚠️ **NÃO VERIFICADO** |
| Hook mutador transacional e seguro de perks | ⛔ **NÃO VERIFICADO** — `NO_MUTATION` |
| QA física em cliente/servidor/modpack | ⚠️ **NÃO TESTADA** |

O Black Arcana mantém autoridade sobre seus rituais, casting e `WorldEffectPolicy`. O RPG Skill Tree permanece sibling/provider para progressão, atributos, Mastery e perks via boundary real, deduplicado, autorizado e server-owned. Uma linha de evento ou um pedido de spawn **não** constitui um cast concluído nem autoriza conceder Mastery.

## 4. Reprodução e critério de limitação

```sh
python3 docs/qa/alexscaves_1010_galena_neoforge_211248_entity_join_patches_probe.py --selftest
python3 docs/qa/alexscaves_1010_galena_neoforge_211248_entity_join_patches_probe.py \
  --userdev /caminho/neoforge-21.1.248-userdev.jar \
  --output /diretorio-novo/report.json
python3 docs/qa/alexscaves_1010_galena_neoforge_211248_entity_join_patches_checks.py \
  --report /diretorio-novo/report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-ENTITY-JOIN-PATCHES-21.1.248.json' \
  --adversarial
```

A [CI](../../../../.github/workflows/alexscaves-1010-galena-neoforge-211248-entity-join-patches.yml) valida checksum público, hash/tamanho fixos da sonda, SHA-256 exato do JSON e rejeições adversariais. Se uma dessas provas falhar, **fail-closed**; não reaproveitar resultados de versão adjacente.

**Pendências próximas:** obter as janelas causalmente relevantes de `ServerLevel` e `PersistentEntitySectionManager` de forma clean-room, identificar ramo de cancelamento e retorno, determinar alcance no callpath de `MagneticWeaponEntity`, verificar comportamento do inventário após recusa e realizar testes físicos quando possível. Não se declara certificação da ficha Galena até essas pendências serem resolvidas.

**Índices e contadores:** nova prova de subcontrato de patch **não** adiciona raiz mágica nem ficha individual completa. Manter Alex's Caves **130/134 estáticas** e global **269/2446** no recorte observado; **4/164** providers com catálogo documental concluído e **0/164** integralmente perk-ready.
