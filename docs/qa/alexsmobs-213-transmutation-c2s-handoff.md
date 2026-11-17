# Alex's Mobs Continued 2.1.13 — Transmutation Table C2S: evidência individual

**Estado:** 🟡 auditoria SHA-exata read-only / descoberta inicial; `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`.

## Motivação e proveniência

Após a integração da PR #1106 (Dimensional Carver), a próxima ação do recorte observado de Alex's Mobs é **Item Transmutation**, hoje 0/3 contratos estáticos. A [ficha existente](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/actions/item-transmutation.md) documenta `MenuTransmutationTable.clickMenuButton`, `MenuTransmutationTable.transmute` e `TileEntityTransmutationTable`, mas não demonstra o **handler nativo completo** de `MessageTransmuteFromMenu` nem a proveniência do remetente, da seleção e da sessão.

Autoridade física: modlist atual do sibling `alexsmobs-2.1.13-neoforge+1.21.1.jar`, mod ID `alexsmobs`, Minecraft 1.21.1 NeoForge / Java 21; SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`, 27.452.738 bytes. Auditoria exata anterior PR #511 / GitHub Actions 36949047824. Não usar `Codx-org/AlexsMobsContinued` 2.2.3 como prova da versão instalada.

## Questão técnica central

A ficha já comprova que `clickMenuButton` envia seleção e que o menu faz settlement de item/XP/reroll após guardas específicos. **Isso não comprova que o receptor C2S autentica o jogador da conexão, vincula o menu atual, valida o índice sem confiar em dados do cliente, impede replay ou evita duplo settlement.** Sem essas garantias, nenhuma perk pode modificar custo, opções, output, XP ou reroll com segurança.

## Protocolo verificável

O [probe](alexsmobs_213_transmutation_c2s_probe.py), [13 testes sintéticos](alexsmobs_213_transmutation_c2s_probe_test.py) e [workflow](../../.github/workflows/alexsmobs-213-transmutation-c2s.yml) auditam **três classes** no publisher físico:

- `com/github/alexthe666/alexsmobs/message/MessageTransmuteFromMenu.class`;
- `com/github/alexthe666/alexsmobs/inventory/MenuTransmutationTable.class`;
- `com/github/alexthe666/alexsmobs/tileentity/TileEntityTransmutationTable.class`.

O auditor confere duplamente SHA do JAR, tamanho e major JVM 65, lista de métodos/descritores, SHA do corpo interpretado, contagens de branches e callsites relevantes. Publica somente janelas **curtas e delimitadas** de operandos, sem copiar corpo inteiro ou redistribuir JAR de terceiros.

O primeiro run imprime `UNSEALED_TRANSMUTATION_C2S_DISCOVERY`; após inspeção das evidências reais, fixar o manifesto `EXACT-TRANSMUTATION-C2S-2.1.13.json`, atualizar esta nota e a ficha individual, e repetir `--snapshot`. A aplicação de regras de segurança exigirá reconstrução dos branches/ligações **efetivamente** observados e testes negativos; uma mera referência de `getSender` não prova que o retorno seja usado como autoridade no settlement.

## Estados e gates

- **Inventário:** três raízes semânticas presentes (1 `COUNTED_EXACT` transmutation, 2 `CONDITIONAL`); não criar novas raízes para as três alternativas de output.
- **Contrato estático:** manter 0/3 enquanto faltarem eixos e certificação individual.
- **Recepção C2S:** avaliar compatibilidade do contexto, playerId, containerMenu, slot, escolha e persistência; declarar desconhecido tudo que não estiver demonstrado.
- **Perks e Mastery:** no máximo mapeamento de candidatos conceituais; `NO_MUTATION` / fail-closed.
- **QA física:** `AMC-T01..T03` e teste de multiplayer, mudança de inventário, disconnect/reload, seleção inválida e replay continuam `NOT_TESTED`.
- **Stage:** 06 permanece ativo; a auditoria não implementa nem promove a Stage.

Nenhuma alteração em Raygun, X-Ray, ACArmorMaterial, Enshrouded ou RPG Skill Tree é feita nesta etapa.
