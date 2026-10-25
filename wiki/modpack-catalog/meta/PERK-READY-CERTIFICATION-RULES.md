# Certificação técnica 100% para perks — regras de auditoria

Esta auditoria é **mais estrita** do que os diretórios legados com prefixo ✅: os nomes antigos significam apenas que um inventário foi criado.

Um ✅ individual exige prova verificável nos campos: identidade e versão exata, comportamento executado e recebedor, parâmetros/fórmulas/limites, targeting e tipos de dano/efeito quando aplicáveis, custos/cooldowns, limites de autoridade/contratos de perks, e validação/testes compatíveis com a alegação. O manifesto guarda o caminho exato da evidência de cada campo. Um campo não aplicável precisa ter prova de não aplicabilidade e nunca deve ser inventado.

Um provider só recebe ✅ 100% quando:
1. Seu universo catalogável está fechado por fonte verificável atual (todas as famílias mágicas, skills, atributos e sistemas pertinentes);
2. Todos os objetos foram individualizados (ou exceção semântica justificada) e marcados 100% conforme o manifesto;
3. A prova do universo fechado, identidade de versões e quaisquer condicionamentos estão documentados;
4. A definição do escopo permite revisão independente.

Os índices são snapshots gerados a partir de arquivos Markdown identificáveis por nome; heurística de nomes não descobre conteúdo existente apenas em registries, JSONs, composites ou JARs. Portanto os denominadores de fichas são **recortes observados**; não são o denominador universal. Ausência de ficha produz ⚠️, não ❌.

Atualize o manifesto e regenere os índices ao concluir cada objeto/provider; revisões de PR e CI devem impedir ✅ sem evidências, contagens negativas, itens duplicados ou resultados desatualizados.

A pasta `wiki/modpack-catalog/providers/INDEX.md` é o painel global; cada mod e cada subpasta possui seu próprio `INDEX.md`. Nenhuma mudança nesta organização modifica runtime de Black Arcana, RPG Skill Tree, Enshrouded ou os providers externos.


## Atualização contínua

Quando houver fichas novas, exclusões, subpastas novas ou evidência suficiente para promover uma ficha, atualizar a fonte e o manifesto e executar:

    python3 scripts/catalog/generate_perk_ready_indexes.py
    python3 scripts/catalog/check_perk_ready_indexes.py
    python3 scripts/catalog/generate_perk_ready_indexes.py --check

O workflow "Perk-ready provider index coverage" verifica os índices em PRs que alteram providers, o manifesto, o gerador ou seus testes. Se um objeto novo não aparecer ou se o numerador estiver stale, o CI rejeita o snapshot.

O verificador **não infere** a completude do prefixo antigo da pasta, nem permite ✅ de objeto sem identidade, comportamento, parâmetros, targeting, custos, integração e validação explicitamente documentados. Mesmo uma pasta com todas as fichas concluídas não recebe ✅ de provider até haver fechamento fundamentado do universo de objetos; rosters pontuais de spells não bastam para fechar perks e sistemas de outros tipos.

## Primeiro certificado do recorte estático — Ars Nouveau / Amplify

O índice técnico de fichas pode atribuir ✅ **apenas ao contrato estático documentado** quando houver: identidade do JAR SHA-exato, revisão de source em commit imutável (ou análise binária equivalente), comportamento causal do objeto, custos e parâmetros, aplicação ou não aplicabilidade de targeting e projétil/duração, fronteira de mutabilidade provider-native e limites de validação explícitos.

**Exemplo concreto:** `ars_nouveau:glyph_amplify` ([ficha](../providers/✅-ars-nouveau/glyphs/augments/amplify.md)) apresenta os sete campos, além de `NOT_VERIFIED` para hook mutador e `NOT_TESTED` para QA físico. O ✅ é **100% da documentação estática do componente**, jamais execução de perk, integração aprovada, config de jogador ou teste real. O provider Ars permanece ⚠️ porque as outras fichas e o fechamento das famílias catalogáveis ainda não estão certificados.

O manifesto de cada ✅ exige `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `version`, `artifact_sha1`, `evidence_grade` (source-pinned + identidade binária SHA-exata ou comportamento binário SHA-exato), `mutating_hook`, `physical_qa` e referências locais **existentes** com justificativas por campo; os links externos de fonte são descritos na ficha, mas não são tratados como arquivos locais comprovados apenas por terem uma URL.

**Distinção de percentuais:** o quadro geral mantém dois denominadores independentes: `mods com universo técnico integral fechado / pastas de providers` e `fichas estáticas certificadas / fichas individuais detectadas`. Nenhum dos dois é o total físico universal de tudo que a modlist contém. Um ✅ de ficha não implica ✅ do mod.
