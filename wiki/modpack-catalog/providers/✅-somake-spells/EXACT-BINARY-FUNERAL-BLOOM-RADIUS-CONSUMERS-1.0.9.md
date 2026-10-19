# Somake 1.0.9 — Funeral Bloom: consumidores estruturais de raio e seleção de alvos

**Estado:** ✅ `EXACT_SHA1_METHOD_LEVEL_RADIUS_CONSUMER_REFERENCES` (JAR exato, callsites e descriptors JVM) · ⚠️ passagem de operandos, geometria e gameplay não demonstrados · ⛔ mutação via perks `FAIL_CLOSED`.

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
