# Iron's 3.16.3 — execução QA passiva de Burning Dash e Eldritch Blast

**Escopo:** observação e validação de logs de **duas magias já inventariadas** no perfil Minecraft 1.21.1 / NeoForge **21.1.248** / Java 21. **Stage 06.05 continua 🟡**. Este protocolo não implementa spells, perks ou Mastery. A PR #825 continua *draft* enquanto faltam os testes físicos.

## Autoridades e evidência já obtida

- O runtime de Iron's é responsável pela cobrança, status dos recasts e aplicação de dano. Black Arcana não executa casts de terceiros nem altera custo, cooldown, i-frames, entidades ou campos de provider.
- [Actions #38830097297](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38830097297) **SUCCESS** no JAR **publicado** `irons_spellbooks-1.21.1-3.16.3.jar`, SHA-256 `13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73`: `BurningDashEffect.applyEffectTick` descarta o booleano de `DamageSources.applyDamage` e alcança `invulnerableTime` no mesmo ramo sem condição local intermediária; `AbstractSpell.castSpell` consulta recast e publica `SpellOnCastEvent` antes de `onCast`; timeout e persistência possuem códigos compilados. **É prova estática**, não medição de jogo.
- [Dossiê transversal](../../wiki/modpack-catalog/providers/✅-irons-spells/audits/CAUSAL-PERKS-DAMAGE-CANCEL-AND-RECAST-SESSION-3.16.3.md): 21 referências fonte em dez arquivos da revisão imutável `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`, com limites e gates.

## Fixture isolada e ativação

Fonte [`IronsEventPhaseRuntimeEvidence.java`](../../src/catalogQaProbe/java/dev/gustavopere/blackarcana/qa/catalog/IronsEventPhaseRuntimeEvidence.java), pertencente **somente** ao JAR auxiliar `black_arcana_catalog_qa`, compilado por `./gradlew --no-daemon catalogQaProbeJar jar`. O JAR de produção `black_arcana` não deve conter a classe. A fixture é **desativada por padrão**.

Na cópia **autorizada e isolada** do servidor físico, colocar o JAR auxiliar compatível com a revisão testada, junto de Black Arcana e Iron's, e informar o argumento JVM de boot:

`-Dblack_arcana.catalog_qa.irons_event_phase=true`

Isso é um argumento JVM, **não** comando no chat do jogo. Não confundir com `-Dblack_arcana.catalog_qa.arrow_volley=true` (outra fixture). Os dois podem ser usados no mesmo QA, mas a emissão do fingerprint de Iron's ocorre **uma vez no boot** para ambos, com tag `[BLACK_ARCANA_ARROW_VOLLEY_QA]` por reaproveitamento do coletor existente.

A fixture examina **apenas eventos públicos**: `SpellOnCastEvent` de `irons_spellbooks:eldritch_blast`, `SpellDamageEvent` de `irons_spellbooks:burning_dash`, `LivingDamageEvent.Post` para a fonte correspondente e `ServerTickEvent.Post` para snapshots de fechamento. O `SpellOnCastEvent` não representa por si só uma sessão de Mastery; o `SpellDamageEvent` é tentativa e pode ser cancelado antes de `hurt`.

**Limites de segurança:** no máximo **8 atores**, **64 alvos**, **64 eventos de cast**, **192 tentativas**, **16 snapshots pendentes simultâneos**, **16 IDs locais de sessão** e intervalo máximo de **100 ticks** entre snapshots de ativação correlacionados. Ultrapassar qualquer limite emite `budget_exhausted`, que o parser considera **FAIL_CLOSED**. Os slots de ator/alvo/sessão são **identificadores locais efêmeros**, não UUIDs reais nem tokens públicos do Iron's. Não são salvos em NBT nem reaproveitados como chave de progressão.

## Cenários físicos mínimos — não executados até anexar evidência

1. **Burning Dash — caso permitido:** cast legítimo contra alvo LivingEntity controlado, coletando `SpellDamageEvent`, `LivingDamageEvent.Post` e leitura de `invulnerableTime` até o fim do tick. Comparar tentativas e pós-danos, sem multiplicar XP por tick.
2. **Burning Dash — caso veto:** num servidor QA com um listener de teste/claim autorizado, vetar uma tentativa, confirmar sua classificação e amostrar i-frames do alvo. Uma flag `cancelled_event_snapshot=true` expressa **somente estado do evento no instante da observação**; outros listeners podem alterar esse estado depois, e o parser não declara que o helper retornou false. Se não houver `LivingDamageEvent.Post`, isso **não prova isoladamente** a causa do veto.
3. **Eldritch Blast — sessão completa:** níveis **1–5**, conjuração inicial e **2–6 recasts adicionais** nominais, 80 ticks por janela, mana/cooldown provider-owned, danos e efeitos visuais separados. Medir eventos e estado do recast **antes e depois** da ativação. O instrumento classifica `ROOT_CANDIDATE`, `RECAST_CANDIDATE` e `UNLINKED_RECAST`; isso não comprova identidade de sessão sem provedor.
4. **Interrupções/concorrência:** teste isolado de timeout, relog, morte, troca de dimensão, ataque simultâneo ao mesmo alvo, spell cancelado, claims/PvP e outros mods. Quando não houver raiz observada ou houver múltiplas tentativas no mesmo tick/target, exigir **FAIL_CLOSED**.
5. **Proveniência:** coletar log integral do servidor, Java, NeoForge instalado, lista/fingerprint dos mods pertinentes, hash do JAR auxiliar, condições da execução e captura de jogo; não assumir que o hash do JAR publicado é o do servidor instalado. O fingerprint registrado no log pelo auxiliar ainda precisa ser confrontado com o arquivo físico autorizado.

## Logs e classificação

A tag `[BLACK_ARCANA_PHASE_QA]` é emitida pelo observador read-only:

- `type=cast`: ator e sessão locais, `ROOT_CANDIDATE`/recast, `prior_recast`, tick e nível original versus snapshot mutável do evento. O uso de `MagicData` é exclusivamente leitura.
- `type=cast_followup`: recast ativo e mana em snapshot **depois** do cast, amostrado no `ServerTickEvent.Post`.
- `type=damage_followup`: tentativa, ator/alvo locais, cancelamento **observado durante o evento**, contagem de posts correlacionados, ambiguidade e i-frames antes/depois.
- `type=budget_exhausted`: captura incompleta, rejeitada.

O correlator de pós-dano procura **mesma dimensão, ator, alvo e tick**, mas isso é uma **heurística**, não identificador de hit do Iron's. Múltiplas tentativas na mesma combinação são marcadas ambíguas e não geram créditos. Outros mods podem modificar i-frames entre o evento e o fim do tick, logo um delta de i-frames **não prova sozinho causalidade**.

Na raiz do checkout, executar:

`python3 docs/qa/irons_3163_event_phase_trace_check.py --log runs/server/logs/latest.log --report build/qa/irons-event-phase.json`

O parser [`irons_3163_event_phase_trace_check.py`](./irons_3163_event_phase_trace_check.py) requer checksum do Iron's no log, um padrão consistente de raiz/recasts e followup e rejeita dados ausentes/ambíguos. Seu melhor resultado possível é **`TRACE_CLASSIFIED_NOT_GAMETEST`**. [Testes sintéticos do parser](./irons_3163_event_phase_trace_check_test.py) **não** contam como execuções no Minecraft.

## Aprovação e bloqueios

| Gate | Situação |
|---|---|
| Bytecode estático do JAR publicado 3.16.3 | ✅ Actions #38830097297 |
| Compilação do novo observador com API public/provider no JAR auxiliar | 🟡 consultar Actions do HEAD de implementação |
| Testes sintéticos do parser | 🟡 consultar Actions do HEAD de implementação |
| Logs reais de cast/dano/recast no NeoForge 21.1.248 instalado | ⚠️ pendente |
| Testes físicos de cancelamento, pós-hit, timeout e NBT | ⚠️ pendente |
| Mastery/XP por recast, manipulação de i-frame ou reprocessar dano vetado | ⛔ bloqueado |

Nenhum avanço de Stage 06.05, merge ou alteração do runtime do Iron's é autorizado por logs sintéticos. O Black Arcana mantém sua autoridade mágica; RPG Skill Tree permanece sibling exclusivo de atributos, Mastery/perks e gates por contrato real.
