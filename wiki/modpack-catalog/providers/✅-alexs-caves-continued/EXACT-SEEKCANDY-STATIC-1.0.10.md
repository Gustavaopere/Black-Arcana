# Seekcandy — certificado técnico estático individual / publisher Alex's Caves 1.0.10

**Scope:** `STATIC_TECHNICAL_CATALOG_ONLY` · **Evidence:** `SHA_EXACT_BINARY_BEHAVIOR` · **Mutation:** `NO_MUTATION` · **Hook:** `NOT_VERIFIED` · **Physical QA:** `NOT_TESTED`. A [ficha completa](enchantments/seekcandy.md) é a especificação funcional; este arquivo registra a reprodução e os limites da evidência. O contrato NÃO autoriza integração mutadora.

## Fonte física

Modlist do `Gustavaopere/neoforge-rpg-skilltree` → `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1 / NeoForge / Java 21). Tamanho **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. JSON `data/alexscaves/enchantment/seekcandy.json`: 361 bytes, SHA-256 `7e564925928b90368d9042f1b722f89464bfbd708abf69ced0d785b5871f0a74`.

O [manifesto exato individual](EXACT-SEEKCANDY-STATIC-1.0.10.json) contém:
- censo por bytes dos **1.555 classfiles do provider**, com referências binárias diretas `SEEKCANDY` exclusivamente no registro e em `SugarStaffItem`;
- cinco classfiles SHA-256 selecionados e os métodos compilados relevantes, todos com hashes de corpo JVM e descritores validados;
- todas as âncoras de método previamente validadas pelo [manifesto de Multiple Mint](EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json) no JAR exato;
- pivôs de fluxo para ativação, aquisição, estado sincronizado, movimentação, filtros, dano, knockback, descarte, cooldown, desgaste e persistência;
- resource JSON, `#alexscaves:enchantable/sugar_staff` e locale publisher `en_us` com hashes verificados.

## Assinaturas e decisões verificadas

| Ponto | Prova / consequência |
|---|---|
| `SugarStaffItem.use` | 226 instruções (digest `76ba0a5bbf219e25f809c5e4d512fab3503f3e4dd99721e628787a7bde37d475`), guarda de servidor, captura target via `getClosestLookingAtEntityFor(...,32D)`, separação Shift→Hex e normal→Peppermint |
| Guarda Seekcandy | @342–355: target não nulo e `ACCompat.enchantLevel(stack,SEEKCANDY)>0` |
| Pedidos no ramo | @358–377: `setSeekingEntityId(target.getId())`, `setSpinSpeed(50F)`, seleção de cooldown `50` |
| Número e custo | `N=3+level(MULTIPLE_MINT)` tentativas, `Level.addFreshEntity` com boolean descartado, único `addCooldown` ao final e `hurtAndBreakUsedHand(stack,1,...)`; sem novo cast/segunda cobrança |
| `SeaStaffItem.getClosestLookingAtEntityFor` | 119 instruções (digest `9c5f594f399ca3ace5b9d65ad5f4db7f53ddd5e01d1c4654bd951bdaf1a04306`), alvo `Mob` com filtros player/alianças/linha de visão, ordenação quadrática por posição do clip; `32D` é argumento do seletor, não alcance de voo |
| `SpinningPeppermintEntity.tick` | 373 instruções (digest `acf4390aed5a2b3f26af31e982ccabec5a0d245d8bea5c594344e4d299f21937`), speed `7F` e radius `3F` sobrescritos em cada tick, resolução `Level.getEntity(seekingId)`, centro orbital atualizado, raio convergindo com `4-4min(1,tickCount/30)` |
| Straight vs orbit | `isStraight` escolhe caminho com yaw/delta em vez do steering orbital; combinação de Seekcandy e Peppermint Punting não está homologada como homing eficaz |
| `hurtEntities` | 90 instruções (digest `f7580b92bc9585191e0b831f5aeb332e4a94ad95cfc173a74a157d543858dbfc`), fonte `mobProjectile`, filtros de owner/friendly-fire, `ACCompat.hurt(...,3F)`, knockback solicitado somente se hit aceito, discard se algum hit aceito e seeking ID positivo/diferente de -1 |
| Owner e NBT | UUID do owner salvo e recuperável lazy, mas hurt usa campo owner; `SeekingEntityId` em `SynchedEntityData` default -1 **não é persistido nos overrides próprios de NBT**; leitura de `AroundY` usa `AroundZ` no bytecode 1.0.10 |

A saída do probe comprova apenas **os campos, condições, fórmulas e chamadas selecionados do provedor**, não a aceitação do spawn, os resultados de colisão, o retorno de dano em todas as situações, nem segurança de mutação ou comportamento sob configurações externas.

## Reprodução

```bash
python3 docs/qa/alexscaves_1010_seekcandy_static_probe.py \
  --jar '/caminho/alexscaves-1.0.10-neoforge+1.21.1.jar' --javap javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SEEKCANDY-STATIC-1.0.10.json'
python3 docs/qa/alexscaves_1010_seekcandy_static_probe_test.py -v
python3 docs/qa/alexscaves_1010_seekcandy_cards_test.py -v
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

O workflow `.github/workflows/alexscaves-1010-seekcandy-static.yml` baixa o JAR físico exato, executa testes fail-closed, verifica todos os pontos do manifesto `--seal`, o catálogo semântico e os índices; a CI principal do Black Arcana mantém os gates de build e servidor. **Não** interpretar esses testes estáticos como QA física do modpack instalado, prova de APIs mutadoras ou autorização para mover Stage. Em modpack real, testar PvP, claims, alvos que desapareceram, reuso de IDs, descarte, reload, knockback, compatibilidade com Punting, troca de mundo e atribuição de Mastery/XP antes de qualquer implementação.
