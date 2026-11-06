# Precise Volley — contrato estático SHA-exato do Dreadbow 1.0.10

A [ficha](enchantments/precise-volley.md) cobre `alexscaves:precise_volley` (nível máximo I) na chuva de flechas do Dreadbow. O [selo individual](EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.json) fixa o SHA da ficha, JSON, idioma, tag, hashes dos classfiles e **234 pivôs JVM delimitados**, reutilizando o [manifesto Dreadbow/Dark Arrow](EXACT-DREADBOW-CONTRACTS-1.0.10.json) já auditado. Nenhum código do provider foi incorporado ao Black Arcana.

Publisher: Alex's Caves Continued **1.0.10**, CurseForge projeto `1645389`, arquivo `8856293`; JAR **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. JSON `precise_volley.json` de **363 bytes**, SHA-256 `59efc44222dcd59530e13a50cb413a2db0c875213ced1a2ac9de2ef982615f53`. Parâmetros: `max_level=1`, `weight=2`, `anvil_cost=4`, `mainhand`, custo mínimo **1** e máximo **41** no nível I. Descrição inglesa: flechas do Dreadbow caem mais perto da região central.

Em `DreadbowItem.releaseUsing`, o predicado `level(PRECISE_VOLLEY)>0` seleciona `inaccuracy=0F` para a chamada `shoot`. Na Dark Arrow conversível, seleciona `setShadowArrowDamage(2F)` em vez de `3F`. `DarkArrowEntity.onHitEntity` pode dobrar o dano solicitado se `isPerfectShot`: **2/4F** com Precise em vez de **3/6F** sem ele, sempre sujeito ao retorno de `ACCompat.hurt`, filtros de owner/aliados e fading. Em projéteis não convertíveis Precise não escreve shadow damage.

As consultas `128F×p` e fallback `42F×p`, o spawn com jitter 16×4×16, velocidade `0.5F+1.5F×r`, contagens `ceil(30F×p)` / `ceil(8F×p)` e os custos por salva não mudam pelo nível de Precise. `Relentless Darkness>0` desvia `releaseUsing`; `onUseTick` não consulta Precise e pode usar `2F` por outro caminho. O registro do encantamento na tag e outros dados de exclusão não substituem um teste físico de compatibilidade.

Validação:
```sh
python3 docs/qa/alexscaves_1010_precise_volley_cards_test.py -v
python3 docs/qa/alexscaves_1010_precise_volley_probe.py \
 --jar /caminho/alexscaves-1.0.10.jar \
 --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DREADBOW-CONTRACTS-1.0.10.json' \
 --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.json' \
 --output /tmp/precise-evidence.json
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
 --profile dreadbow \
 --jar /caminho/alexscaves-1.0.10.jar \
 --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DREADBOW-CONTRACTS-1.0.10.json' \
 --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
 --javap /caminho/jdk21/bin/javap
```

**Limites:** `STATIC_TECHNICAL_CATALOG_ONLY`, `SHA_EXACT_BINARY_BEHAVIOR`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Nenhuma QA física, Stage, alteração de runtime, homologação de modpack multiplayer ou fechamento integral do provider.
