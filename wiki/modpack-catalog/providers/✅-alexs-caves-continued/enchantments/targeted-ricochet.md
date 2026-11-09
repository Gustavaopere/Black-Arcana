# Targeted Ricochet — `alexscaves:targeted_ricochet` (1.0.10)

**Contrato individual:** ✅ certificado **somente estático** (`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`). Hook mutador `NOT_VERIFIED`; QA física `NOT_TESTED`; política `NO_MUTATION`. Nenhuma implementação de perk, cast novo ou autorização para modificar o provider.

## Identidade, descrição e proveniência

- **Provider:** Alex's Caves Continued, mod ID `alexscaves`, Minecraft 1.21.1 / NeoForge / Java 21. Entrada física #019 da modlist do RPG Skill Tree.
- **JAR instalado/publisher:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge arquivo `8856293`, **75.279.314 bytes**. SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **JSON próprio:** `data/alexscaves/enchantment/targeted_ricochet.json` (422 bytes), SHA-256 `adb5dfde437fbe38910045b6ec593103c43224224c8ab3a0101dec522a5ebb1e`; key compilada `ACEnchantmentRegistry.TARGETED_RICOCHET`.
- **Item elegível:** `#alexscaves:enchantable/shot_gum` com `alexscaves:shot_gum`, SHA da tag `3ccaf9482a8187e3c99f45ff7d5a28c7c73fe39c1840daef13f294821301e31d`.
- **Descrição funcional própria:** encantamento do Shot Gum que permite ao Gumball redirecionar o ricochete para a entidade viva elegível mais próxima após colisão. O texto inglês do JAR descreve essa intenção, mas **não** promete acerto, busca sem obstáculos ou novo ataque.

## Propriedades e custos publicados

| Parâmetro | Valor físico |
|---|---|
| `max_level` | **1** (I); consumer testa apenas nível `>0` |
| `weight` | `2` (peso de encantamento, não chance de hit) |
| `min_cost` | base `1`, incremento acima do primeiro `16`; nível I = 1 |
| `max_cost` | base `41`, incremento acima do primeiro `10`; nível I = 41 |
| `anvil_cost` | `4` (aquisição, não gasto por ricochete) |
| `slots` | `mainhand` |
| `exclusive_set` | `[alexscaves:triple_split]` no JSON; incompatibilidade declarativa, sem provar que um stack adulterado nunca contenha ambos |

## Ativação, condições e causalidade

`ShotGumItem.acInventoryTick(ItemStack,Level,Entity,boolean)` captura estado de disparo `S=isShooting(stack)` e tempo `T=getShootTime(stack)`; somente **`S && T==5`** entra no produtor de projéteis (`@81–89`). O valor do parâmetro `selected` não participa dessa guarda nesse corpo. O produtor lê `ACCompat.enchantLevel(stack,TARGETED_RICOCHET)` em `@137–144`; se o nível é positivo, produz booleano `true` (`@147–152`) e o aplica em `GumballEntity.setTargetsOnBounce(boolean)` (`@432–434`). O nível é lido na stack no disparo, **não** em cada novo bounce. O campo sincronizado `TARGETS_ON_BOUNCE` inicia em `false` (`defineSynchedData @49–56`).

O mesmo produtor nativo solicita **dois Gumballs normais** ou **um explosivo** (quando `EXPLOSIVE_FLAVOR` está ativo); o máximo solicitado de bounces é `M=4+2×level(BOUNCY_BALL)`. Dano inicial solicitado `4F` e velocidades iniciais de disparo `1.5F` normal ou `0.5F` explosivo, com dispersão `5F`, pertencem à arma, não a Targeted Ricochet. O pedido de inserção ocorre no lado servidor e o retorno de `Level.addFreshEntity` é descartado. Munição, cooldown de acionamento e desgaste permanecem [provider-native](../equipment/shot-gum.md).

## Geometria, seleção e ricochete

