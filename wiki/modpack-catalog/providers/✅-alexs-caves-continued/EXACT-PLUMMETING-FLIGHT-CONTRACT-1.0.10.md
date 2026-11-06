# Plummeting Flight 1.0.10 — contrato estático SHA-exato

A [ficha](enchantments/plummeting-flight.md) documenta `alexscaves:plummeting_flight` na Extinction Spear arremessada e no transporte do espírito Subterranodon. Reutiliza o [manifesto Spirit Dinosaur](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json), já certificado no mesmo JAR publisher, sem recatalogar a lança, duplicar magia ou reproduzir código. O [selo individual](EXACT-PLUMMETING-FLIGHT-CONTRACT-1.0.10.json) fixa JSON, idiomas, SHA da ficha, classfiles e **373 âncoras** oriundas dos métodos compilados do manifesto pré-existente.

**Fonte:** Alex's Caves Continued 1.0.10, CurseForge projeto 1645389, arquivo 8856293; JAR 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Recurso `plummeting_flight.json`: 374 bytes, SHA-256 `163b032e37c716f0ef172a37b739a6d61340dab7c629c070698f8543999ec830`, max_level III, weight2, anvil4, mainhand, custos mínimos I/II/III 1/14/27 e máximos 41/51/61. A fonte pública 1.1.1 não é autoridade para os parâmetros do JAR 1.0.10.

**Causalidade:** `ExtinctionSpearEntity.onHitEntity` solicita dano 10F+damageBonus para LivingEntity, usa `causeSpiritDinosaurDamage`, e depois de `hurt=true` (exceto retorno Enderman) e owner não nulo cria Subterranodon. O encantamento é lido da stack da lança e copiado a `SynchedEntityData.ENCHANTMENT_LEVEL`. `DinosaurSpiritEntity.tickSubterranodon` soma `0.03 + 0.005×L` ao movimento vertical do espírito e continua o transporte somente enquanto o target ID existe e `duration < 40+5L`. Reposiciona o alvo com `setPos` e zera seu delta. Não cria novo dano, não comprova altura final nem spawn aceito.

**Fronteiras:** o tick movimenta com delta anterior e faz damping ~0.9 antes de executar o subtipo. Owner Player e entidade-alvo têm resoluções próprias; NBT registra `UsingPlayerUUID`/`DinosaurType`, mas não o nível sincronizado, target ID, contador de duração ou fading. Save/reload, side, física, claims/PvP, choque com blocos e distância final permanecem pendentes. Hooks mutadores são fail-closed.

Validação:
```sh
python3 docs/qa/alexscaves_1010_plummeting_flight_cards_test.py -v
python3 docs/qa/alexscaves_1010_plummeting_flight_probe.py \
  --jar /caminho/alexscaves-1.0.10.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json' \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-PLUMMETING-FLIGHT-CONTRACT-1.0.10.json' \
  --output /tmp/plummeting-evidence.json
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile spirit_dinosaur \
  --jar /caminho/alexscaves-1.0.10.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk21/bin/javap
```

**Contrato:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, provider integral aberto. Nenhuma implementação Java, Stage, mundo físico ou perk executável homologada.
