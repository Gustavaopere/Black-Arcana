# Peppermint Punting 1.0.10 — contrato estático SHA-exato reutilizado

A [ficha](enchantments/peppermint-punting.md) encerra, no escopo **estático individual**, a seleção `alexscaves:peppermint_punting` pelo `SugarStaffItem.use` e os consumidores de `SpinningPeppermintEntity`. O corpo do consumidor já foi auditado e selado no contrato de [Multiple Mint](EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json): mesmas classes, métodos e SHA do JAR. A [prova compacta individual](EXACT-PEPPERMINT-PUNTING-CONTRACT-1.0.10.json) fixa os campos exatos do JSON Punting, SHA da ficha, classes e pivôs já presentes naquele manifesto. **Não se copia nem se redistribui implementação do provider.**

Autoridade do publisher: Alex's Caves Continued **1.0.10**, CurseForge projeto `1645389`, arquivo `8856293`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O JSON `data/alexscaves/enchantment/peppermint_punting.json` tem **370 bytes**, SHA-256 `ebe5a66b3d69d1d4384149959893712a7458ed9acfcc9064fa58fd16e8ba412b`, `weight=2`, `max_level=1`, `anvil_cost=4`, somente `mainhand`, custos `1/41` no nível I. Descrição original de idioma vinculada ao recurso.

O nível positivo seleciona `setStraight(true)`, yaw `180+headYaw+(i−1)×15`, speed inicial `8F` e cooldown `20`; zero seleciona órbita, yaw `180+(i−1)×30`, speed `12F` e cooldown `80`. Esses valores não alteram quantidade `3+MULTIPLE_MINT`, nem os `80` ticks de lifespan, fonte de dano `mobProjectile`, dano solicitado `3F` ou desgaste `1`. Seekcandy com alvo pode substituir speed por `50F` e cooldown por `50`; o tick escreve speed `7F` e radius `3F` antes da movimentação. O branch reto usa deltas, gravidade e colisão; portanto os valores iniciais **não** são distância ou velocidade efetiva homologadas.

O [probe read-only](../../../../docs/qa/alexscaves_1010_peppermint_punting_probe.py) baixa e verifica o JAR SHA-exato, extrai somente o JSON/tag/descrição, compara hashes de classes e as âncoras do manifesto Multiple Mint; o [teste individual](../../../../docs/qa/alexscaves_1010_peppermint_punting_cards_test.py) confere o selo, os ramos causais, o ledger e o crosswalk. O workflow `Alex's Caves 1.0.10 Peppermint Punting exact resource` executa essa evidência contra o publisher. O workflow consolidado `Alex's Caves 1.0.10 exact static contracts` reexecuta o consumidor pai e regressões individuais. Fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara 1.1.1 e é **corroboração apenas**, sem substituir os bytes 1.0.10.

```sh
python3 docs/qa/alexscaves_1010_peppermint_punting_cards_test.py -v
python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile multiple_mint \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap /caminho/jdk-21/bin/javap
python3 docs/qa/alexscaves_1010_peppermint_punting_probe.py \
  --jar /caminho/alexscaves-1.0.10.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json' \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-PEPPERMINT-PUNTING-CONTRACT-1.0.10.json' \
  --output /tmp/punting-evidence.json
```

**Limites:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Não promove Stages, outros encantamentos, renderer, world claims ou homologação integral de perks.
