# Seis spells — inventário estático exato

**Aprofundamento compilado adicional (18/10/2026):** ✅ [Sulfur Bomb e Pale Thorn: parâmetros exatos de dano, alvo, área e efeitos](../EXACT-BINARY-BOMB-THORN-0.1.2.md) comprovados pelo [workflow #39133252975](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39133252975), 10/10 autotestes, artifact **12138732504**. Estado individual agora: **5/6** spells têm ao menos um caminho causal delimitado binário; Slime Aspect continua com identidade física e parâmetros source-pinned, sem consumer-effect auditado. **6/6** registros já haviam sido contados; nenhum novo ID. ⚠️ QA real e configuração host pendentes.


**Prova binária adicional (18/10/2026):** ✅ [3/6 fichas com método compilado delimitado](../EXACT-BINARY-PERK-CONSUMERS-0.1.2.md) — Sulfur Clouds, Sulfur Release e Resin Spray, Java21 [#39131725388](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39131725388), 8/8 autotestes. **6/6 registradas** e **6/6 source-pinned** permanecem intactas; a aprovação de 3 métodos não equivale à homologação dos outros campos, ações ou perks.


**Atualização de fichas técnicas (18/10/2026):** ✅ **6/6 fichas** com source-pin de classe/`onCast`, defaults, geometria, dano/status, lifecycle e boundary de perks, sem copiar implementação. [Matriz transversal](../PERK-CAUSAL-SOURCE-MATRIX-0.1.2.md). Paridade completa de fórmulas com JAR 0.1.2, Iron's 3.16.3, configurações efetivas e gameplay: ⚠️ NÃO VERIFICADO. Quantidade de novas magias: **+0**.


**✅ 6/6** identidades em `ModSpellRegistry`, provadas no JAR 0.1.2 com metadata `0.1.0`. [Dossiê técnico](../EXACT-BINARY-SPELLS-0.1.2.md). Disponibilidade in-game e configuração **⚠️**.

1. [Slime Aspect](slime-aspect.md) — `backportedspellbooks:slime_aspect`
2. [Sulfur Bomb](sulfur-bomb.md) — `backportedspellbooks:sulfur_bomb`
3. [Sulfur Clouds](sulfur-clouds.md) — `backportedspellbooks:sulfur_clouds`
4. [Sulfur Release](sulfur-release.md) — `backportedspellbooks:sulfur_release`
5. [Pale Thorn](pale-thorn.md) — `backportedspellbooks:pale_thorn`
6. [Resin Spray](resin-spray.md) — `backportedspellbooks:resin_spray`

As seis identidades já compunham a contagem semântica. **+0** novas. Valores e efeitos da fonte de referência não substituem QA físico do runtime.
