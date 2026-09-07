# Goety Cataclysm 1.21.1-1.8.2 — regras de integração

## Authority

A integração futura com Black Arcana deve preservar três autoridades distintas:

1. **Goety**: Soul Energy, Focus/Staff casting, servant ownership/lifecycle, rituals, Research e demais estados próprios;
2. **L_Ender's Cataclysm**: criaturas, bosses, ataques e gameplay nativo do mod-base;
3. **Goety Cataclysm**: conteúdo e conversões/bridges que o addon efetivamente registra entre os dois providers.

Black Arcana permanece autoridade apenas de seus próprios casts, hazards, rituals, spell domains, Corruption, Strain, Backlash e world-safety policies.

## Regras obrigatórias

- Não criar segunda Soul Energy ou converter mana Black Arcana em Soul Energy implicitamente.
- Não reconstruir um Focus/Staff cast de Goety dentro do canonical cast pipeline do Black Arcana.
- Não duplicar servant ownership, summon lifetime, AI ownership ou revive semantics.
- Não conceder custo/reembolso adicional quando o provider já liquidou o cast.
- Não aplicar dano uma segunda vez para “reconhecer” um spell do addon.
- Não inferir que um ataque parecido com Cataclysm é um cast Goety Cataclysm sem causalidade verificável.
- Não inferir registry IDs ou class names a partir de nomes visuais.
- Qualquer world effect destrutivo criado pelo próprio Black Arcana continua passando por `WorldEffectPolicy`.

## Causalidade e deduplicação

Uma integração só poderá reagir a um cast/ability do addon quando existir evidência provider-native suficiente para identificar:

- origem do evento;
- caster/owner;
- habilidade/Focus de origem;
- alvo ou área causal;
- momento de settlement;
- identidade de replay/deduplicação quando necessária.

Sem hook estável ou evidência equivalente, o adapter fica desabilitado/fail-closed. Observação por dano final, partículas, nome traduzido ou tipo visual de entidade não é boundary suficiente para conceder progressão ou disparar Arcane Danger.

## Arcane Danger

Goety Cataclysm não recebe Danger Profile automaticamente por ser “cataclysmic”, dark magic ou boss-derived.

Para qualquer spell futuro:

- Danger Profile precisa ser definido explicitamente pelo Black Arcana;
- Arcane Resistance/Corruption Resistance/Strain/Backlash não substituem as defesas/custos do provider;
- Backlash não pode gerar proc chains ofensivas normais;
- uma reação Black Arcana deve ser uma consequência adicional bounded, não uma segunda execução do spell do provider.

## Estado atual

`FAIL-CLOSED PARA INTEGRAÇÃO TÉCNICA ESPECÍFICA`.

A publicação exata foi identificada, mas a revisão source/API correspondente à build `1.21.1-1.8.2` não foi localizada. Portanto a documentação atual serve para authority mapping e deduplicação conceitual; ela não autoriza implementação de adapter provider-specific.
