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
