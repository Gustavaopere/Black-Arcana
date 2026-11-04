# Alex's Caves Continued 1.0.10 — Humungous Hex SHA-exact contract

A [ficha técnica de Humungous Hex](enchantments/humungous-hex.md) encerra o **escopo estático individual** da identidade `alexscaves:humungous_hex`. São independentes a execução real do jogo, mutadores de perks, modificações de alcance/target e encerramento do universo inteiro de Alex's Caves Continued.

## Fonte de autoridade

- Modlist sibling: `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1, NeoForge, Java 21).
- Artefato publisher CurseForge 1645389/8856293: **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- [Manifesto congelado](EXACT-HUMUNGOUS-HEX-CONTRACT-1.0.10.json): JSON do encantamento e de Spell Lasting, item tag, idiomas selecionados, SHA de ficha, quatro classfiles (SugarStaffItem, SugarStaffHexEntity, SugarStaffModel, SugarStaffHexRenderer), descritores e digests dos métodos inspecionados, 11 pivôs compilados, limites explícitos. Não distribui JAR ou implementação do provider.
- [Sonda fail-closed](../../../../docs/qa/alexscaves_1010_humungous_hex_probe.py), [testes sintéticos](../../../../docs/qa/alexscaves_1010_humungous_hex_probe_test.py) e [workflow](../../../../.github/workflows/alexscaves-1010-humungous-hex.yml). O script confronta os dados com o artefato real, recusa divergência de hash/tamanho/identity/JSON/descritores/digest/offsets e prova que a documentação não sofreu drift.
- [Contrato Sugar Staff Hex já canônico](actions/sugar-staff-hex-cast.md), [evidência binária comum](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) e [auditoria de método/entidade](EXACT-TECHNICAL-CONTRACTS-1.0.10.md) dão a cadeia completa de casting, custo, targeting, contador, save e efeitos. A fonte pública 1.1.1 é apenas referência adjacente, não dados de produção da 1.0.10.

## Diferenças que impedem perks inseguras

`SugarStaffItem.use` solicita escala `1+0.25×L`, gerando larguras totais **4/5/6** para L=0/I/II. `SugarStaffHexEntity.getDimensions` aplica largura `4×scale` e altura `0.25`, atualizando dimensões quando o dado sincronizado muda. `hurtEntities` usa a AABB efetiva **e** um teste independente `distanceTo(hex)<=4`. Logo, aumentar largura não certifica aumento correspondente da distância máxima, área circular ou número de hits.

O renderer SHA-exato consulta `getHexScale` (`render @75`) e aplica `PoseStack.mulPose @108` e `PoseStack.scale @119`; isso demonstra **apresentação visual** e não autoriza alteração de targeting. Dano solicitado segue 1F ordinário / 6F nos últimos ticks; duração permanece `100+60×SPELL_LASTING`, cooldown do item 100 ticks. `HEX_SCALE` não consta das três chaves NBT de persistência `DespawnsIn/Lifespan/Owner`, pendendo validação de save/restart e sincronização em gameplay real.

A identidade é única: nenhum cast, cost, callback de perk, dano adicional, chain de proc ou raiz semântica foi criado pelo Black Arcana. O item retém seu comportamento provider-native, e qualquer integração futura deve preservar authority server-side, deduplicação, PvP/claims e `WorldEffectPolicy`.

## Reprodução do selo

```sh
python3 docs/qa/alexscaves_1010_humungous_hex_probe_test.py -v
python3 docs/qa/alexscaves_1010_humungous_hex_probe.py \
  --jar /caminho/alexscaves-1.0.10.jar \
  --javap /caminho/jdk21/bin/javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-HUMUNGOUS-HEX-CONTRACT-1.0.10.json' \
  --output /tmp/humungous-evidence.json
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

**Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · `provider_universe_closed=false`. Não promover Stage ou homologação integral de perks por este selo.
