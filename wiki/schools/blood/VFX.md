# Blood — VFX/Animação da reforma hemática

## Estado

`CONCEITO / PESQUISA`

- tether visual entre caster e fonte somente quando vínculo real estiver ativo;
- pulsos trafegam pelo tether apenas quando reserva/transferência for confirmada pelo servidor;
- fluxo visual de sangue segue a direção real da transferência, sem representar mB inexistentes;
- fontes autorizadas podem exibir marcas persistentes de vínculo;
- tipos especiais de sangue podem usar materiais/VFX distintos;
- reservatório deve mostrar nível/volume real armazenado;
- quebra de vínculo possui feedback visual/sonoro próprio;
- UI distingue `BLOOD`, `VITAL_ENERGY`, `SOUL/SPIRIT` e `MANA`;
- efeitos novos devem aproveitar Ace's Spell Utils / AAA Particles / GeckoLib quando apropriado sem transformar VFX em autoridade de gameplay.

O cliente nunca cria, consome ou confirma sangue; apenas representa snapshots/receipts server-authoritative.
