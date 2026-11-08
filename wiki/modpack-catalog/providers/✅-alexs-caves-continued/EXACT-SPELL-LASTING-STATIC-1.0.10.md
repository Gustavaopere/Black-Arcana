# Spell Lasting 1.0.10 — prova técnica estática da duração da Hex

**Objeto:** `alexscaves:spell_lasting`, modificador nativo da ação `Sugar Staff Hex Cast`. **Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Mutação:** `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

## Identidade física e recursos

- `alexscaves-1.0.10-neoforge+1.21.1.jar` · **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- `data/alexscaves/enchantment/spell_lasting.json` · **365 bytes** · SHA-256 `839c95095540d2c40624575ad74aada2df482d7b4364d86fd8ebc238593a47dc`.
- `data/alexscaves/tags/item/enchantable/sugar_staff.json` · **51 bytes** · SHA-256 `eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc`.
- `en_us`: descrição do publisher declara +3 segundos de duração da Hex por nível; sem entrada própria `pt_br` no JAR auditado.
- Recurso: `weight=10`, `max_level=3`, `min_cost={base:1,per_level_above_first:8}`, `max_cost={base:41,per_level_above_first:10}`, `anvil_cost=1`, `slots=["mainhand"]`.
- Varredura byte a byte de **1.555 classfiles**: o símbolo direto `SPELL_LASTING` está em `ACEnchantmentRegistry.class` e `SugarStaffItem.class`. O censo de token não exclui reflexão, mods externos e código transformado.

## Evidências binárias individuais

| Método compilado SHA-exato | SHA-256 |
|---|---|
| `SugarStaffItem.use(Level,Player,InteractionHand)` | `76ba0a5bbf219e25f809c5e4d512fab3503f3e4dd99721e628787a7bde37d475` |
| `SugarStaffHexEntity.tick()V` | `7e74eb07baffa9564591754a76e56ec237eee0bbae08e84497cff3bedeeea9fa` |
| `SugarStaffHexEntity.getLifespan()I` | `2f6d0e3d2ab32b9eb34e3c5f39beac1690845a2885c89739b93f9155c02f7727` |
| `SugarStaffHexEntity.setLifespan(I)V` | `86ceb63b3ac2cd312739e0937c0a6034dc5bf04bcf9e589e06f2c24461e44578` |
| `SugarStaffHexEntity.hurtEntities(Z)V` | `83b41481b0f5fcd819c2ea7590bb244e16954e728ee734f2c22a34d7b7f73ee9` |
| `SugarStaffHexEntity.readAdditionalSaveData(CompoundTag)V` | `09c94be5b7344f66796c5bf14afc1a884974c844e081f1a2ee75d6f6131f1f50` |
| `SugarStaffHexEntity.addAdditionalSaveData(CompoundTag)V` | `eea7becd8a33a9d01920a0254f9ffb48563151b1f492fa98ec23cf1833e02d5f` |

No produtor, o ramo agachado/servidor contém `SPELL_LASTING @164`, leitura de nível `@167`, multiplicação inteira `@170`, adição `@171` e escrita `setLifespan @172`. Os operandos `bipush 100 @158` e `bipush 60 @160` dão **`L=100+60×level` ticks**, que resulta em **100,160,220,280** para níveis 0–III. O método já submeteu a Hex a `Level.addFreshEntity @124` e aplica cooldown independente de **100 ticks** `@178–180`; dano no item de **1** durabilidade por cast é solicitado `@464–468`. O ramo sem agachar usa `SpinningPeppermintEntity.setLifespan(80) @412`, **sem Spell Lasting**.

No consumidor, `tick @5–17` inicializa `despawnsIn` a partir de `getLifespan` quando vale -1; `@28–42` decrementa, `@48–49` descarta se já não positivo. `tick @285–299` solicita `hurtEntities(despawnsIn<5)`. Na Hex, o método de dano e seus guards continuam próprios da entidade. Os métodos NBT persistem `DespawnsIn`, `Lifespan` e UUID `Owner` condicional; `HEX_SCALE` não é serializado nessas rotinas. Sem teste físico não há garantia de owner/escala efetiva após reload.

A [ficha individual](enchantments/spell-lasting.md) detalha targeting, dano `1F/6F` do consumidor, cooldown/custo do item, condições do cast, owner e implicações de perks. O [manifesto individual](EXACT-SPELL-LASTING-STATIC-1.0.10.json) registra as classes/métodos completos como hashes e **somente pequenas janelas JVM**; 35 âncoras preexistentes de `SugarStaffItem.use`, 9 de `Hex.tick`, 11 de `Hex.hurtEntities` e 4 do leitor NBT foram contrastadas com o JAR 1.0.10.

## Reproduzir

```bash
python3 docs/qa/alexscaves_1010_spell_lasting_static_probe_test.py -v
python3 docs/qa/alexscaves_1010_spell_lasting_static_probe.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar --javap javap \
  --seal wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SPELL-LASTING-STATIC-1.0.10.json
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

A [CI dedicada](../../../../.github/workflows/alexscaves-1010-spell-lasting-static.yml) baixa o mesmo JAR apenas para inspeção com Java 21; compara SHA-1/SHA-256/tamanho, recurso/tag, hashes das classes, digest de métodos, âncoras binárias, manifesto selado e índices. **Não importa código de terceiros para o repositório.**

**Limites:** nenhuma mutação, integração de Mastery, validação física, datapacks carregados, aceitação de spawn, scheduler/ticks reais, PvP/claims/alianças, persistência após restart, resolução do owner e eventuais consumers de terceiros são homologados. `provider_universe_closed=false`.
