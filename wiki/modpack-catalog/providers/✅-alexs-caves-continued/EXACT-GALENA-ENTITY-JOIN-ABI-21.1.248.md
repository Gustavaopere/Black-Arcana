# Galena Gauntlet — ABI de entrada de entidades do alvo NeoForge 21.1.248

**Estado:** ⚠️ subcontrato ABI **estático, de escopo limitado, reproduzido e SHA-exato**; não é certificação técnica individual integral da Galena, hook mutador ou QA física. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · `provider_universe_closed=false` · `semantic_magic_roots_delta=0`.

## 1. Proveniência e seleção da versão

- **Provider consumidor:** Alex's Caves Continued `alexscaves` **1.0.10**, Minecraft 1.21.1 / NeoForge / Java 21; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` de **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A [modlist do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/World%20Gen/%E2%9C%85-alexs-caves-continued%20v1.0.10.md) registra SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. **Novo dump do JAR da instância: não verificado.**
- **Engine de compilação pinada:** `neo_version=21.1.248` nos `gradle.properties` de [Black Arcana](https://github.com/Gustavaopere/Black-Arcana/blob/main/gradle.properties) e [RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/gradle.properties) no checkpoint de 23/11/2026. Isso comprova a **versão de compilação**, não necessariamente todos os bytes de runtime de uma instância externa.
- **Fonte upstream efetivamente examinada:** [Maven oficial NeoForge 21.1.248](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.248/). `neoforge-21.1.248-universal.jar`: **3.551.268 bytes**, SHA-256 `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`, **2.521 membros**; `neoforge-21.1.248-sources.jar`: **1.796.948 bytes**, SHA-256 `b4b912457549ff586873ce78b39b08af96f11a0e3a54c6b77576c6a25907083f`, **1.978 membros**. Ambos conferidos contra os SHA-256 publicados pelo Maven, além de serem pinados na sonda.
- **Evidência do alvo:** [workflow inicial de descoberta #45182745228](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45182745228), job `137720448259`, status **success**. Relatório `report.json`: **11.559 bytes**, SHA-256 `002f2f736ccd9e3af35f0c4bebfac03cc58127b40cdfaad5cca70a8a964aa3c1`. O relatório é artefato temporário; a [sonda](../../../../docs/qa/alexscaves_1010_galena_neoforge_211248_entity_join_abi_probe.py), o [manifesto](EXACT-GALENA-ENTITY-JOIN-ABI-21.1.248.json), o [checker](../../../../docs/qa/alexscaves_1010_galena_neoforge_entity_join_abi_checks.py) e a [CI direcionada](../../../../.github/workflows/alexscaves-1010-galena-neoforge-211248-entity-join-abi.yml) permanecem versionados. Os novos gates de checker devem ser confirmados na **HEAD final da PR**, sem aproveitar a conclusão de descoberta anterior como substituta.

## 2. Classes e assinaturas reproduzidas

| Classfile upstream exato | SHA-256 | Métodos declarados |
|---|---|---:|
| `net/neoforged/neoforge/event/entity/EntityJoinLevelEvent` | `644af7ec062b1497050a50ecb1936aadcf097eb63afd6fa7d56fc7a063e4fe20` | 4 |
| `net/neoforged/neoforge/event/entity/EntityEvent` | `23e99c7a8e2a144ed15c3c755c6a81403bd677215ccb6c967f6f95fd2d25d86e` | 2 |
| `net/neoforged/neoforge/event/EventHooks` | `f810377f87c95c04bb4de7a7ac68e8f4862f9ca33a34cc74e067e65e2a92d66b` | 114 |

O arquivo `sources.jar!/net/neoforged/neoforge/event/entity/EntityJoinLevelEvent.java` tem SHA-256 `63f3a66ce430bc4ca49ae03190733f95baad7387a85c5417450d9947acca929f`. Sua implementação original não foi copiada.

**`EntityJoinLevelEvent`:** a declaração de classe no artefato inspecionado inclui `ICancellableEvent`. O `javap -p -s` identificou exatamente:

| Método | Descritor JVM |
|---|---|
| Construtor `(Entity, Level)` | `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/level/Level;)V` |
| Construtor `(Entity, Level, boolean)` | `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/level/Level;Z)V` |
| `getLevel()` | `()Lnet/minecraft/world/level/Level;` |
| `loadedFromDisk()` | `()Z` |

**`EntityEvent`:** declara construtor `(Entity)` → `(Lnet/minecraft/world/entity/Entity;)V` e `getEntity()` → `()Lnet/minecraft/world/entity/Entity;`. Há **zero assinaturas não resolvidas** pelo parser para os três tipos inspecionados. O subconjunto de `EventHooks` selecionado por nome (`join` ou `entity`) não inclui métodos com `join` no identificador: isso **não equivale** à ausência de publicação do evento por outras classes/patches Minecraft.

## 3. Comparação SHA-exata com NeoForge 21.1.250

A [auditoria independente da versão adjacente 21.1.250](EXACT-GALENA-ENTITY-JOIN-ABI-21.1.250.md) reproduziu os mesmos **três hashes de classfiles** e o mesmo **hash do arquivo-fonte do evento**. Portanto, **esses bytes específicos são idênticos em ambos os artefatos `universal` oficiais**; os conjuntos gerais de JARs são diferentes e não foram provados equivalentes.

| Objeto confrontado | NeoForge 21.1.248 × 21.1.250 |
|---|---|
| `EntityJoinLevelEvent.class` | ✅ SHA-256 igual |
| `EntityEvent.class` | ✅ SHA-256 igual |
| `EventHooks.class` | ✅ SHA-256 igual |
| `EntityJoinLevelEvent.java` do `sources.jar` | ✅ SHA-256 igual |
| JAR `universal` completo | ⚠️ **SHA-256 diferente** |
| JAR `sources` completo | ⚠️ **SHA-256 diferente** |
| `Level.addFreshEntity`, transformação Minecraft, event bus e lifecycle | ⛔ **não comparados nem certificados** |

Isso elimina a incerteza de versão **somente nesse recorte ABI**. Não transporta certificação de runtime, segurança ou disponibilidade de hooks de uma versão para outra.

## 4. Relevância para a Galena e gates ausentes

O [dossiê SHA-exato de retorno/drop do publisher 1.0.10](EXACT-GALENA-GAUNTLET-RETURN-DROP-1.0.10.md) demonstra que `GalenaGauntletItem.onUseTick` solicita `ItemStack.setCount(0)` na stack da arma oposta antes de `ACCompat.createEntity` e `Level.addFreshEntity`, descartando o booleano da última chamada. A [ponte nativa `ACCompat.createEntity`](EXACT-GALENA-ACCOMPAT-COMBAT-BRIDGES-1.0.10.md) delega a `EntityType.create(level)`; não garante referência não nula, spawn aceito, restituição ou rollback.

O evento `EntityJoinLevelEvent` é uma **possível superfície de observação futura**, pois a ABI upstream é real e potencialmente cancelável. São **NÃO VERIFICADOS**: (a) seu disparo no caminho efetivo da `MagneticWeaponEntity`; (b) seu lado/ordem relativos à mutação `setCount(0)`, à criação e à inclusão no mundo; (c) o tratamento pelo engine do retorno negativo de `addFreshEntity`; (d) a integridade da stack e do NBT após recusa, reload, troca de dimensão, inventário cheio ou mod de proteção; (e) eventual autoria estável/UUID e deduplicação de XP, Mastery, kill e crafting; (f) desempenho e conflitos de outros listeners.

**Não inferir que o evento corrige falha de spawn, concede hook seguro, garante proteção de claims ou prova perda/duplicação.** Só a observação no servidor da conclusão real da ação, com deduplicação e autorização do provider, poderia sustentar perks. Black Arcana conserva autoridade sobre o runtime mágico e WorldEffectPolicy; RPG Skill Tree recebe progressão/atributos/Mastery apenas por boundary demonstrado.

## 5. Reprodução e certificação restrita

```sh
python3 docs/qa/alexscaves_1010_galena_neoforge_211248_entity_join_abi_probe.py \
  --universal /caminho/neoforge-21.1.248-universal.jar \
  --sources /caminho/neoforge-21.1.248-sources.jar \
  --javap /caminho/java21/bin/javap \
  --output /diretorio-novo/report.json

python3 docs/qa/alexscaves_1010_galena_neoforge_entity_join_abi_checks.py \
  --report /diretorio-novo/report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-ENTITY-JOIN-ABI-21.1.248.json' \
  --adversarial
```

A sonda rejeita JARs com hashes distintos, métodos faltantes e assinaturas irrecuperáveis. O checker valida manifesto, versão, descritores, a equivalência exata dos hashes dos classfiles e **25 falsificações adversariais**; esse número é cobertura planejada no código, não um resultado de execução **até a CI final apresentar sua saída**.

**Consequência para os índices:** a Galena continua ⚠️ parcial e o universo integral de Alex's Caves não está demonstrado. Manter **130/134 contratos técnicos estáticos no recorte observado**, **269/2.446 contratos globais observados** e **4/164 catálogos documentais de providers**, sem incrementar contadores por mera descoberta da ABI. `NO_MUTATION` e fail-closed permanecem obrigatórios.
