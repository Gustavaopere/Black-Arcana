# Epic Fight — checkpoint técnico de perks (16/10/2026)

**Mod instalado (autoridade física já documentada):** `epicfight` / `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar` / SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`. Ver [auditoria do artefato exato](../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md) e [disposition integral](SKILL-DISPOSITION-21.17.3.1.md). O registry core foi classificado em **43/43 IDs exatos**, com **3 ações sobrenaturais** na métrica de magia e **40 skills não mágicas** úteis para pesquisa de perks. Nenhuma nova identidade semântica acrescentada neste lote.

## Barras separadas por nível de evidência

- **Global — universo de magias/rituais de todos os mods:** piso anterior **1.856 objetos semânticos mínimos / 1.854 estritos**, denominador total do pack **aberto (—%)**. Skills marciais não aumentam esse numerador.
- **Epic Fight — identidade e categoria do core (exato 21.17.3.1):** **43/43 = 100%** do registro core enumerado/dispositionado, sendo 3 `COUNTED_EXACT` e 40 `EXCLUDED` (o segundo termo é apenas exclusão da métrica de magia, não do escopo de perks).
- **Epic Fight — matriz de parâmetros para perks nesta tranche (source 21.17.3 adjacente):** **13/43 = 30,23%** do registry recebeu aprofundamento source-adjacent por habilidade, via **10 dossiês** (seis anteriores cobrindo 9 IDs, mais quatro passivas novas). **30/43 ainda fora destas tranches técnicas de profundidade**; não presumir que não tenham outra documentação histórica. O percentual mede **cobertura de pesquisa de código adjacente**, NÃO correspondência do JAR 21.17.3.1 nem capacidade de implementar perks.
- **Epic Fight — parâmetros JSON e presença de símbolos no JAR exato 21.17.3.1:** ✅ **9/43 = 20,93%** das skills do registro core passaram em um **gate binário estático limitado**: [run 38979022783](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38979022783) SUCCESS, SHA-1/SHA-256 iguais ao físico, nove JSONs empacotados sem desvio do esperado, 12 classes via javap, zero símbolos ausentes, seis testes sintéticos. [Prova e limites](../EXACT-BINARY-PERK-PARAMETERS-21.17.3.1.md). **Ainda não é** contrato hook/ABI/causalidade instrução-a-instrução, datapack aplicado, execução real, Mastery ou adapter. As quatro novas passivas continuam **SOURCE_ADJACENT ONLY**.

## Objetos aprofundados

| Grupo | IDs exatos do registro | Conteúdo auditado na revisão 21.17.3 (condicionado) |
|---|---|---|
| Defesa | [`parrying`](technical/PARRYING-21.17.3-SOURCE-ADJACENT.md) | janela8t, direção do ataque, `penalty×impact`, guard/parry e stamina |
| Defesa | [`impact_guard`](technical/IMPACT-GUARD-21.17.3-SOURCE-ADJACENT.md) | tipo de dano, `damage_reducer=.2`, tentativa de hurt residual e tags |
| Passiva | [`swordmaster`](technical/SWORDMASTER-21.17.3-SOURCE-ADJACENT.md) | `MODIFY_ATTACK_SPEED`, categorias de arma, `speed_bonus=30`, stamina/regen |
| Passiva | [`forbidden_strength`](technical/FORBIDDEN-STRENGTH-21.17.3-SOURCE-ADJACENT.md) | `CONSUME_SKILL`, fallback STAMINA→HEALTH e modifiers próprios |
| Dodge | [`roll` + `step`](technical/DODGE-ROLL-STEP-21.17.3-SOURCE-ADJACENT.md) | custo4/3 defaults, input cliente, execução server, animações/movesets e estado |
| Trident innate | [`wrathful_lighting`, `tsunami`, `everlasting_allegiance`](technical/TRIDENT-INNATES-21.17.3-SOURCE-ADJACENT.md) | `consumption` 50/50/40 (sem Resource confirmado), properties de attack phase e selector Riptide/Channeling/Loyalty |
| Passiva | [`technician`](technical/TECHNICIAN-21.17.3-SOURCE-ADJACENT.md) | `ON_DODGE` restitui stamina modificada; feedback por animation é separado; stamina regen +0.4 |
| Passiva | [`berserker`](technical/BERSERKER-21.17.3-SOURCE-ADJACENT.md) | health perdido, bônus por floor percentual, attack speed com cap 5.0, damage modifier e stamina +6 |
| Passiva | [`stamina_pillager`](technical/STAMINA-PILLAGER-21.17.3-SOURCE-ADJACENT.md) | `KILL_ENTITY` restaura 30% do déficit de stamina com teto de +2 por callback |
| Passiva | [`death_harvest`](technical/DEATH-HARVEST-21.17.3-SOURCE-ADJACENT.md) | `KILL_ENTITY` weapon-innate gera orb de recuperação de gauge, NÃO projétil ofensivo independente |

**Verificações documentais:** dez dossiês publicados e relidos; **52 âncoras SHA/linhas em 19 arquivos Java distintos** verificadas (**43 em 14** da tranche inicial + **9 em 5** das quatro novas passivas), sem intervalo inválido. Treze nomes de parâmetros `*.json` upstream consultados. **Prova binária adicional e separada:** run [38979022783](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38979022783) foi SUCCESS no publisher JAR SHA-exato, com 9 JSONs empacotados, 12 classfiles e 6/6 self-tests; o run inicial [38978906335](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38978906335) falhou por inspeção incorreta da classe externa `EpicFightEventHooks` e foi corrigido para as internas `$Entity` e `$Player`, mantendo os checks. Isso **não é QA visual, runtime, GameTest ou aceite físico do modpack montado**.

## Riscos prioritários e estratégia segura

1. **Discrepância de release delimitada:** o source pinado `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` declara `mod=21.17.3`; o JAR exato do pack é `21.17.3.1`. Os **9 parâmetros JSON iniciais** foram agora comprovados no binário SHA-exato. Isso **não estabelece equivalência global do source nem comportamento dos métodos**, tampouco prova os JSONs das quatro passivas novas. Inspecionar controle e ordem real dos métodos no JAR antes de aprovar qualquer hook per-player.
2. **Evento observável ≠ setter seguro:** `Entity.MODIFY_ATTACK_SPEED` e `Player.CONSUME_SKILL` existem na fonte adjacente. Contrato de listener, fase preflight, sidedness, composição de modifiers e alteração dos recursos no JAR físico ainda condicionados.
3. **Dano guard residual:** `ImpactGuardSkill` pode cancelar incoming e invocar um novo `hurt` reduzido, com novos `DamageSource` tags. Numa bridge com Iron's, não duplicar dano/crit/Mastery nem classificar automaticamente `DamageTypes.MAGIC` como todo dano magical provider.
4. **World safety:** as três trident-innates pertencem a Epic Fight. Não emitir thunder, recall ou teleport AOE de novo por Black Arcana; categorizar cast e efeitos secundários pelo mesmo root com dedup.
5. **Mastery:** progressão do RPG sibling só por fato comprovado de acerto/defesa/cast, não packet client, FX ou tentativa cancelada. Não assumir que o progress provider terá setter nativo para stamina, hitbox, i-frames, raio de ataque ou `DamageType`.

## Próximo bloco de auditoria

A partir do gate **9/9 JSON + 12/12 símbolos** exatos, auditar as **instruções e ordem causal** dos métodos (não apenas existência de símbolos), confirmar os quatro novos JSONs de **Technician, Berserker, Stamina Pillager e Death Harvest** no JAR, e avançar para **Guard base, Endurance e demais movimentos/weapon innates**. Fazer fichas de eixos individuais apenas para valores provados; `NÃO_VERIFICADO` nos demais. Revisar overlap com PR #795 e preservar branch `#825` draft enquanto QA/aceite não estiver fechado.

**Ownership:** Black Arcana = runtime próprio, rituals/world safety/Arcane Danger; RPG Skill Tree = progression/Mastery/perks/gates; Epic Fight = combat skills, stamina, animations/movesets e settlement; Enshrouded = Shroud/exposure próprios. Sem transferir autoridade por similaridade temática. Stage 06.05 🟡 / Stage 09 físico pendente, sem promoção.
