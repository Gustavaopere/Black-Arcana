# NeoForge 21.1.248 / 21.1.250 — comparação distribuída

Status: evidência estática auxiliar, **NO_MUTATION**. Não é certificado de objeto, de equivalência transitiva nem de runtime transformado.

O build sibling fixa 21.1.248; o ledger físico #001 declara 21.1.250. O probe materializa as distribuições oficiais pelo instalador e compara bytes, sem executar magia ou instalar no pack.

## Evidência observada

Run [45464793964](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45464793964), job 138696694051, artifact 14954887050: schema 2, 51957 bytes, SHA-256 `53d4b7d17a9be60788be0f42d09754f0daf96ccce16ef2cd176f24bfa2661a7c`.

- Server overlay: ambos 5675624 bytes, SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`.
- SRG: ambos 14246609 bytes, SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`.
- Universal 248: 3551268 bytes, `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`.
- Universal 250: 3551255 bytes, `1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956`.
- 59/59 owners selecionados idênticos (estado, combate, mineração, explosão/tickets e SavedData).
- Universal direto: 1491 classes iguais, uma diferente, nenhuma exclusiva. Classe diferente: `net/neoforged/neoforge/common/data/SoundDefinition$SoundType.class`.
- Recursos: 788 iguais, três alterados (manifest, jarjar metadata e mods.toml), um exclusivo de cada versão: o CoreMods JAR interno.
- CoreMods interno 248: `f3cb872880f7dd7923d50f77bd9cf120291f3370fc89fd6a0f865f1e30d60517`; 250: `eee41553202c153f025a2461de319a17641246d037a848f96e50bcaec48021e6`.

## Expansão schema 3

[Run 45465724666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45465724666), job 138699973280, artifact 14954773360: schema 3, 55211 bytes, SHA-256 `12aea5ab66f309459d69d7c2609f0a28b0efa54f2771b7f120e670a98f9d2809`. Os sete classfiles e três recursos internos dos CoreMods têm hashes individuais idênticos entre versões; nenhum membro novo, removido ou alterado. Isso demonstra identidade dos membros, não igualdade do contêiner ZIP ou do processo de carregamento. O relatório fixa 59/59 classes selecionadas e o censo universal, e o workflow exige reprodução exata do selo schema 3. Igualdade de classfiles distribuídos não comprova igualdade dos bytes carregados após transformação, mixins e demais providers.

QA física NOT_TESTED; hooks NOT_VERIFIED; roots delta 0; universo aberto.
