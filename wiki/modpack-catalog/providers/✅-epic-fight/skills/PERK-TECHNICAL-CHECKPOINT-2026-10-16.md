# Epic Fight — checkpoint técnico de perks (16/10/2026)

**Mod instalado (autoridade física já documentada):** `epicfight` / `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar` / SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`. Ver [auditoria do artefato exato](../EXACT-21.17.3.1-ARTIFACT-SKILL-AUDIT.md) e [disposition integral](SKILL-DISPOSITION-21.17.3.1.md). O registry core foi classificado em **43/43 IDs exatos**, com **3 ações sobrenaturais** na métrica de magia e **40 skills não mágicas** úteis para pesquisa de perks. Nenhuma nova identidade semântica acrescentada neste lote.

## Barras separadas por nível de evidência

- **Global — universo de magias/rituais de todos os mods:** piso anterior **1.856 objetos semânticos mínimos / 1.854 estritos**, denominador total do pack **aberto (—%)**. Skills marciais não aumentam esse numerador.
- **Epic Fight — identidade e categoria do core (exato 21.17.3.1):** **43/43 = 100%** do registro core enumerado/dispositionado, sendo 3 `COUNTED_EXACT` e 40 `EXCLUDED` (o segundo termo é apenas exclusão da métrica de magia, não do escopo de perks).
- **Epic Fight — matriz de parâmetros para perks nesta tranche (source 21.17.3 adjacente):** **9/43 = 20,93%** do registry recebeu aprofundamento novo por habilidade, via **6 dossiês** (5 marciais/defensivos cobrindo 6 IDs e 1 transversal dos 3 trident innates). **34/43 ainda fora desta tranche técnica de profundidade**; não presumir que não tenham outra documentação histórica. O percentual mede **cobertura de pesquisa de código adjacente**, NÃO correspondência do JAR 21.17.3.1 nem capacidade de implementar perks.
- **Epic Fight — comprovação física dos parâmetros/hook nesta tranche:** **NÃO VERIFICADO / —%**, sem suite binária específica ou test provider-present; nenhuma perk/adaptor ou Mastery adicionada.

## Objetos aprofundados

| Grupo | IDs exatos do registro | Conteúdo auditado na revisão 21.17.3 (condicionado) |
|---|---|---|
| Defesa | [`parrying`](technical/PARRYING-21.17.3-SOURCE-ADJACENT.md) | janela8t, direção do ataque, `penalty×impact`, guard/parry e stamina |
| Defesa | [`impact_guard`](technical/IMPACT-GUARD-21.17.3-SOURCE-ADJACENT.md) | tipo de dano, `damage_reducer=.2`, tentativa de hurt residual e tags |
| Passiva | [`swordmaster`](technical/SWORDMASTER-21.17.3-SOURCE-ADJACENT.md) | `MODIFY_ATTACK_SPEED`, categorias de arma, `speed_bonus=30`, stamina/regen |
| Passiva | [`forbidden_strength`](technical/FORBIDDEN-STRENGTH-21.17.3-SOURCE-ADJACENT.md) | `CONSUME_SKILL`, fallback STAMINA→HEALTH e modifiers próprios |
| Dodge | [`roll` + `step`](technical/DODGE-ROLL-STEP-21.17.3-SOURCE-ADJACENT.md) | custo4/3 defaults, input cliente, execução server, animações/movesets e estado |
| Trident innate | [`wrathful_lighting`, `tsunami`, `everlasting_allegiance`](technical/TRIDENT-INNATES-21.17.3-SOURCE-ADJACENT.md) | `consumption` 50/50/40 (sem Resource confirmado), properties de attack phase e selector Riptide/Channeling/Loyalty |

**Verificações do lote:** seis arquivos documentais publicados e relidos no GitHub; **43 âncoras source-pinned em 16 arquivos Java** foram verificadas quanto a SHA, existência e limites de linhas (**37** nos primeiros 5 documentos + **6** no trident, sem intervalo inválido). Nove nomes de parâmetros `*.json` distintos foram consultados no upstream. Nenhum compilador, GameTest, reprodução de bug, correspondência de bytecode 21.17.3.1 ou QA visual foi executado como parte da documentação.

## Riscos prioritários e estratégia segura

1. **Discrepância de release:** o source pinado `Antikythera-Studios/epicfight@a78aa24b72e90a9d09f5fd61925e4369d117abaf` declara `mod=21.17.3` em `gradle/libs.versions.toml`. O pack utiliza publisher JAR `21.17.3.1`. Mesmo patch/minor não é equivalência provada. Executar auditoria bytecode de métodos e extrair `skill_parameters` **do JAR físico exato** antes de aprovar qualquer hook per-player.
2. **Evento observável ≠ setter seguro:** `Entity.MODIFY_ATTACK_SPEED` e `Player.CONSUME_SKILL` existem na fonte adjacente. Contrato de listener, fase preflight, sidedness, composição de modifiers e alteração dos recursos no JAR físico ainda condicionados.
3. **Dano guard residual:** `ImpactGuardSkill` pode cancelar incoming e invocar um novo `hurt` reduzido, com novos `DamageSource` tags. Numa bridge com Iron's, não duplicar daño/crit/Mastery nem classificar automaticamente `DamageTypes.MAGIC` como todo dano magical provider.
4. **World safety:** as três trident-innates pertencem a Epic Fight. Não emitir thunder, recall ou teleport AOE de novo por Black Arcana; categorizar cast e efeitos secundários pelo mesmo root com dedup.
5. **Mastery:** progressão do RPG sibling só por fato comprovado de acerto/defesa/cast, não packet client, FX ou tentativa cancelada. Não assumir que o progress provider terá setter nativo para stamina, hitbox, i-frames, raio de ataque ou `DamageType`.

## Próximo bloco de auditoria

Auditar no binário físico os parâmetros e hooks das 9 skills deste lote (preferir Java21 + fingerprint exato e comparação com o upstream), depois avançar para **Guard base, Technician, Berserker, Stamina Pillager, Death Harvest, Endurance e demais movimentos/weapon innates**. Fazer fichas de eixos individuais apenas para valores provados; `NÃO_VERIFICADO` nos demais. Revisar overlap com PR #795 e preservar branch `#825` draft enquanto QA/aceite não estiver fechado.

**Ownership:** Black Arcana = runtime próprio, rituals/world safety/Arcane Danger; RPG Skill Tree = progression/Mastery/perks/gates; Epic Fight = combat skills, stamina, animations/movesets e settlement; Enshrouded = Shroud/exposure próprios. Sem transferir autoridade por similaridade temática. Stage 06.05 🟡 / Stage 09 físico pendente, sem promoção.
