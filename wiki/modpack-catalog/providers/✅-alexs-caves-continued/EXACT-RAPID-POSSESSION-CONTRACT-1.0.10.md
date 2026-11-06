# Rapid Possession — selo SHA-exato do movimento do Totem (1.0.10)

Este contrato **individual de encantamento** reutiliza o [manifesto das oito ações](EXACT-TECHNICAL-CONTRACTS-1.0.10.json) e a [ficha Totem of Possession](actions/totem-possession-remote-control.md). A [ficha Rapid Possession](enchantments/rapid-possession.md) delimita somente o novo objeto de catálogo, não cria cast/ritual, não duplica o Totem e não implanta um mutador.

**Publisher:** Alex's Caves Continued 1.0.10, CurseForge projeto 1645389 / arquivo 8856293; JAR 75.279.314 bytes SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. JSON `rapid_possession.json` 376 bytes SHA-256 `449eda001a6bb6507ef4e43cc18e601659d970e8bd7d43967aff32dfed07288a`.

**Dados:** níveis I–III, weight10, anvil1, slot mainhand, custo mínimo 1/6/11 e máximo 41/51/61; tag item `alexscaves:totem_of_possession`. O texto inglês publisher indica movimento acelerado de Mobs possuídos.

**Consumidor exato:** `TotemOfPossessionItem.onUseTick` @318–334 lê `RAPID_POSSESSION` via `ACCompat.enchantLevel` e calcula `F=1.25+0.35×L`. Para Mobs o provider solicita `navigation.moveTo(destination,ramp×F)`, enquanto a rota não-Mob usa `oldVelocity×0.8+direction×(0.15×F)`. O raio de comando `32×ramp` é separado e não cresce com L. Níveis 0/I/II/III produzem fatores **1.25/1.60/1.95/2.30**; uma perk não pode interpretar esses fatores como velocidade física, reach ou dano fixo. O [selo](EXACT-RAPID-POSSESSION-CONTRACT-1.0.10.json) compara 29 âncoras históricas SHA-exatas e 17 pivôs adicionais lidos do método compilado na mesma classe.

**Autoridade:** vínculo por UUID/tag/ID, gate de olhar/Sightless, alvo da visão, ataques na caixa inflada por3, transferência e detonação permanecem propriedade da ação nativa. `setDamageValue` client-only não certifica desgaste server-side; sincronização da stack não autoriza mutação de atributos. QA física, network authority, hooks, PvP/claims e mundo ainda estão pendentes.

Reprodução no mesmo JDK21:
```sh
python3 docs/qa/alexscaves_1010_rapid_possession_cards_test.py -v
python3 docs/qa/alexscaves_1010_rapid_possession_probe.py \
 --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
 --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TECHNICAL-CONTRACTS-1.0.10.json' \
 --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAPID-POSSESSION-CONTRACT-1.0.10.json' \
 --output /tmp/rapid-possession-1010.json
```

**Limite final:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, sem promotion de Stage ou runtime e sem universo do provider fechado.