`GumballEntity.onHit(HitResult)` chama a superclasse antes de seus filtros. Em bloco com collision shape não vazio, chama `bounceFromDirection(face)`; em entidade que não é o owner nem outro Gumball, registra o ID em `hitEntityIds` e solicita o bounce se `!splitsOnHit`. **A lista não impede `Entity.hurt`**: `onHitEntity` não consulta `hitEntityIds` antes do pedido de dano. Não deduzir proteção contra hits duplicados.

`GumballEntity.bounceFromDirection(Direction)` (**198 instruções**) implementa a lógica condicional:

| Condição ou superfície | Contrato compilado |
|---|---|
| Saída explosiva prioritária | Se `B>M−1 && isExplosive()`, define `Vec3.ZERO`, escreve `BOUNCES=M` e retorna; não procura alvo naquele ramo |
| Flag de target | Se `TARGETS_ON_BOUNCE=false`, segue a reflexão normal |
| Volume de busca | `AABB(eyePosition+(-10,-10,-10), eyePosition+(10,10,10))`: **caixa 20 × 20 × 20**, não esfera de raio 10 |
| Tipo de candidato | `LivingEntity` via `Level.getEntitiesOfClass` |
| Owner | Quando presente, exclui candidato que é o owner ou `candidate.isAlliedTo(owner)`. **Não testa a relação inversa nesse seletor** |
| Hits anteriores | Exclui ID presente em `hitEntityIds`; essa lista é apenas filtro de próxima aquisição |
| Ordem | Menor `candidate.distanceTo(gumball)`; empate mantém o primeiro da enumeração |
| Vida e LOS | O laço próprio não chama `isAlive` nem `hasLineOfSight`; não inventar exclusões que dependem da engine |
| Vetor ao adquirir | `normalize(target.eyePosition − gumball.position) × 0.800000011920929D` e `setDeltaMovement` |
| Contador | Ao encontrar alvo, incrementa `BOUNCES` somente no servidor; se `B>M`, solicita descarte, sem o novo vetor desse ramo |
| Nenhum candidato | Usa reflexão normal: eixo X/Z do impacto invertido e escalado por `0.800000011920929D`; eixo Y por `0.5D`; demais componentes preservados |
| Limite no fallback | Contador também incrementado somente no servidor; descarte solicitado quando `B>M` |

Não confundir o volume de seleção com alcance balístico, o vetor escrito com velocidade final observada, nem o mecanismo após colisão com homing contínuo por tick. `bounceSoundCooldown=5` após som habilitado é apenas intervalo de som, **não** cooldown de magia ou de dano.

## Dano, secondary consumers, autoria e persistência

`GumballEntity.onHitEntity(EntityHitResult)` usa fonte de dano Gumball baseada no owner e faz o pedido nativo `Entity.hurt(source,getDamage())`, cujo retorno booleano é descartado. Os filtros de amizade do dano incluem condições próprias diferentes da busca direcionada. **Targeted Ricochet não adiciona dano, DamageType, knockback, cura, status ou disparos extras**; são N/A como efeitos diretos. Dano final, proteção PvP/claims e ataques aceitos não foram testados.

Quando `splitsOnHit` é verdadeiro, o método de hit tenta construir **três filhos** de Gumball, desativa split nos filhos e **copia** o flag `targetsOnBounce` (`@305–308`), além de dano, explosivo e máximo de bounces. Esse ramo **não chama `setOwner`** para os filhos, logo não comprova autoria herdada nem concede Mastery/XP ao atirador por presunção. O JSON de Targeted Ricochet exclui Triple Split declarativamente; a cópia existe no código e só tem relevância conjunta se outro mecanismo permitir esse estado.

`TARGETS_ON_BOUNCE` é booleano de `SynchedEntityData`, default `false`. Os overrides próprios `addAdditionalSaveData` e `readAdditionalSaveData` do Gumball (9 instruções cada) chamam `super` e gravam/leem diretamente somente `Color`, sem serialização própria de flag, lista de IDs, contagem ou vetor. Não concluir perda ou conservação após save/reload: persistência herdada, reconstrução de instância e rede permanecem `NOT_VERIFIED`. Filhos, owner e descarte efetivo também exigem QA física.

