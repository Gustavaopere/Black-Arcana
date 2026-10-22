# Perceptio — Principle / sistema de progressão

**Provider:** Ypsilon's Fundamentalism / Fundamental Principles (`ypfundamentals`) · **tipo:** categoria/passiva, não spell registrado · **enum:** `PERCEPTIO` · **chave técnica:** `usesRaycast`. Não inventar `ypfundamentals:perceptio` como registry ID de magia: a chave de categoria é string do ledger. **+0 identidades mágicas.**

Recalcula o comprimento do raycast antes da execução, incluindo uma nova base dependente da distância original; não é só somar blocos por nível.

## Autoridade e evidência

JAR do inventário físico versionado: `ypfundamentals-1.1.7.1.jar`, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`, modlist RPG #575. [Prova binária histórica dos 15 spells](../EXACT-BINARY-SPELLS-1.1.7.1.md) não valida os métodos da passiva. Esta ficha é `SOURCE_PARAMETERS / SOURCE_CAUSALITY`, pin oficial [a9b8f8222fb2a800edece8c1568984bd2a764fc2](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L33), Minecraft 1.21.1/Java21/NeoForge; source declara dependência de Iron's `1.21.1-3.16.2`, pack usa `3.16.3`. Config efetiva e aplicação dos mixins no JAR instalado **NÃO VERIFICADO**. Reauditoria documental: 22/10/2026.

## Matriz para perks

`l` é nível deste Principle, salvo quando explicitado outro; faixa normal de setLevel: 0–20. Defaults abaixo são de ServerConfig no source, não leitura da config implantada. `NATIVE` designa passiva/config já existente; `CONDITIONAL` exige versão, owner, fase e coexistência; `SEM_HOOK_SEGURO` registra ausência de seam externo demonstrado neste escopo, não impossibilidade universal.

| Eixo | Fórmula, fase e limites | Mutabilidade para integração |
|---|---|---|
| Alcance / fórmula | Se flags Perceptio/global ativas: R=8+D/5+(int)(l×addRange) blocos; default addRange=1,5. D=start.distanceTo(end). Exemplo D=100,l=0 →28; l=20 →58 antes de Locus. Conversão int trunca a parcela por nível. | NATIVE: substitui parte da base; não descrever como alcance original +1,5l. |
| Composição / target | Em RaycastBuilder#performRaycast HEAD exige originEntity ServerPlayer. Se bbInflation>0 e Locus/global ativos, multiplica R pelo Locus do mesmo jogador. Sem Perceptio, base é D; ainda pode sofrer Locus. Preserva direção normalizada e atualiza end. | CONDITIONAL: a ordem Perceptio→Locus é source-confirmada; filtros/LOS continuam host-owned. |
| Reuso / caps | Não consulta usesRaycast por ID, não tem limite absoluto de blocos e não marca builder como já processado. Nova chamada pode recalcular sobre end modificado. Não força chunks explicitamente neste mixin; proteção/lifecycle do consumidor NÃO VERIFICADO. | SEM_HOOK_SEGURO para destino/target kind/área por analogia com range. |
| Outros eixos | Nenhum novo intent de cast, projétil, summon ou alteração de DamageType é criado pela identidade de Principle. Range, target/área, hitbox, duração e dano não descritos acima continuam provider-owned; campo não auditado = NÃO VERIFICADO, não setter presumido. | SEM_HOOK_SEGURO para transplantar modificações entre providers. |

**Origem dos valores:** [Util helper](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/util/Util.java#L188) · [ServerConfig defaults](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/ServerConfig.java#L265).

## Pipeline e consumidores

Distância original do builder → base 8+D/5 e bônus truncado quando ativo → Locus condicional → novo end → performRaycast host. Não altera bbInflation nem aumenta diretamente hitbox. Perceptio≥12 também é requisito combinado de Saeptum, sem executar domínio ou contornar proteção.

**Símbolos exatos:** [RaycastBuilderMixin#adjustRaycastRange](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/mixins/principlesMixins/RaycastBuilderMixin.java#L32).

## Progressão, power e deduplicação

A classificação por ASM é uma heurística do provider para o registry global, não prova de alvo/dano efetivo de cada spell. `SpellNerfCast(SpellOnCastEvent)` executa em ServerPlayer, concede XP às categorias retornadas quando PRINCIPLES_SYSTEM está ativo e CastSource é diferente de SCROLL. Não há filtro explícito de creative/spectator ou token pai/filho nesse trecho; não importar a elegibilidade de Mastery do RPG como se fosse do Ypsilon. `calculateXpFromSpell` depende de raridade e CONTINUOUS, depois multiplica principleXpMultiplier. O attachment inicializa em 0, setLevel limita 0–20, e custo de `n→n+1` usa `(int)(20+20×1,3^(n+1))` (primeiro 0→1 = 46), não 40. Persistência/sync e verificação de funcionamento estão no [contrato comum](README.md).

`PowerSpellsMixin` também altera getSpellPower para Player: soma um termo `Pbase×(basePower+levelAddition×nívelCategoria)` por categoria; as subcategorias usesShoot/createsAoeEntities/usesSummon/usesTargeting recebem metade se configurado. Depois multiplica pela razão de fatigue quando ativa. Defaults −0,10 e +0,01; não é substituição de P por apenas esse termo. A ativação de cada passiva não é checada individualmente nesse loop de power. Esse efeito compartilhado pode influenciar os demais campos do spell que consumam P e não é novo dano terminal.

**Referências comuns:** [enum dos 13 Principles](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/util/Principles.java#L3) · [nome técnico](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/PrinciplesProgressionManager.java#L165) · [setLevel/clamp](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/customAtt/PrinciplesLevelsAttachment.java#L88) · [XP/cast event](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L567) · [power compartilhado](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/mixins/principlesMixins/PowerSpellsMixin.java#L35).

RPG Skill Tree continua authority de seus atributos/perks/Mastery; Ypsilon mantém seu ledger, categorias, fatigue e efeitos. Black Arcana mantém seu runtime mágico/world safety; Enshrouded mantém Shroud/exposure. Não escrever attachment do provider, aplicar novamente sua passiva nem conceder XP paralelo sem contrato de integração comprovado. Mixin privado é localizador de comportamento, não API pública de perk.

## QA e próximos testes

Validar D=0/10/50/100, níveis ímpares com truncamento, bbInflation 0/positivo, Locus ativo/inativo e reuse do builder; testar range de aquisição separado de impacto e chunks/proteções.

Estado: **source examinado; runtime/config/cliente/Survival/modpack PENDING**. Nenhum adapter/perk, cópia de código/assets ou promoção de Stage. Descrição é resumo original do código consultado; links servem para inspeção, não incorporam implementação. [Índice e licença](README.md).
