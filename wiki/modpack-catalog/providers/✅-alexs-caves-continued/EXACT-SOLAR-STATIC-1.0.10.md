# Solar 1.0.10 — reprodução do contrato binário estático

**Objeto:** `alexscaves:solar`. **Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY`. **Estado mutador:** `NOT_VERIFIED` / `NO_MUTATION`; **QA física:** `NOT_TESTED`. O método nativo é parte do Raygun, não uma nova raiz de casting.

## Identidade publisher física

- `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes.
- JAR SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- JAR SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Recurso `data/alexscaves/enchantment/solar.json`: 353 bytes, SHA-256 `6b89d32889d8da9adfad072c534ae76627b1c620d489951bf1095f1805809b80`.
- Tag `data/alexscaves/tags/item/enchantable/raygun.json`: 46 bytes, SHA-256 `8e7cb71ff2c706004fba0493f2237e96da3af53dea6e3ae414542b5150cc012d`.
- Censo simbólico: `SOLAR` em 2/1.555 classfiles: `ACEnchantmentRegistry` e `RaygunItem`; a ausência de token em outros consumidores não exclui reflexão ou código externo.

## Evidências de métodos

- `RaygunItem.acInventoryTick(ItemStack,Level,Entity,boolean)V`, 109 instruções, SHA-256 `7dd6613ef567ab79f0065253788e6ee9156bb86908b63907808599d5e3b560d2`. Guardas: servidor, nível positivo, stack não em uso, `ChargeUsed>0`, RNG `<0.02F`, `canSeeSky(entity.blockPosition().above())`, `isDay`, `!hasFixedTime`, `sunAboveHorizon`; efeito: `setCharge(D−1)` e `setUseTime(0)`.
- `RaygunItem.getCharge`: 11 instruções e SHA `c69c154524dbe4b4e46ed589438f7548cc39658305072a59b7c6a7dc9ec25baa`. Lê `ChargeUsed` com fallback 0.
- `RaygunItem.setCharge`: 11 instruções e SHA `cedf012dbfb8edf1ca2171c57001dc8937f2982e3755a156da058a74d260993e`. Solicita escrita `CompoundTag.putInt("ChargeUsed",D)`.
- `RaygunItem.hasCharge`: 8 instruções e SHA `0b89217b97ca4f3d1c155c01b4170d1f0cb9141e4ee854ccf0c72892cd3b1db7`. Limite do predicado: `D<1000`.
- `ACCompat.sunAboveHorizon(Level,BlockPos)Z`: 16 instruções e SHA `e56a191d33a1ab462518d5113e1df101c98663bafa1b263da092cf46a9767da7`; dois operandos binários independentes `0.259F` e `0.74F` (âncoras pré-certificadas), guardas de retorno booleano `1/0`. Testa `getTimeOfDay(1F)` fora do intervalo delimitado; não usa posição para o cálculo do horário.
- `ItemStackTickMixin.ac_inventoryTick`: 19 instruções e SHA `ceeb91a726e908df227666b823d9811552dc84032df23dcc1570add5a11698d6`; encaminha `acInventoryTick` quando o item implementa `ACTickingItem`.

## Como reproduzir

```bash
python3 docs/qa/alexscaves_1010_solar_static_probe_test.py -v
python3 docs/qa/alexscaves_1010_solar_static_probe.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap javap \
  --seal wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SOLAR-STATIC-1.0.10.json
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

A [CI dedicada](../../../../.github/workflows/alexscaves-1010-solar-static.yml) executa com Java 21 e baixa o publisher somente para auditoria; não armazena o JAR de terceiros no repositório. O manifesto [`EXACT-SOLAR-STATIC-1.0.10.json`](EXACT-SOLAR-STATIC-1.0.10.json) é o selo verificável de classes, métodos, recursos e limites. A [ficha individual](enchantments/solar.md) descreve todos os parâmetros e o limite de interoperabilidade.

**Não comprovado:** frequência física dos callbacks, eficácia/aceitação da recarga no multiplayer, estabilidade de carga sob pacotes cliente, save/reload, uso em inventário de outras entidades, configuração/datapacks efetivos, mutating hooks, GameTest específico de Solar ou funcionamento de perk. Uma execução CI da sonda **não** é QA física.