## Classes, signatures e rastreabilidade técnica

- `ShotGumItem.class` SHA-256 `08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238`; método `acInventoryTick(ItemStack,Level,Entity,boolean)V`, 285 instruções, digest `6f9325406aaf142af4b415bff94b9123882b72a2ab981370d9be30a5e7c18093`.
- `GumballEntity.class` SHA-256 `343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535`; `bounceFromDirection(Direction)V` 198 instruções/digest `0f687d784c92e2b8e7eebfc3cc9a85041b5fdfb37c6c5e4a32aaa2489df66282`, `onHit(HitResult)V` 79/digest `6ba773699f0bddfbc33bff72ee912bdcd63896fde4a09c9bbb19c7ae795dcbe2`, `onHitEntity(EntityHitResult)V` 162/digest `0797340fb44ecfa83c2b77dc07a12e1101b5427d9cb3ca5e4308b054ee309ffe`.
- `defineSynchedData(Builder)V` 43 instruções/digest `deea79e6acbb3c39be970d0c9fe5366176f727f01fde3cbbb890136597549d05`. `setTargetsOnBounce(Z)V` e `targetsOnBounce()Z` têm 7 instruções cada. Todos os digests de métodos, referências simbólicas e janelas JVM constam no manifesto.
- Censo direto de 1.555 classfiles: token `TARGETED_RICOCHET` apenas em registry e `ShotGumItem`; `TARGETS_ON_BOUNCE` apenas em `GumballEntity`. Reflections, mixins e mods externos podem acrescentar consumers.

## Design de perks / Mastery e limites

Uma futura perk poderia conceitualmente ampliar AABB/range, alterar filtros de owner, linha de visão, limite de bounces, chance de ricochete, vetor ou parâmetros de cooldown, mas não há **hook mutador real e seguro homologado**. `ShotGumItem.acInventoryTick` e `GumballEntity.bounceFromDirection` são consumidores privados do provider, não APIs do Black Arcana. RPG Skill Tree fornece progressão/atributos/Mastery por boundary real; Black Arcana preserva autoridade do runtime mágico e server authority.

Não adicionar casts, projéteis, dano ou XP por mera leitura do flag, pedido de bounce, tentativa de spawn, retorno de `hurt` descartado ou ID em lista. Evitar double-processing com split/explosive, cap externo sem prova, loops ilimitados, filtragem client-authoritative e attribution errada a filhos. **`NO_MUTATION` / fail-closed.**

## Reprodução e QA pendente

- [Manifesto SHA-exato](../EXACT-TARGETED-RICOCHET-STATIC-1.0.10.json), [prova e comandos](../EXACT-TARGETED-RICOCHET-STATIC-1.0.10.md), [sonda read-only](../../../../../docs/qa/alexscaves_1010_targeted_ricochet_static_probe.py), [testes sintéticos](../../../../../docs/qa/alexscaves_1010_targeted_ricochet_static_probe_test.py).
- Sonda verifica JAR/JSON/tag/classfiles/digests anteriores, CFG e offsets dos consumidores, filtros, branch explosivo, vetor e persistência própria. Logs da auditoria física SHA-exata: [run 42537721876](https://github.com/Gustavaopere/Black-Arcana/actions/runs/42537721876).
- **Pendências:** trajetória e número de hits reais, distância efetiva, distribuição dos candidatos/empates, PvP/claims, save/reload, sync servidor/cliente, caso Triple Split ilegítimo, ownership dos filhos, efeitos de datapacks e outros mods, integração mutadora e QA de modpack/dedicated server. Status de todos esses itens: `NOT_VERIFIED`/`NOT_TESTED`; o provider ainda não está fechado.
