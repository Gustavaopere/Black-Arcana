# Targeted Ricochet 1.0.10 — prova estática exata do Shot Gum e Gumball

**Contrato individual:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. Hooks mutadores `NOT_VERIFIED`, QA física `NOT_TESTED`, runtime `NO_MUTATION`. Prova de emissão e ricochete *compilados*, não de alvos atingidos em jogo.

## Origem e JAR

- Minecraft 1.21.1 / NeoForge / Java 21. Modlist física RPG Skill Tree #019: `alexscaves-1.0.10-neoforge+1.21.1.jar`.
- Publisher CurseForge file `8856293`; 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- `data/alexscaves/enchantment/targeted_ricochet.json` (422 bytes), SHA-256 `adb5dfde437fbe38910045b6ec593103c43224224c8ab3a0101dec522a5ebb1e`; `supported_items=#alexscaves:enchantable/shot_gum`; `exclusive_set=[alexscaves:triple_split]`.
- `data/alexscaves/tags/item/enchantable/shot_gum.json` SHA-256 `3ccaf9482a8187e3c99f45ff7d5a28c7c73fe39c1840daef13f294821301e31d`.
- [Manifesto individual SHA-exato, digests e janelas JVM](EXACT-TARGETED-RICOCHET-STATIC-1.0.10.json), selado pela sonda e aprovado no [CI 42537721876](https://github.com/Gustavaopere/Black-Arcana/actions/runs/42537721876). Não reutilizar provas da versão pública adjacente 1.1.1 como paridade automática com 1.0.10.

## Classfiles e pontos de consumo

- `ACEnchantmentRegistry.class`: SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32`.
- `ShotGumItem.class`: SHA-256 `08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238`.
- `GumballEntity.class`: SHA-256 `343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535`.

| Método JVM | Instruções | Digest SHA-256 do parse |
|---|---:|---|
| `ShotGumItem.acInventoryTick(ItemStack,Level,Entity,boolean)V` | 285 | `6f9325406aaf142af4b415bff94b9123882b72a2ab981370d9be30a5e7c18093` |
| `GumballEntity.bounceFromDirection(Direction)V` | 198 | `0f687d784c92e2b8e7eebfc3cc9a85041b5fdfb37c6c5e4a32aaa2489df66282` |
| `GumballEntity.onHit(HitResult)V` | 79 | `6ba773699f0bddfbc33bff72ee912bdcd63896fde4a09c9bbb19c7ae795dcbe2` |
| `GumballEntity.onHitEntity(EntityHitResult)V` | 162 | `0797340fb44ecfa83c2b77dc07a12e1101b5427d9cb3ca5e4308b054ee309ffe` |
| `GumballEntity.defineSynchedData(Builder)V` | 43 | `deea79e6acbb3c39be970d0c9fe5366176f727f01fde3cbbb890136597549d05` |
| `GumballEntity.setTargetsOnBounce(Z)V` | 7 | `ab92c0d0d82ac234c6e5dbe910171ca532a0a0cadc5c69d7bb81363e27522979` |
| `GumballEntity.targetsOnBounce()Z` | 7 | `9cd03a004d137fe29438411500c8948d0216ea9536340a2a5ad5a8c0ebff3db1` |
| `GumballEntity.addAdditionalSaveData(CompoundTag)V` | 9 | `71d94d6babff7eb6ec1b9ff66f035c970ed9cfd4bf428cfbde1e6dfc9e7a52cf` |
| `GumballEntity.readAdditionalSaveData(CompoundTag)V` | 9 | `6ab17f1d19425646dc4e5bf69274f479ff3634b7f552c005af6041c408c765e5` |

## Branches estáticas e offsets selecionados

- **Arma:** `ShotGumItem.acInventoryTick` exige `S && T==5` antes da criação. `TARGETED_RICOCHET@138`, `ACCompat.enchantLevel@141`, `ifle151@144`, booleano em `@147/151`, `setTargetsOnBounce@434`. Não comprova que `Level.addFreshEntity` aceitou o projétil.
- **Estado:** `GumballEntity.defineSynchedData` define `TARGETS_ON_BOUNCE=false` em `@49–56`. Set e get são métodos próprios de 7 instruções; a ativação é configurada na instância lançada, não um buff global.
- **Parada explosiva:** `bounceFromDirection@3/7/12/19` consulta contador e máximo, testa explosivo e pode retornar após zerar velocidade/definir bounces. O ramo é anterior à busca do alvo.
- **Busca:** `targetsOnBounce@39/ifeq290@42`; AABB eye-centered `±10D` em `@70–101`; seleção de `LivingEntity`; filtros contra owner e `candidate.isAlliedTo(owner)` em `@133–152`, lista de hits em `@155–172` e menor `distanceTo` em `@175–200`. Não há `LOS` explícita, `isAlive` local ou filtro de aliança reversa neste laço.
- **Redirecionamento:** ao encontrar candidato, `@203–209` marca ramo; só no servidor incrementa contador em `@210–227`; se `B>M`, solicita descarte `@230–245`. Caso contrário, calcula vetor `target.eyePosition−gumball.position`, normaliza em `@260`, escala em `0.800000011920929d @263` e chama `setDeltaMovement@287`.
- **Sem candidato:** `@318–458` reflete componente do eixo de impacto (coeficientes compilados `0.800000011920929d` para X/Z, `0.5d` para Y), preserva outros componentes e atualiza contagem somente no servidor. Som usa contador independente de 5 ticks.
- **Colisão:** `onHit@2` chama super antes dos filtros locais, bloco com colisão chama bounce `@54` e entidade elegível adiciona ID de histórico e chama bounce `@168` quando `!splitsOnHit`. O histórico não é uma barreira geral contra `hurt` repetido.
- **Dano e split:** `onHitEntity` solicita `Entity.hurt@139` com retorno descartado. Com split ativo tenta três filhos, copia a flag `targetsOnBounce@305–308`, mas não atribui explicitamente owner. JSON declara exclusão com Triple Split, sem assegurar que dados externos nunca criem a combinação.
- **NBT próprio:** `addAdditionalSaveData` e `readAdditionalSaveData` chamam super e só escrevem/leem `Color`. Persistência do flag, hitIds e owner herdado, além de mensagens/sync físicos, continuam `NOT_VERIFIED`.

**Censo de referências diretas:** 1.555 classfiles; `TARGETED_RICOCHET` em `ShotGumItem` e registry; `TARGETS_ON_BOUNCE` na entidade Gumball. Reflexão, code injection e consumidores externos não são negados por esse censo.

## Comandos de reprodução (JAR local, read-only)

```sh
python3 docs/qa/alexscaves_1010_targeted_ricochet_static_probe_test.py -v
python3 docs/qa/alexscaves_1010_targeted_ricochet_static_probe.py \
  --jar '/caminho/alexscaves-1.0.10-neoforge+1.21.1.jar' \
  --javap "$JAVA_HOME/bin/javap" \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TARGETED-RICOCHET-STATIC-1.0.10.json'
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

A sonda verifica SHA-1/SHA-256/tamanho, recursos e tag, hash de classes, hashes parseados de métodos e asserts fail-closed de CFG, sem descompilar/republicar source de terceiros. Os testes sintéticos verificam rejeição de offsets/desvios/símbolos alterados.

## Escopo de validade

Certificado estático individual ✅ para o publisher 1.0.10. Não certifica dano líquido, número de projéteis inseridos, alcance efetivo, LOS de engine, hits em jogo, proteção PvP/claims, persistência após reload, owner de descendentes, hook de perk, Mastery ou multiplayer. Não altera o runtime Black Arcana ou RPG Skill Tree; `NO_MUTATION` permanece obrigatório. Sem prova do universo completo, Alex's Caves não pode ser declarado integralmente catalogado.
