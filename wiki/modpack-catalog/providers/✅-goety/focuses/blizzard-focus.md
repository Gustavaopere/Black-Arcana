# Goety 3.1.4 — `blizzard_focus`

Status: **✅ CATALOGADO / COUNTED_EXACT** · identificador factual obtido da auditoria do **JAR 3.1.4 hash-matched** · **⚠️ funcionamento físico/números não validados nesta etapa**.

## Identidade canônica

- **Provider:** Goety (mod id `goety`).
- **JAR instalado e auditado:** `goety-3.1.4.jar` (NeoForge/Minecraft 1.21.1); SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`.
- **Identidade de Focus no artefato:** `blizzard_focus` — item/ação de Focus ativo do conjunto exato de 123. Não é o `empty_focus` proxy.
- **Posição no inventário exato:** 10/123. Número ordinal editorial, não identificador de registry ou ordem de carregamento.
- **Aquisição documental:** o JAR exato contém receita base de aquisição homônima para este Focus e sem condition de mod carregado; o conjunto tem 80 recipes de tipo `goety:ritual` e 43 shaped. **O tipo específico desta receita não é deduzido apenas pela lista agregada.** A execução real com recursos/progressão do modpack não foi comprovada nesta etapa.
- **Conta semântica:** `COUNTED_EXACT`, já incluída nos 123 Focuses Goety do ledger; materializar a ficha **não acrescenta uma nova identidade**. Receitas alternativas de obtenção não criam outros spells.
- **Escola/categoria exata, classe e método runtime, cast-time, Soul Energy, cooldown, alcance, dano, efeitos, targeting, PVP/proteção, progressão/research e numeric balance:** **NÃO VERIFICADO nesta ficha**. A identificação factual do item não estabelece automaticamente contrato de API/efeito.

## Authority e deduplicação

Goety é a autoridade de Soul Energy, Focus/Staff casting, custos, recipe execution, servants, cleanup e estado persistente. Black Arcana não cria outro Soul ledger, uma segunda conjuração, um débito adicional, novo summon ou uma segunda world mutation; quaisquer bridges futuras exigem boundary server-safe comprovada e comportamento fail-closed.

## Evidência

- [Inventário semântico exato 3.1.4](../EXACT-3.1.4-SEMANTIC-INVENTORY.md): lista de **123** nomes `_focus` ativos, com `empty_focus` excluído e aquisição agregada 80/43.
- [Auditoria do artefato](../EXACT-3.1.4-ARTIFACT-AUDIT.md): hash físico verificado e exclusões.
- [Fronteira de integração](../INTEGRATION-RULES.md) e [catálogo anterior](../FOCUS-CATALOG.md).

**Clean-room:** a ficha contém dados factuais de identidade e proveniência, não código, assets, tradução de tooltip ou implementação upstream.

## Dossiê para Codex e perks — identidade binária, lógica condicionada

- **Objeto real confirmado:** `goety:blizzard_focus` é um Focus físico do Goety `3.1.4`, conforme inventário de 123 Focuses no JAR SHA-matched. Esta ficha **não** comprova que o Focus seja uma classe distinta nem que o ID do item seja um spell ID executável.
- **Identidade do artefato:** `goety-3.1.4.jar`, SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`; [proveniência e auditoria](../EXACT-3.1.4-ARTIFACT-AUDIT.md).
- **Código/assinaturas do runtime exato:** classe do feitiço/Focus, método de `cast`, registration de subspell, custo real de Soul Energy, cooldown, radius, targeting, duração, dano, damage type e eventos de interceptação: **NÃO VERIFICADO** no artefato atual por este dossiê. Não preencher utilizando branch Goety `1.20` ou versões 3.1.5/3.2.0: não são o JAR instalado.
- **Matriz de perks:** `source-linked-class=⛔`, `native-resource-authority=Goety`, `damage/range/area/targets=⛔ sem contrato`, `spawn/servant owner=Goety`, `RPG Skill Tree=progressão somente quando existir boundary legítimo`.
- **Próxima prova exigida:** class/member/bytecode da versão SHA-exata, vínculo item → spell executor, config real, contexto da área, política de alvo, consumo e eventos; após isso passar para análise de mutabilidade, caps e QA. **Fail-closed** para perks geométricas e custo.

**Status separado:** ✅ item/identidade binária já catalogados; ⚠️ parâmetros e causalidade do cast ainda não catalogados com evidência suficiente; ⛔ bridge de mutação sem hook. Esta anotação não altera os 123 objetos semânticos.
