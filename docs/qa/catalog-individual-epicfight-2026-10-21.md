# Catálogo técnico — fichas Epic Fight e progresso por provider

## Escopo e fontes

- Data: **21/10/2026**.
- Branch: `docs/catalog-individual-epicfight-20261021`.
- Base Black Arcana: `bab5cd14d02edcab76af0a0f5839860548c435b9`.
- RPG Skill Tree/modlist: `ed5b65b890767b406ce41127bcb793775263c7bd`.
- Enshrouded: `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`.
- JAR publisher Epic Fight: [CurseMaven 405076 / 8175609](https://cursemaven.com/curse/maven/epic-fight-mod-405076/8175609/epic-fight-mod-405076-8175609.jar), **8.578.288 bytes**; SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`, SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`. Hashes conferidos nesta rodada, comparados à evidência física registrada; não à instalação ao vivo.
- Fonte comparativa recuperada: `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf`, que declara **21.17.3** em `gradle/libs.versions.toml`. Não presumir equivalência integral com o JAR **21.17.3.1**.

## Alterações e contagem

**40 fichas core novas + três fichas de ações existentes enriquecidas = 43 caminhos dedicados por ID**, incluindo 42 skills jogáveis e uma sentinela. Os 28 dossiês source-adjacent continuam sendo análises de apoio. **+0 objetos mágicos**, +0 adapters e +0 hooks mutadores homologados. Foi documentado separadamente um recurso `air_slash.json` sem vínculo core comprovado.

O [painel corrente](../../wiki/modpack-catalog/meta/PROGRESSO-CATALOGO-ATUAL.md) relaciona **164 providers** da árvore e **13 recortes quantificados** com proveniência. Os outros percentuais ficam indeterminados; nenhum zero de trabalho é inferido. Mínimo semântico **≥1.856/≥1.854**, campanha selecionada de identidade **38/39**, universo técnico total aberto. Corrigidas as referências correntes que ainda tratavam #825 como draft ou Iron's como não auditado.

## Verificação local executada

1. SHA-1/SHA-256 e tamanho do JAR; `read_jar_parameters` + `compare_parameters` do verificador existente: **42/42 objetos JSON core**, sem divergências. Este passo não executa `javap`, método do provider ou jogo.
2. Enumeração exaustiva do diretório de parâmetros no ZIP: **43 JSONs = 42 core + `air_slash.json`**. `empty.json` ausente, conforme o contrato de sentinela. `air_slash` contém `consumption=2.0`.
3. Leitura do pool UTF-8 do classfile `EpicFightSkills`: **43/43 literais core esperados presentes**, sem literal `air_slash`. Presença de símbolos não prova algoritmo de registro nem causalidade instrucional; os gates binários anteriores continuam como evidência separada.
4. Mapa documental: **43 IDs únicos e 43 caminhos únicos**, 42 jogáveis, uma sentinela e três raízes mágicas já existentes; todos os caminhos e links locais das fichas conferidos.
5. Localizadores: FQCN, existência de arquivo/método e limites de âncoras confrontados com a fonte recuperada; revisão por campo mantém `SOURCE_ADJACENT`. Assinatura localizada não é API mutadora homologada.
6. Painel: **164 diretórios** realmente existentes, todos com README; 13 métricas limitadas; denominador/numerador global técnico nulos. SVGs parseados como XML, sem scripts ou recursos externos.
7. Regressões existentes: `global_magic_catalog_test.py`, `catalog_physical_ledger_test.py`, `provider_39_evidence_queue_test.py` e `epicfight_211731_perk_binary.py --self-test`; resultados finais de CI/merge são registrados na PR e conferidos no SHA exato antes do merge.

Não foram criados testes que apenas espelham a formatação das fichas. As verificações de cobertura procuram falhas reais de contagem, caminhos, identidade, recurso extra e falsa promoção de evidência.

## Cruzamento do runtime sibling

Lidos o bootstrap, gate de versão, callbacks e testes existentes em RPG `main@ed5b65b`: `EpicFightProgressionHooks.register`, `onSkillConsume`/`EpicFightStaminaPolicy.adjustedCost`, `onSuccessfulDodge`, `onDealDamageAuthority` e `onDealDamage`. O [dossiê de contratos existentes](../../wiki/modpack-catalog/providers/✅-epic-fight/skills/RPG-SIBLING-BOUNDARIES-ed5b65b.md) está vinculado às 43 fichas. Ele distingue mutadores de custo STAMINA já implementados de novos campos sem hook comprovado. Código/testes sibling foram lidos, não reexecutados; nenhum runtime foi modificado.

## Limites e continuidade

Java local disponível: **17**. Os testes Java/NeoForge completos são executados pelo CI Java **21**, sem declarar build local inexistente. Esta rodada não realizou sessão de cliente, jogador conectado, consumo em gameplay, dano final, configuração implantada, PvP/claims ou integração do RPG/Enshrouded. O CI não resolve essas pendências por inferência.

Nenhum arquivo de `src/main/`, JAR, asset, texto de tooltip ou implementação upstream foi incluído. As fichas contêm resumos originais, fatos/parâmetros, símbolos e localizadores para interoperabilidade. Casting, recursos e settlement dos providers permanecem sob suas autoridades; Black Arcana, RPG Skill Tree e Enshrouded preservam os respectivos contratos.

**Continuação:** fechar denominadores por objeto nos providers ainda não quantificados, incluir addons/habilidades não mágicas, aprofundar consumidores downstream e provar hooks mutadores server-side por campo. `air_slash` permanece recurso sem consumidor comprovado. Stage 06.05 🟡 / Stage 09 físico PENDING; sem promoção.
