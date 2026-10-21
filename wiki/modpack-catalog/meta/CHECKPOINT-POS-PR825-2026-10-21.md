# Black Arcana — checkpoint do catálogo pós-PR #825 (21/10/2026)

## Escopo e autoridade
- **Base congelada:** `Black-Arcana/main@1cded69beef79f860454ecd2ace2de611e248168`; entrega da [PR #825](https://github.com/Gustavaopere/Black-Arcana/pull/825), squash em `1cded69beef79f860454ecd2ace2de611e248168`. Modlist sibling consultada em `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.
- **Modlist:** árvore da pasta `PROJECT-INSTRUCTIONS/modlist/` contém **591 arquivos Markdown** no SHA sibling. Isto é uma contagem de fichas da modlist, **não** o denominador de mods mágicos ou de objetos mágicos.
- **Método:** evidência GitHub/Java 21/compilada ou source-pinned é distinta de comportamento em cliente/Survival. Clean-room: hashes, caminhos, símbolos, descritores e observações; não copiar bytecode, fontes/asset de terceiros em nosso runtime.

## Progresso sem inflação

| Eixo | Numerador / denominador | Estado e fronteira |
|---|---|---|
| Universo global de objetos mágicos | **—%** (denominador desconhecido) | ⚠️ **divergência a reconciliar**: [índice histórico de 13/10](CATALOGO-GLOBAL-MAGIAS.md) registra **≥1.857 global / ≥1.855 estritos**, mas [ledger semântico de 15/10](SEMANTIC-MAGIC-COVERAGE.md) registra **≥1.856 global / ≥1.854 estritos**. Não somar, não substituir silenciosamente, não inferir conclusão de cobertura. Revisão de deduplicação e proveniência permanece aberta. |
| Campanha binária de **39 providers selecionados** | **35/39 (89,74%)** certificações de identidades físicas; **4/39 (10,26%)** condicionados | ✅/⚠️ proveniente da 35ª prova no ledger semântico (Hazen N Stuff 1.4.0.14). Os 39 não são todos os mods da modlist nem a completude do conteúdo de cada provider. |
| Iron's Spells 3.16.3 — magia ativa | **110/110 (100%)** fichas de identidade e anotações técnicas source-pinned | ✅ [PR #795](https://github.com/Gustavaopere/Black-Arcana/pull/795), merged; nenhuma identidade nova por esse enriquecimento. |
| Iron's Spells 3.16.3 — auditoria causal individual | **110/110 (100%)** dossiês source-causal documentais | ✅ [PR #825](https://github.com/Gustavaopere/Black-Arcana/pull/825) merged com 390 caminhos (317 Markdown, 44 scripts de QA, 15 workflows, 11 arquivos de companion QA, 2 testes Java, 1 `build.gradle`). **Não** significa 110 spells testados fisicamente, hooks seguros ou perks ativas. `soulfire_ray` e `thunder_step` são classes com `registerSpell` comentado no pin e ficaram **EXCLUDED**; `cloud_of_regeneration` legacy/deprecated fora dos 110 ativos. |
| Ars Nouveau 5.13.1 | **85/85 glyph parts + 24/24 rituais = 109/109** IDs de registro compilados | ✅ binário exato para identidade; ⚠️ custos e gameplay/Survival/integração ainda não homologados. |
| Somake Spells 1.0.9 | **83/83** IDs registrados, recorte estático **8/83** (9,64%) | ✅ identidade, 🟡 aprofundamento. Blood Cut lifesteal `0.15f × LivingDamageEvent.Post.getNewDamage()` para `event.getSource().getEntity()` como `LivingEntity` é uma rota estática; dispatch real, HP recuperado e hooks continuam ⚠️/⛔. |
| Epic Fight 21.17.3.1 | **43/43** IDs core classificados; **3/43** atos sobrenaturais no escopo semântico | ✅ classificação; **40/43** ações não mágicas continuam úteis ao mapeamento de perks/stamina/combate; nenhum adapter Mastery/perks homologado automaticamente. |

## QA e runtime
- [PR #825](https://github.com/Gustavaopere/Black-Arcana/pull/825) HEAD pré-merge `fddf024566c406d83973b5eb14991b3f3ad05a9c`: **17 workflows / 18 checks concluídos com SUCCESS**, SHA de cada run conferido. Os dois jobs `verify` e `stage05_qa_companion_smoke` passaram. A execução pós-merge de `main@1cded69beef79f860454ecd2ace2de611e248168` [#39657350132](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39657350132) **estava em andamento no momento da criação deste checkpoint**; estado posterior deve ser checado novamente.
- As alterações técnicas estão em QA-only source sets e workflows; `src/main/` não foi alterado no PR #825. Observar classes ou eventos no companion não constitui consumo/mutação em produção.
- O [PR #866](https://github.com/Gustavaopere/Black-Arcana/pull/866) já estabilizou fixtures do índice UUID em GameTests e foi integrado anteriormente; **não** implicou promoção de Stage.
- **Stage 06.05:** 🟡 aceitação física pendente. **Stage 09:** ⚠️ real-client/Survival/modpack completo PENDING. **RPG Skill Tree:** progressão, atributos, Mastery/perks e gates só por contrato real; Black Arcana retém casting, rituais, world safety, domains e runtime próprio.

## Próximas lacunas objetivas
1. Resolver a diferença histórica **1.857/1.855 versus 1.856/1.854** por comparação do ledger de IDs e regras de deduplicação; até lá a barra global permanece **—%**.
2. Identificar os **4/39 providers condicionados** usando o ledger da campanha e a versão física da modlist, sem rotulá-los como ❌ não catalogados; obter prova binária/JAR instalado quando possível.
3. Continuar inspeção de consumidores e hooks de perks por campo (alcance, AOE/targeting, dano/tipo, projétil, duração, custo, cooldown, eventos e segurança mundo). Sem superfície real, **⛔ fail-closed**.
4. Executar QA provider-native e modpack/Survival para verificar o resultado real e deduplicação; registrar separadamente de testes unitários, hashes, JSON ou bytecode.

**Os percentuais acima são de eixos diferentes e não podem ser somados nem propagados automaticamente para Stage, integração de perks ou completude global.**
