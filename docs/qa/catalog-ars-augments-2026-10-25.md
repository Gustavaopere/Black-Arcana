# Ars Nouveau — certificação estática dos 13 augments, 25/10/2026

Continuação de Amplify na PR #897, base Black Arcana `43661700cd027bc2cf51eb09e9ed46ea9c551f4e`. Os checks pós-merge dessa base foram confirmados como SUCCESS: verify, stage05_qa_companion_smoke e provider_index_consistency. Os rascunhos concorrentes MFTE foram preservados em branch local separada, sem promovê-los a certificação.

## Entrega e escopo

As doze fichas restantes de augments receberam revisão dos sete campos exigidos pelo [critério de certificação](../../wiki/modpack-catalog/meta/PERK-READY-CERTIFICATION-RULES.md): identidade, comportamento, parâmetros, targeting, custos, integração e validação. Amplify recebeu uma precisão sobre a API pública já existente. O [contrato comum](../../wiki/modpack-catalog/providers/✅-ars-nouveau/AUGMENT-STATIC-CERTIFICATION-5.13.1.md) reúne as diferenças entre operador, flags, contagem da receita, consumidor e contrato de perk.

O manifesto passa de **1 para 13 certificados estáticos**, todos no Ars Nouveau: **13/13 augments**, **13/85 glyphs**, **13/138 fichas Ars detectadas** e **13/2075 fichas candidatas globais**. **0/164 providers** têm universo integral certificado. Não foram criadas identidades, fichas candidatas ou certificações de outros providers. A contagem de fichas observadas não fecha o universo físico da modlist.

Cada entrada mantém `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`. O ✅ cobre a classificação documentada dos campos estáticos, incluindo os não aplicáveis e as integrações bloqueadas/condicionadas. Não aprova um perk executável.

## Proveniência e prova binária

Source oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, versão declarada 5.13.1/MC1.21.1/NeoForge21.1.228; pack NeoForge21.1.250. A licença do source inclui LGPLv3 e reserva assets; foram usados fatos, paráfrases e referências, sem copiar implementação ou arte upstream.

Publisher Modrinth **qEFs5RRw**, arquivo `ars_nouveau-1.21.1-5.13.1.jar`: **20107711 bytes**, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, SHA-256 `99dff85e8778f7ae21dfd51cdedadf20f555a834fc757c0afe5f03c10eea96f2`, medidos nesta sessão e comparados aos metadados oficiais. Coincide com o fingerprint histórico físico #047; o perfil instalado original não está disponível nesta sessão para nova medição.

O gate existente `ars_5131_exact_ids_binary_audit.py` foi executado localmente com Java21 e o JAR publicado, confirmando novamente **85 glyphs +24 rituais**, incluindo os13 augments, seus IDs e classes. Resultado `SHA_MATCHED_COMPILED_109_RESOURCELOCATION_CLASS_IDS_NOT_RUNTIME`, +0 raízes. Essa prova fecha identidade estática, sem equiparar todos os métodos/consumidores do JAR ao source ou provar configuração/gameplay instalados.

## Precisões relevantes para perks

- `SpellModifierEvent` existe e expõe builder mutável após augments/itens e antes do consumidor. Isso é uma superfície real; adapter RPG/Black Arcana, clamps, equivalência de custos e deduplicação permanecem não verificados. Reatribuir o campo builder não substitui o objeto original retornado pelo caminho auditado.
- Stats, flags e contagem/receita são entradas diferentes. Split usa stats em certos consumidores; Pierce do projétil lê a receita original. Mutação de uma lista não recalcula automaticamente multiplicadores já construídos.
- Aceleração tem fórmula/piso no caminho normal de Projectile; seu overload de bloco usa outra emissão. Duração depende do receptor e presença de Extend/Reduce pode mudar Harm para Poison mesmo com modificador numérico líquido zero.
- AOE não é raio universal. Dampen tem consumo numérico e por contagem em Explosion. Caps por glyph e sua validação dependem do contexto de montagem/cast e de flags de configuração.
- Extract/Fortune têm incompatibilidade declarada, sem veto programático default comprovado no recorte. Randomize possui vários consumidores de RNG. Sensitive distingue flag/contagem, pick de blocos e consulta separada de entidades; não concede um bypass genérico de targeting ou proteção.

## Validação

- Revisões independentes dos três grupos de quatro fichas concluídas. Common e precisão em Amplify revisados; a correção de alcance em Sensitive foi reavaliada contra o source fixo.
- Nas 13 fichas e no contrato comum: **209 referências pinadas**, **55 arquivos source distintos**, **89 links locais** e **14 tabelas**, com IDs, arquivos e limites de linhas conferidos. Referências não são 209 hooks únicos.
- Nos **20 Markdown** alterados, incluindo este relatório e os índices: **509 links locais** e **23 tabelas** conferidos; sem referências indefinidas ou colunas inconsistentes. `git diff --check` limpo.
- **133 testes existentes PASS**: 20 de integridade dos índices, 3 do gerador, 12 de registro estático Ars, 15 de IDs compilados Ars, 52 do catálogo global, 5 do ledger físico e 26 do tracker de pendências.
- Verificação dos **509 índices** PASS: 164 providers,2075 fichas candidatas,13 certificadas,0 providers integrais e0 problemas. Modo de verificação do gerador também PASS.
- Manifesto preserva os registros de rosters e o dicionário de providers; novos certificados possuem sete evidências locais existentes com justificativa por campo. Gerador mantém2075 candidatas e164 providers.

Nenhum Java/runtime, adapter, dependência, lockfile, limite do provider ou Stage foi alterado. Configuração implantada, permissões/claims, aprendizagem e custos reais, fluxo completo de composição, cliente, multiplayer, persistência e QA físico continuam pendentes. Resultados de PR/CI/merge devem ser registrados somente após execução real.
