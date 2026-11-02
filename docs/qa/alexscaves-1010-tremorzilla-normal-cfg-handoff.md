# Handoff: Tremorzilla Beam — dominância no CFG normal JVM, 1.0.10

**Estado:** evidência estática SHA-exata do JAR publisher 1.0.10; **não** equivale a execução em modpack, política efetiva de PvP/claims ou hook seguro. Complementa [análise de referências de mundo/LOS](alexscaves-1010-tremorzilla-world-los-handoff.md) da PR #1005, sem alterar Black Arcana ou RPG Skill Tree.

## Fonte e método

- Modlist de autoridade: `neoforge-rpg-skilltree/main@59ff2a0e827fd08faa603f4482f8104ac433383c`, item `alexscaves-1.0.10-neoforge+1.21.1.jar` (mod id `alexscaves`).
- JAR SHA-256: `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` (75.279.314 bytes).
- `TremorzillaEntity.class` SHA-256: `e1ac60a8005f9414dde1d25a92a2110df65cef145c3225e9c2557c96672fe8dc`.
- Método: grafo orientado de bytecode **normal, intramétodo**, a partir de `javap -c -p -s`, com arestas de desvios condicionais (`if*`), `goto*`, fallthrough e terminação. Não modela exception table, dispatch ou transformações; desvio desconhecido falha fechado. Uma chamada *A* domina o ponto *B* quando todo caminho normal alcançável até *B* passa por *A*. **Dominância da chamada não prova que seu retorno seja verificado ou que haja autorização.**
- [Manifesto selado exato](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TREMORZILLA-NORMAL-CFG-1.0.10.json), [sonda](alexscaves_1010_tremorzilla_normal_cfg_probe.py), [regressões](alexscaves_1010_tremorzilla_normal_cfg_probe_test.py), [workflow Java 21](../../.github/workflows/alexscaves-1010-tremorzilla-normal-cfg.yml).

## Grafo auditado

| Método | Instruções | Arestas normais | Retornos ao offset anterior (backedges) |
|---|---:|---:|---:|
| `breakBlocksAround(Vec3,float,boolean,boolean,float)` | 166 | 178 | 1 |
| `tickBreath()` | 306 | 323 | 1 |
| `canEntityBeHurtByBeam(LivingEntity,Vec3)` | 27 | 27 | 0 |

### Entrada de modificação de mundo

Em `breakBlocksAround`, `ACPlatform.canEntityGrief @12` **e** `Level.isClientSide @22` dominam, no CFG normal compilado, **cada um** dos seguintes sites:

| Operação | Offset | canEntityGrief @12 domina? | isClientSide @22 domina? |
|---|---:|---|---|
| `Level.destroyBlock` | 249 | Sim | Sim |
| `ACCompat.onBlockExploded` | 268 | Sim | Sim |
| `ACCompat.createEntity` | 296 | Sim | Sim |
| `Level.addFreshEntity` | 349 | Sim | Sim |

**Limite de leitura:** confirma que as chamadas nativas são atravessadas em caminhos normais até essas operações, **não** que `canEntityGrief` é suficiente para todos os claims, que a resposta do predicate seja aplicada corretamente, que os efeitos respeitem a `WorldEffectPolicy` de Black Arcana ou que não haja outros caminhos de mutação por mixin/provider.

### `tickBreath` — a chamada de raycast não domina todos os sites

Em `tickBreath`, a consulta `Level.isClientSide @4` domina os dois sites de `breakBlocksAround @525/@620` e os dois de `hurtEntitiesAround @552/@578`. Entretanto, a chamada local `Level.clip @393` **não** domina nenhum desses quatro sites: há caminhos **normais** no bytecode até cada um que não passam por essa chamada específica.

Isso **não prova** que o feixe cause dano através de paredes, que `canEntityBeHurtByBeam` não filtre o alvo, que o retorno do raycast seja ignorado ou que exista exploração em multiplayer. Confirma apenas uma diferença relevante na topologia do controle de fluxo do método. O `canEntityBeHurtByBeam` contém outro `Level.clip @37`, que domina sua consulta de resultado `BlockHitResult.getType @40`; sua semântica efetiva deve ser analisada separadamente.

## Próximos gates para contrato de perks

1. Reconstruir os ramos e os valores de retorno efetivamente consumidos por `ACPlatform.canEntityGrief`; examinar o helper da **mesma versão compilada**, inclusive compatibilidade com claims/modpacks.
2. Distinguir os caminhos de `tickBreath` com/sem `Level.clip @393` e sua relação com `canEntityBeHurtByBeam`, `beamServerTarget`, `beamTime`, recarga e target controlado.
3. Auditar `ACCompat.onBlockExploded`/`createEntity` e o comportamento físico da entidade nuclear no servidor do modpack, com `WorldEffectPolicy`/permissões reais.
4. Não expor mutações de dano/raio/duração a perks sem boundary de provider seguro, com prevenção de duplicação de dano, efeitos e Mastery.

**Decisão:** `Tremorzilla Beam=⚠️ NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `NO_MUTATION`, `physical_qa=NOT_TESTED`. Nenhuma raiz adicional, nenhuma promoção de fichas, de provider perk-ready ou do Stage 06.
