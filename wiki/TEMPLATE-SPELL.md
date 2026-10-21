# <Nome do Feitiço>

## Estado

`<IMPLEMENTADO / CANÔNICO | IMPLEMENTADO / VALIDAÇÃO FINAL DEFERIDA | PLANEJADO | CONCEITO / PESQUISA | BLOQUEADO / FAIL-CLOSED>`

## Identidade

- **ID:** `<namespace:id>`
- **Escola/domínio:** `<...>`
- **Provider/host:** `<...>`
- **Tier/raridade:** `<...>`
- **Função:** `<dano / controle / utilidade / defesa / mobilidade / ritual / suporte>`

## Descrição para o jogador

<TBD>

## Obtenção e aprendizado

- **Como desbloquear:** `<...>`
- **Como aprender:** `<...>`
- **Item/scroll/spellbook/ritual:** `<...>`
- **Requisitos:** `<...>`
- **Gate de RPG Skill Tree:** `<...>`

## Custo e casting

- **Recurso:** `<mana / sangue mB / vida / spirit / outro>`
- **Custo base:** `<...>`
- **Escalonamento de custo:** `<...>`
- **Cooldown:** `<...>`
- **Cast time:** `<...>`
- **Channel time:** `<...>`

## Targeting

- **Alcance:** `<...>`
- **Área:** `<...>`
- **Máximo de alvos:** `<...>`
- **Linha de visão:** `<...>`
- **Regras de seleção:** `<...>`

## Efeito mecânico

- **Dano base:** `<...>`
- **Tipo de dano:** `<...>`
- **Escalonamento:** `<...>`
- **Duração:** `<...>`
- **Efeitos secundários:** `<...>`
- **Interações especiais:** `<...>`

## Balanceamento e limites

- **PvP:** `<...>`
- **Bosses:** `<...>`
- **Summons/minions:** `<...>`
- **Anti-farm:** `<...>`
- **Hard ceilings:** `<...>`

## Authority / pipeline

- **Authority:** `<...>`
- **Pipeline canônico:** `<...>`
- **Deduplicação:** `<...>`
- **Fallback:** `<...>`
- **Fail-closed:** `<...>`

## Visual, animação e áudio

- **Casting pose:** `<...>`
- **VFX:** `<...>`
- **Shader/post-processing:** `<...>`
- **SFX:** `<...>`
- **HUD/feedback:** `<...>`

## Integrações

- **Iron's Spells:** `<...>`
- **Ars Nouveau:** `<...>`
- **Goety/Malum/Eidolon/Vampirism:** `<...>`
- **RPG Skill Tree:** `<...>`
- **Outros:** `<...>`

## Craft/ritual/estrutura

<TBD ou N/A>

## Implementação

- **Classes/runtime:** `<...>`
- **Data files:** `<...>`
- **Estado persistente:** `<...>`
- **Notas técnicas:** `<...>`

## Auditoria causal para perks (obrigatória para ficha técnica)

Padrão completo: [PERK-TECHNICAL-CATALOG-CONTRACT.md](modpack-catalog/meta/PERK-TECHNICAL-CATALOG-CONTRACT.md). Identificação de registry não comprova mutabilidade externa.

### Identidade física e código-fonte

- **JAR atual / hash:** `<nome exato + SHA e modlist, se verificados>`
- **Versão / source pin:** `<release e commit/tag do código correspondente; divergências>`
- **Registry / classe / método / signature:** `<símbolos comprovados + permalink>`
- **Config default / config implantada:** `<distinguir; valores em ticks/s/blocos>`
- **Nível de prova:** `<SOURCE_PINNED | RELEASE_BOUNDED | COUNTED_EXACT | CONDITIONAL | UNKNOWN, por campo>`

### Pipeline de execução verificado

- **Ingresso e desbloqueio:** `<trigger, item, skillbook, ritual, packet, Survival, server>`
- **Preflight e costs:** `<server gates, authority, reserve/commit/refund>`
- **Target resolver:** `<tipo, entidade/bloco/área, LOS, range, filtros, teto e claims>`
- **Spawn / hit / efeitos:** `<classes, phase, projectile AABB, hurt method, damage type, efeitos derivados>`
- **Cooldown / duração:** `<momento de aplicação, cast/channel, ticks/s, lifecycle>`
- **Duplicação e riscos:** `<child casts, DOT, procs, PvP, multi-hit, griefing, resources>`

### Campos modificáveis (um estado e evidência por eixo)

| Eixo | Valor atual (base, escala, teto, unidade) | Onde é resolvido (classe#método/config) | Seam e fase | Possibilidade / pendência |
|---|---|---|---|---|
| Dano e tipo de dano | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO |
| Alcance / LOS | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO |
| Alvo (self/entity/block/area) | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO |
| Área / max targets | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO |
| Projétil (hitbox/scale/velocidade/lifetime) | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO |
| Tempo (cast/channel/duração/DOT/cooldown) | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO |
| Recursos, custos e refunds | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO |
| Status/summons/world effects | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO | NÃO VERIFICADO |

**Vocabulário de viabilidade:** `CONFIG_NATIVE`, `HOOK_VERIFICADO`, `CONTRATO_CONDICIONAL`, `SEM_HOOK_SEGURO` ou `NÃO_VERIFICADO`. Preencher `N/A` quando eixo não se aplica; não inferir hook de uma classe ou da possibilidade de modificar via mixin. Alteração single-target→AOE, tipo de dano ou hitbox fica **⛔ fail-closed** sem método pré-settlement validado.

### Contrato de integração proposto (somente após validação)

- **Perk e provider owner:** `<...>`
- **Hook real / assinatura / versão:** `<... ou SEM_HOOK_SEGURO>`
- **Server-side / fase antes de damage/cost settlement:** `<...>`
- **Caps / safety / compatibilidade / dupla aplicação:** `<...>`
- **Teste e comportamento observado:** `<não testado até existir evidência>`

## Testes

- [ ] Unitário
- [ ] GameTest
- [ ] Integração provider
- [ ] Dedicated-server smoke
- [ ] Real-client VFX/input

## Referências e proveniência

- **Fontes do comportamento atual:** `<repo/docs/API>`
- **Inspirações externas:** `<fonte + aspecto abstrato adaptado>`
- **Observação de IP:** não reproduzir texto, nomes exclusivos, símbolos ou arte proprietária de terceiros; adaptar apenas conceitos mecânicos gerais.
