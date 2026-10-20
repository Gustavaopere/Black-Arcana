# Somake 1.0.9 — Funeral Bloom: consumidores estruturais de raio e seleção de alvos

**Estado vigente (PR #841; 20/10/2026):** ✅ SHA-exata a cadeia de raio até os argumentos X/Z de `AABB.inflate(R,10.5d,R)` e **o resultado dessa expansão entregue ao argumento AABB de `ServerLevel.getEntitiesOfClass(Class,AABB,Predicate)` pelo slot JVM 3** · ⚠️ caixa receptora, comportamento do predicado, alvos aceitos, buds/impacto real e QA físico não demonstrados · ⛔ perk mutadora `FAIL_CLOSED`. Resultados históricos abaixo conservam o escopo de cada prova.

## Proveniência física

- Modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`, Somake `somakespells-1.0.9-1.21.1.jar`, CurseForge File **8867079**, mod ID `somakespells`, SHA-1 **`171841ac9f802be9309ecc166c1d972ac6d404c0`**. Ambiente Minecraft 1.21.1 / NeoForge / Java21.
- [Workflow de auditoria de consumidores #39262591589](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39262591589): `SUCCESS`, **9 testes** sintéticos/negativos e inspeção de 3 classfiles físicos. Um HEAD subsequente congela o conjunto esperado de callsites e descritores de versão exata; só resultados desse HEAD são elegíveis para merge.
- [Verificador](../../../../docs/qa/somake_109_radius_consumers.py), [testes](../../../../docs/qa/somake_109_radius_consumers_test.py), [workflow](../../../../.github/workflows/somake-109-radius-consumers.yml). A saída contém assinaturas de métodos e referências simbólicas agrupadas por método, nunca JAR, implementação Java, bytecode ou assets do publisher.

## Matriz estrutural dos métodos compilados

| Classe / método | Instruções JVM | Invocações estáticas/virtuais/especiais | `invokedynamic` | Referências relevantes |
|---|---:|---:|---:|---|
| `FuneralBloomSpell.onCast(Level,int,LivingEntity,CastSource,MagicData)` | 81 | 21 | 1 | `getRadius(int,LivingEntity):float`; `getImpactDamage(int,LivingEntity):float`; construtor de `FuneralBloomControllerEntity` |
| `FuneralBloomSpell.getRadius(int,LivingEntity)` | 28 | 4 | 0 | Getter com duas expressões certificadas [na auditoria de caminhos](EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md) |
| `FuneralBloomControllerEntity.tick()` | 156 | 29 | 0 | `getRadius():float` e `launchWave(ServerLevel):void` |
| `FuneralBloomControllerEntity.launchWave(ServerLevel)` | 196 | 36 | 2 | `getRadius():float`, `AABB.inflate(double,double,double)`, `ServerLevel.getEntitiesOfClass`, `getOwner()`, criação de `FuneralBloomBudEntity` |
| `FuneralBloomBudEntity.tick()` | 150 | 33 | 0 | lifecycle, dependência do estado da controller (`isRemoved`) e posições da entidade |
| `FuneralBloomBudEntity.impact(ServerLevel)` | 279 | 35 | 0 | `LivingEntity.getBoundingBox`, `AABB.inflate(double,double,double)`, `ServerLevel.getEntitiesOfClass`, `DamageSources.applyDamage`, `SpellHealEvent`, `LivingEntity.heal`, `getOwner`, `isAlliedTo` |

## Descritores relevantes para integração

- `onCast` invoca `getRadius:(ILnet/minecraft/world/entity/LivingEntity;)F`, além de construir a controller com descriptor **`(Level,LivingEntity,float,int,int,int,int,float,int,int)void`** na forma JVM `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;FIIIIFII)V`. **Dois argumentos do construtor são float**, mas a coincidência com o getter não comprova qual posição recebe o resultado; isso exigirá reconstrução de pilha da instrução `invokespecial`.
- `controller.tick` e `controller.launchWave` invocam `getRadius:()F`, que é a superfície de leitura do estado da controller. Ainda não há prova de campo backing específico, valor originalmente copiado nem unidade de medida.
- `controller.launchWave` passa por `getBoundingBox`/`AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;`, depois possui chamada a `ServerLevel.getEntitiesOfClass` e instancia bud com descriptor **`(Level,FuneralBloomControllerEntity,LivingEntity,Vec3,int,float,int,int)void`**. A presença dessas referências no mesmo método **não** garante que `getRadius()` seja a dimensão de `inflate` nem que todo alvo elegível gere bud.
- `bud.impact` possui uma **segunda** chamada independente a `AABB.inflate:(DDD)Lnet/minecraft/world/phys/AABB;` e a `ServerLevel.getEntitiesOfClass`. Nesse método há referências a `DamageSources.applyDamage`, `SpellHealEvent` e `LivingEntity.heal`. O **método `bud.impact` não possui callsite direto `getRadius`**, então não atribuir automaticamente à área de dano o mesmo raio de `controller.launchWave`.

## Causalidade e status de perks

**Comprovado:** as referências de execução e símbolos acima existem nos seis métodos específicos do JAR 1.0.9; `onCast` conhece o getter do spell e a construção da controller; a controller consulta seu próprio `getRadius` e possui um caminho de seleção; a bud possui seleção/área e efeitos próprios. **Não comprovado:** dataflow de valores através dos argumentos dos construtores, distância da AABB em cada fase, hierarquia de branch/lifetime, alcance em blocos, eficácia de dano/cura/Wither, deduplicação por vítima, owner válido, comportamento em cliente/multiplayer ou presença real da API modificadora.

Dois eixos potenciais permanecem separados no catálogo: **raio de seleção/lançamento de buds** e **área de impacto de cada bud**. Mesmo quando ambos usam `AABB.inflate`, podem ter escalas e regras independentes. Não usar o retorno de `FuneralBloomSpell.getRadius` para implementar uma perk de área sem prova de dependência e hook versionado.

- ⛔ **FAIL_CLOSED** para perks per-player de raio, tamanho de área, targeting, dano, status, duração e quantidade de buds.
- ⚠️ `invokedynamic` ocorre em `onCast` (1) e `launchWave` (2): o probe registra a contagem, **não** imputa automaticamente alvo de lambda, predicado ou callback.
- ⚠️ Stage 06.05 segue 🟡; Stage 09 retém QA provider-loaded, Survival, cliente/multiplayer e modpack físico, conforme D035. Black Arcana mantém autoridade do runtime próprio; Somake executa sua magia; Iron's preserva o host e recursos; RPG Skill Tree apenas progressão por contrato real.

**Métricas:** Somake **83/83** identidades previamente inventariadas; cinco fichas com auditoria de entidades downstream sobre 83 (**6,02%**), sete classfiles downstream distintos no acumulado. **Zero** identidade ou adaptador adicional neste lote. [Ficha individual](registry-1.0.9/funeral-bloom.md) · [raio JVM](EXACT-BINARY-FUNERAL-BLOOM-RADIUS-TYPED-1.0.9.md) · [controller/bud](EXACT-BINARY-FUNERAL-BLOOM-BUD-1.0.9.md).

## Prova de operandos da expansão da AABB — 19/10/2026 (PR #840)

**Publisher SHA-exato:** `somakespells-1.0.9-1.21.1.jar`, CurseForge File `8867079`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. Na [auditoria Java21 #39304248399](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39304248399), **21 testes sintéticos/negativos passaram**; os três argumentos `double` de `FuneralBloomControllerEntity.launchWave(ServerLevel) → AABB.inflate:(DDD)AABB` foram rastreados por uma sequência local JVM estrita, não apenas pelo conjunto de callsites.

| Argumento de `inflate` | Proveniência certificada, versão 1.0.9 |
|---|---|
| Primeiro — **X** | `aload_0 → invokevirtual getRadius:()F → f2d` da controller |
| Segundo — **Y** | literal tipado JVM **`10.5d`** (`double`), sem consumo de `getRadius` nessa posição |
| Terceiro — **Z** | `aload_0 → invokevirtual getRadius:()F → f2d` da controller |

**Expressão certificada dos operandos:** `AABB.inflate((double) controller.getRadius(), 10.5d, (double) controller.getRadius())`. São argumentos de expansão nos três eixos do objeto AABB, não uma prova de raio esférico, de dano ou de aquisição de alvo no mundo. O getter da controller lê `SynchedEntityData.get(DATA_RADIUS)`; a cadeia upstream `FuneralBloomSpell.getRadius → primeiro float do construtor → setRadius(clamp 6–18) → DATA_RADIUS` já foi validada nas PRs #838/#839. O getter upstream do spell possui clamp separado `10–15` para entradas finitas (auditoria tipada independente).

**Por que foi necessária a segunda hipótese:** o [scanner estrutural SHA-exato #39303857720](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39303857720) encontrou três chamadas `getRadius` no método inteiro, mas **somente duas antes** da única chamada `inflate`, com conversões `f2d` e intervalos relativos de instruções 5 e 1. O padrão rejeitado de três getters adjacentes retornou `NOT_PROVED`, corretamente; o modelo local de **dois getters X/Z mais literal `double` em Y** foi então certificado sem reclassificar chamadas posteriores.

**Limites estritos:** a cadeia do **objeto AABB receptor** e o encaminhamento da **AABB resultante** a `ServerLevel.getEntitiesOfClass` não foram aqui reconstruídos; tampouco a escolha do owner/caster, filtros de distância/equipe, cardinalidade, criação efetiva de buds, `FuneralBloomBudEntity.impact` (AABB própria), dano/cura, alcance percebido em blocos, configs, Survival, cliente ou multiplayer. Não interpretar `10.5d` como alcance vertical **efetivo** de uma perk antes do consumidor e da QA. A ausência de hook público de mutação por jogador mantém ⛔ `FAIL_CLOSED`.

**Contagens:** Somake **83/83** IDs exatos; **5/83** fichas com entidade downstream auditada na campanha e **0** adapters mutadores homologados. Não acrescenta novo spell nem permite promoção de Stage. Sem redistribuir JAR, bytecode, código ou assets do provider.

## Nova prova física: AABB expandida → slot JVM 3 → consulta de entidades (20/10/2026; PR #841)

**Contexto exato:** `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`; Somake Spells 1.0.9, mod ID `somakespells`, File 8867079, `somakespells-1.0.9-1.21.1.jar`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`. Java 21; método `com.somake.somakespells.entity.FuneralBloomControllerEntity#launchWave(ServerLevel)`, **196 instruções JVM**.

