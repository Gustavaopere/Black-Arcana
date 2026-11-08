# Alex's Caves Continued — Straight Hook 1.0.10: prova estática exata

**Estado:** contrato técnico **estático** individual SHA-exato; `NO_MUTATION`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; universo do provider não encerrado.

## Artefato e proveniência

- Minecraft **1.21.1**, NeoForge, Java 21.
- Publisher e artefato físico auditado: `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge arquivo `8856293`), 75.279.314 bytes.
- SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- SHA-256: `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Recurso `data/alexscaves/enchantment/straight_hook.json` (369 bytes), SHA-256 `75508b5c035e6e240a17ca3e31a4757838cb03e6b7f444e2ece49df284cc3b6f`.
- Tag `#alexscaves:enchantable/candy_cane_hook` SHA-256 `b1d1990dd02fec11c14976f0f0a893e30b6c25e443efc013428cbdd4ef334310`.
- [Manifesto selado e auditável](EXACT-STRAIGHT-HOOK-STATIC-1.0.10.json) contém identidade, JSON, classes, métodos, hashes, janelas JVM e limites de prova. A primeira sonda read-only executou no [run 42524688014](https://github.com/Gustavaopere/Black-Arcana/actions/runs/42524688014); a validação exata do método e testes sintéticos passaram no [run 42525288364](https://github.com/Gustavaopere/Black-Arcana/actions/runs/42525288364).

## Grafo de métodos e evidências

- `ACEnchantmentRegistry.class` SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32`.
- `CandyCaneHookEntity.class` SHA-256 `e590bb67ea2b594861a30b05a5099fbd5eafe2920ff867883aaa6fd7cec478f8`; 33 métodos detectados.
- `CandyCaneHookItem.class` SHA-256 `d999251e494c45420e58881181e9d67757247b6865dc4a547bf0da8a46cf8e44`; 13 métodos detectados.
- `CandyCaneHookEntity(Player,Level,ItemStack,boolean)V` (231 instruções), digest parseado `7a0daa960e96a3a43a051b1cde2e3129701e5581ce44657bd9d283712e402322`: `STRAIGHT_HOOK@437` → `ACCompat.enchantLevel@440` → `ifle 460@443` → `RESISTS_GRAVITY@450` → `SynchedEntityData.set@457`. O nível **positivo** na stack grava `true`; a leitura é snapshot da criação.
- `defineSynchedData(Builder)V` (47 instruções), digest `0480c1d0669174f700e8ef829cb9ac645d1b4705c6bf12142d146dd25d907cfe`, define `RESISTS_GRAVITY=false` em `@82–90`.
- `getDefaultGravity()D` (20 instruções **integralmente verificadas**), digest `6661bcce0135dbf5e4a239c8277c9ca7ebc4093322584ce7140b8376247e9695`:

| Offset JVM | Gate ou retorno |
|---|---|
| `1–4` | `isReeling()`; se verdadeiro, desvia para `40` |
| `11–23` | Lê `RESISTS_GRAVITY`; se falso, desvia para `44` |
| `27–37` | `getDeltaMovement().horizontalDistance()` comparado a `0.05000000074505806D`; `ifle 44` |
| `40–41` | Retorna `0D` (via `goto 47`) |
| `44–47` | Caso contrário, retorna `0.07999999821186066D` |

Em particular, `isReeling` também zera o retorno sem o encantamento. A resistência só zera a gravidade no voo sem recolhimento quando a velocidade horizontal é **estritamente maior** que o limiar. A física efetiva ainda depende de engine e game QA. `tick()V`, `fling()V` e callbacks de colisão continuam provider-native; a ficha [Sharp Cane](enchantments/sharp-cane.md) apresenta os contratos prévios do mesmo classfile para owner, busca, dano solicitado e NBT.

A sonda percorreu **1.555 classfiles**: token `STRAIGHT_HOOK` diretamente no registry e na entidade do gancho, e `RESISTS_GRAVITY` apenas na entidade. Esse scan não exclui consumidores externos, reflexão ou transformação.

## Reprodução sem redistribuir código de terceiros

```sh
python3 docs/qa/alexscaves_1010_straight_hook_static_probe_test.py -v
python3 docs/qa/alexscaves_1010_straight_hook_static_probe.py \
  --jar '/caminho/alexscaves-1.0.10-neoforge+1.21.1.jar' \
  --javap "$JAVA_HOME/bin/javap" \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-STRAIGHT-HOOK-STATIC-1.0.10.json'
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

A sonda exige SHA-1, SHA-256, tamanho, JSON/tag, hashes de classes, método inteiro de gravidade e retornos/jumps exatos. Testes sintéticos impedem que mudança de branch seja promovida a evidência. O JAR não é comitado; a inspeção é somente leitura, de interoperabilidade clean-room.

## Autoridade, limites e QA pendente

O `RESISTS_GRAVITY` é estado sincronizado; seus próprios overrides `readAdditionalSaveData` e `addAdditionalSaveData` não o serializam explicitamente. Não se prova por isso perda ou retenção física após reload, pois persistência herdada e reconstrução permanecem fora da sonda. Velocidade física, alcance, PvP, world safety, uso de datapacks, compatibilidade de encantamentos, hooks, QA em cliente/dedicated server e multiplayer seguem `NOT_VERIFIED`/`NOT_TESTED`.

**Separação:** contrato individual estático ✅; nenhum hook mutador homologado; nenhum adapter executável integrado; QA física não testada; provider integral não fechado. Aplicar `NO_MUTATION`/fail-closed, sem novo cast, duplicação de dano, XP, Mastery ou custos.
