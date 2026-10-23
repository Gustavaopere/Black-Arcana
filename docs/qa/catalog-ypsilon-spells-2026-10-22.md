# Ypsilon — 15 spells com parâmetros e consumidores, 22/10/2026

Base Black Arcana `97fb85b4d0dad0edc5b6673bbb94b803b894bb5c` (Principles #875 integrado). RPG/modlist `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`.

## Entrega e limites da evidência

Reauditoria das [15 fichas de spells existentes](../../wiki/modpack-catalog/providers/✅-ypsilons-fundamentalism/SPELL-PERK-BOUNDARIES-1.1.7.1.md), incluindo fórmulas/defaults, aquisição e filtros de alvo, dano/cura, geometria/colisão, entidades/efeitos downstream, tempos, custos, persistência, superfícies mutadoras e roteiro de QA. Um dossiê comum registra ordem do cast, eventos e autoridades dos projetos. **+0 identidades mágicas**; os 13 Principles continuam outro recorte documental, sem somar magias ou homologar o provider inteiro.

Source oficial Ypsilon `ypsilonM/FundamentalPrinciples-1.21.1@a9b8f8222fb2a800edece8c1568984bd2a764fc2`, versão declarada 1.1.7.1. A prova histórica de registry/classe mantém os 15 IDs do JAR SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da` (#575); não se refez equivalência source→classfiles nem inventário ao vivo. Host consultado: Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252` (3.16.3), distinto da dependência 3.16.2 do addon. Black Arcana usa NeoForge 21.1.248 em build/dev; o snapshot físico pinado registra 21.1.250.

`AbstractDomainEntity.java` tem o mesmo blob `1c830383020f373cc7304703a9fbeb307b70eede` nos sources oficiais Ace’s 1.2.6.1 (`0f6110925de4c4c0422095d9ee9ca8ce4009e438`) e 1.2.7.2 (`a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`). A identidade prova somente esse arquivo de source, sem afirmar equivalência dos JARs ou compatibilidade do conjunto.

Achados úteis para perks:

- Law of Regression anuncia cura com `SpellHealEvent`, cujo valor é final e não tem setter; esse evento não é mutador/cancelador da cura.
- Saeptum calcula refinement quadrático em power no ramo Player. Seu DamageSource comum não passa pelo ramo SpellDamageEvent do helper Iron’s. Captura em cubo, sure-hit esférico, construção e restauração têm contratos distintos.
- A base Ace’s mantém owner em map estático e não persiste os snapshots da barreira. A chamada de ticket passa argumento 20, sem demonstrar ticket level20 ou alcance efetivo em chunks.
- Sol separa hitbox com cap, raio bruto de AoE e força da explosão. O fallback local de Damage no load pode ser sobrescrito pelo host; colisão entity+block e persistência final exigem QA.
- Pull tem geometria dinâmica; Sacred Disk tem retorno sem timeout próprio demonstrado; Chains distingue duração/efeito/montaria; Lapsus guarda BlockPos sem dimensão em campo singleton.
- Taunt envia orientação pontual, sem lock contínuo. Laceration inclui arma mesmo sem enchantments; Thorn muda a marca antes de confirmar dano. Pyrokinesis distingue custo por settlement do canal de callbacks por tick.

Os contratos distinguem NATIVE/config global, evento mutador source-confirmado e ausência de hook seguro por campo. Nenhum runtime, adapter, perk, dependência ou lockfile foi alterado; nenhuma implementação ou arte upstream foi importada. A documentação não estabelece licença para redistribuição.

## Validação

- Inventário ativo `ModSpells`: **15 classes/IDs/fichas** reconciliados; registro comentado e StealSummon sem bootstrap excluídos.
- Nas 15 fichas e dossiê comum: **58 links locais**, **423 referências pinadas** conferidas contra arquivos e intervalos de linhas em **85 arquivos source distintos**. São referências, não 423 símbolos/API únicos nem prova binária.
- Nas 20 páginas Markdown do lote, antes deste relatório: **33 tabelas** com colunas válidas e **481 links locais** resolvidos.
- Revisão independente de todas as 15 fichas e do dossiê comum. Corrigidos o escopo ServerPlayer do gate em comandos, a leitura herdada de Damage de Sol, o filtro inicial de raycast de Ignite, a distinção dos loaders e a semântica do argumento de ticket.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/global_magic_catalog_test.py`: **52/52 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/catalog_physical_ledger_test.py`: **5/5 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/magic_pendency_tracker_test.py`: **26/26 PASS**.
- Painel JSON/Markdown: **164 providers**, 15/15 spells e 13/13 Principles separados, `runtime_acceptance=NOT_INFERRED`, denominador global aberto. Mínimos mágicos e campanha binária 38/39 preservados. `git diff --check` sem erro.

As verificações locais deste lote são documentais/source. O build/testes/servidor headless do ambiente sem Ypsilon não homologam estes spells. Config efetiva, aplicação de mixins, JAR funcional, proteção do mundo, Survival/cliente, multiplayer, persistência e coexistência continuam **PENDING**. Nenhum Stage é promovido. Resultado de PR/CI/merge deve ser comunicado após execução real, sem antecipar SHA ou aceite neste relatório.
