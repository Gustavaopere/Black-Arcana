# Blood Price

## Estado

`IMPLEMENTADO / AUTOMAÇÃO VERDE / VALIDAÇÃO FINAL DE MODPACK DEFERIDA`

## Identidade

- **Domínio:** Blood & Curses
- **Função:** custo alternativo/risk-reward
- **Host/provider atual:** compõe com recurso provider-owned; integração confirmada com Iron's mantém Iron's como autoridade do custo ordinário.

## Descrição

Permite substituir parcialmente um custo mágico ordinário por vida real do conjurador, dentro de limites server-authoritative e de forma transacional.

## Custo e casting

- **Recurso ordinário:** provider-owned; no adapter de Iron's, mana permanece authority do Iron's.
- **Substituição:** vida real do conjurador.
- **Percentual/valor final de gameplay:** `TBD — Stage 08 / balanceamento` quando não estiver fixado por configuração/runtime de produção.
- **Commit:** a vida é reservada/refundável até o cast canônico ser confirmado.

## Regras

- não pode gerar loop de imortalidade/feedback positivo;
- custo deve ser resolvido antes da substituição;
- falha do cast não pode consumir vida definitivamente;
- rollback não pode devolver mais do que foi reservado;
- backlash não deve ser reinterpretado como custo hemático ordinário.

## Relação com a nova Arcana Hemática

Este spell **não representa o modelo final** da nova disciplina sem mana. Ele é uma implementação existente de substituição parcial de custo e serve como referência técnica de transação/rollback. A futura Arcana Hemática deve usar sangue próprio/armazenado/vinculado diretamente, sem depender de mana normal.

## Obtenção/aprendizado

`TBD — reconciliar com Stage 08/progressão e host final do spell.`

## Dano

N/A — Blood Price é uma mecânica de custo, não um ataque por si só.

## Cooldown / cast time

Herdados/associados ao spell hospedeiro; não existe cooldown autônomo documentado para a substituição de custo.

## VFX/HUD

`TBD` — apresentação deve refletir claramente a parcela paga por vida e nunca sugerir regeneração de mana hemática.

## Testes

O domínio 07.01 possui testes automatizados RED→GREEN para quote/provider contract; a evidência final do domínio passou JUnit, build NeoForge, JAR inspection, GameTests e dedicated-server smoke. Validação real-modpack/manual permanece deferida.