O [workflow #39465768438](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39465768438) executou **28 testes** e identificou fisicamente `PROVED_WAVE_INFLATE_RESULT_CONSUMED_BY_ENTITY_QUERY` / `aabb_transport=via_local_3`. Após adicionar gate estrito de versão, o [workflow #39466062186](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39466062186) concluiu `SUCCESS` com **29 testes** e `PASS_SHA_EXACT_WAVE_XZ_RADIUS_Y_10_5_AND_QUERY_AABB_LINK`.

**Certificado no corpo compilado:** após `AABB.inflate((double)getRadius(),10.5d,(double)getRadius())`, o objeto AABB produzido é guardado em `astore_3`. Na mesma janela sem escritas intermediárias sobre esse slot, `aload_3` devolve a caixa à pilha; o argumento AABB é consumido pelo descriptor exato `ServerLevel.getEntitiesOfClass:(Ljava/lang/Class;Lnet/minecraft/world/phys/AABB;Ljava/util/function/Predicate;)Ljava/util/List;`. O fluxo abrange **nove instruções intermediárias** e **uma consulta**. O argumento `Class` é `LivingEntity`. O `Predicate` é produzido por `invokedynamic` que captura referências tipadas da controller e de `LivingEntity`; sua **lógica de aceitação interna NÃO foi examinada**.

**RED → GREEN:** a fixture de passagem direta falhou corretamente no [RED #39465037334](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39465037334), pois o JAR real possui armazenamento intermediário; o [GREEN #39465768438](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39465768438) certificou o novo padrão. O gate de regressão físico falhou de propósito em sete desvios no [RED #39465962139](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39465962139) e passou no [GREEN #39466062186](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39466062186), que exige slot local 3, nove instruções, descriptor exato e fingerprint de 196 instruções.

**Limites:** a relação **expansão → consulta de candidatos** está comprovada, mas não a geometria inicial da caixa receptora, nem o resultado efetivo do `Predicate`, elegibilidade PvP/aliados, distância extra, cardinalidade, escolha final, formação de buds ou AABB independente em `FuneralBloomBudEntity.impact`. Não há API/hook homologado de mutação per-player; **⛔ FAIL_CLOSED**. Esta auditoria acrescenta profundidade a uma magia preexistente, não IDs ou adapters. Não redistribui JAR, bytecode, implementação ou assets do provider.
