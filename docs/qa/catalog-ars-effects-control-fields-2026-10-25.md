# Ars Nouveau — quinze Effects: dano, tempo e propagação, 25/10/2026

Base reconciliada com o trabalho de outro chat: `Black-Arcana/main@094c9dc7ec954e26b5b41f5baef917274dfedbb8`, PR #903. Foram conferidos o merge e os três checks pós-merge dessa base: `verify`, `stage05_qa_companion_smoke` e `provider_index_consistency`, todos SUCCESS. Este lote continua os Effects restantes e preserva os trabalhos de outros providers em branches separadas.

## Entrega e contadores

Quinze fichas existentes foram auditadas: Cold Snap, Flare, Wind Shear, Wind Burst, Fangs, Firework, Gravity, Rune, Delay, Reset, Rewind, Linger, Wall, Burst e Orbit. O [contrato comum](../../wiki/modpack-catalog/providers/✅-ars-nouveau/EFFECT-STATIC-CONTROL-FIELDS-FIFTEEN-5.13.1.md) registra a proveniência e as superfícies compartilhadas. As fichas ligam parâmetros, fórmulas e limites a callbacks e consumidores downstream, incluindo casos em que descrição, config declarada e execução diferem.

O manifesto passa de **38 para 53 contratos estáticos**; preserva as 38 entradas anteriores, os registros de rosters e o dicionário de providers. Contadores: **35/67 Effects**, **53/85 glyphs**, **53/138 fichas Ars**, **53/2075 fichas candidatas globais**, **0/164 providers integralmente certificados**. Augments permanecem13/13 e Forms5/5. Não foram acrescentadas identidades ou fichas candidatas. As barras geral e por provider/subpasta continuam nos [índices gerados](../../wiki/modpack-catalog/providers/INDEX.md); o universo integral da modlist continua aberto.

Todos os novos registros têm sete evidências locais por campo e mantêm `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, **`mutating_hook=NOT_VERIFIED`** e **`physical_qa=NOT_TESTED`**. O teste existente de contadores foi atualizado para os novos totais; nenhum teste novo foi criado para espelhar texto das fichas.

## Proveniência e auditoria binária

Source oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release5.13.1. Publisher Modrinth **qEFs5RRw**, `ars_nouveau-1.21.1-5.13.1.jar`: **20107711 bytes**, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, SHA-256 `99dff85e8778f7ae21dfd51cdedadf20f555a834fc757c0afe5f03c10eea96f2`. Somente fatos, paráfrases e referências upstream foram incorporados; não houve cópia de implementação ou assets.

Foi executada novamente a auditoria existente `docs/qa/ars_5131_exact_ids_binary_audit.py` com Java21 e o publisher JAR SHA-exato. Resultado **PASS**, `SHA_MATCHED_COMPILED_109_RESOURCELOCATION_CLASS_IDS_NOT_RUNTIME`: **85 glyphs +24 rituais**, +0 raízes semânticas. Os15 IDs/classes deste lote constam nesse resultado. A prova não equipara integralmente os corpos Java aos métodos compilados, não carrega o registry no jogo e não mede novamente o perfil físico original ausente.

## Achados relevantes para perks

- Cold Snap/Flare: dano inicial, entidades secundárias e estados são etapas distintas; cancelamento de dano não desfaz automaticamente os próximos passos. Shards, Cinders, Mage Fire e Blast possuem consumidores próprios, sem um único pipeline de dano universal.
- Wind Shear: o loop pode contar11 posições, apesar de a descrição mencionar10; `airDamage` é configurado, mas não consumido pela fórmula inspecionada. Wind Burst usa `TRIGGER`, troca a entidade-fonte com Sensitive e não emite o WindCharge auxiliar como projétil.
- Fangs/Firework: warmup, lifetime e dano são eixos diferentes. O consumidor das presas chama `hurt` diretamente; foguete de inventário e fallback sintetizado interpretam augments de forma distinta. Ownership após reload e consumo de item não foram inferidos a partir do nome de um método de busca.
- Gravity/Rune: presença de Extend seleciona um ramo de status; o amplifier não é uma escala universal do consumidor. Rune tem trigger, seleção e autoridade de custo específicos; Runic Chalk fornece um caminho de conversão para permanente.
- Delay/Reset/Rewind: contagens, scalar, fila e segmentação de contexto são operações diferentes. Duração não positiva tem comportamento próprio; Reset só libera limites de um conjunto explícito; Rewind usa histórico limitado e `setHealth`. Valores declarados1/5 no override de configuração não provam caps efetivos.
- Linger/Wall/Burst/Orbit: frequência, quantização, contagem e budget variam por ramo. Linger/Wall podem processar seis alvos numa passagem e exceder o budget100 até105; Sensitive segue outra rotina. Wall tem histórico de hits irregular. Orbit usa fase em radianos e divisor sem clamp local. Teto local não equivale a limite da composição inteira.
- APIs: `SpellModifierEvent` expõe o builder original; `EffectResolveEvent.Pre` permite veto, mas reatribuir campos não troca os locais usados pelo resolver. `Post` também pode ocorrer sem aplicação efetiva. Retomadas, campos e contextos filhos não comprovam um novo cast pago ou crédito de Mastery.

## Validação realizada

- Revisão independente dos quatro grupos de fichas, do documento comum e da ressalva de caps de Rewind: **PASS**. Duas precisões em Firework/Fangs foram corrigidas e reavaliadas.
- Nas15 fichas e no documento comum: **272 referências source pinadas**, sendo **263 com limites de linhas**, **66 arquivos upstream distintos**, **66 links locais** e **16 tabelas**; arquivos, revisão, limites, labels e colunas válidos. Referências repetidas não são hooks distintos.
- **146 testes existentes PASS**:20 de integridade de índices,3 do gerador,13 de contratos Ars Effects,12 do registro estático Ars,15 dos IDs compilados Ars,52 do catálogo global,5 do ledger físico e26 do tracker de pendências.
- Auditoria dos **509 índices PASS**:164 providers,2075 fichas candidatas,53 certificadas,0 providers integrais e0 problemas. A ordem incidental de três índices Goety reescritos pelo gerador foi preservada como na base; não há mudança desse provider.
- `generate_perk_ready_indexes.py --check`: **PASS**,509 índices,2075 candidatas,0 erros. Nos **22 Markdown** alterados: **544 links locais** e **25 tabelas**, sem referência indefinida, arquivo ausente ou coluna inconsistente. `git diff --check`: limpo.

Nenhum Java/runtime, adapter, dependência, lockfile, limite executável ou Stage foi alterado. Custos e configurações instalados, integração RPG Skill Tree/Black Arcana, claims/PvP, cliente/servidor, multiplayer, persistência física e QA em modpack permanecem pendentes. CI e merge são relatados somente depois da execução real; não são QA de gameplay.
