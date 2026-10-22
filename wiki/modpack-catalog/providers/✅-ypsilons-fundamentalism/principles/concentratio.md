# Concentratio — Principle / sistema de progressão

**Provider:** Ypsilon's Fundamentalism / Fundamental Principles (`ypfundamentals`) · **tipo:** categoria/passiva, não spell registrado · **enum:** `CONCENTRATIO` · **chave técnica:** `createEntity`. Não inventar `ypfundamentals:concentratio` como registry ID de magia: a chave de categoria é string do ledger. **+0 identidades mágicas.**

Amplia a capacidade de mana do jogador pelo atributo nativo do Iron's, sem criar uma segunda reserva.

## Autoridade e evidência

JAR do inventário físico versionado: `ypfundamentals-1.1.7.1.jar`, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`, modlist RPG #575. [Prova binária histórica dos 15 spells](../EXACT-BINARY-SPELLS-1.1.7.1.md) não valida os métodos da passiva. Esta ficha é `SOURCE_PARAMETERS / SOURCE_CAUSALITY`, pin oficial [a9b8f8222fb2a800edece8c1568984bd2a764fc2](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L33), Minecraft 1.21.1/Java21/NeoForge; source declara dependência de Iron's `1.21.1-3.16.2`, pack usa `3.16.3`. Config efetiva e aplicação dos mixins no JAR instalado **NÃO VERIFICADO**. Reauditoria documental: 22/10/2026.

## Matriz para perks

`l` é nível deste Principle, salvo quando explicitado outro; faixa normal de setLevel: 0–20. Defaults abaixo são de ServerConfig no source, não leitura da config implantada. `NATIVE` designa passiva/config já existente; `CONDITIONAL` exige versão, owner, fase e coexistência; `SEM_HOOK_SEGURO` registra ausência de seam externo demonstrado neste escopo, não impossibilidade universal.

| Eixo | Fórmula, fase e limites | Mutabilidade para integração |
|---|---|---|
| Mana / valor | Δmana = l × manaAdd; default manaAdd=20 → 0–400 unidades para l=0–20. Retorna 0 se ACTIVE_CONCENTRATIO ou PRINCIPLES_SYSTEM estiver desativado. | NATIVE: configuração global e MAX_MANA; não é reserva/refund por cast. |
| Atributo / identidade | YpsAttributeManager.MANA mira Iron's MAX_MANA com ADD_VALUE e modifier ypfundamentals:entity_mastery. applyModifier remove a identidade anterior, reaplica transient somente se l>0 e há AttributeInstance. | CONDITIONAL: modifier do provider, não reutilizar seu ID no RPG. |
| Tempo / lifecycle | setLevel de PrinciplesLevelsAttachment chama MANA.applyModifier para esta categoria. Login/respawn/clone elegível reinicializam; logout limpa o modifier. Reconfiguração imediata sem restart não foi demonstrada. | CONDITIONAL: config marcada worldRestart; testar refresh e coexistência. |
| Outros eixos | Nenhum novo intent de cast, projétil, summon ou alteração de DamageType é criado pela identidade de Principle. Range, target/área, hitbox, duração e dano não descritos acima continuam provider-owned; campo não auditado = NÃO VERIFICADO, não setter presumido. | SEM_HOOK_SEGURO para transplantar modificações entre providers. |

**Origem dos valores:** [Util helper](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/util/Util.java#L152) · [ServerConfig defaults](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/ServerConfig.java#L210).

## Pipeline e consumidores

Nível source do attachment → Util.getTotalMana → AttributeModifierManager no atributo Iron's. Não há cobrança de mana, alvo, projectile spawn, hurt ou heal nesta passiva. O nível também participa do gate de Saeptum (Concentratio≥12 junto a outros Principles) e de Util.getRefinementMultiplier; isso não concede domínio novo nem autorização de execução a Black Arcana.

**Símbolos exatos:** [YpsAttributeManager#MANA](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/YpsAttributeManager.java#L13) · [AttributeModifierManager#applyModifier](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/AttributeModifierManager.java#L25) · [YpsAttributesHandler#initializeAttributes](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/YpsAttributesHandler.java#L55).

## Progressão, power e deduplicação

A classificação por ASM é uma heurística do provider para o registry global, não prova de alvo/dano efetivo de cada spell. `SpellNerfCast(SpellOnCastEvent)` executa em ServerPlayer, concede XP às categorias retornadas quando PRINCIPLES_SYSTEM está ativo e CastSource é diferente de SCROLL. Não há filtro explícito de creative/spectator ou token pai/filho nesse trecho; não importar a elegibilidade de Mastery do RPG como se fosse do Ypsilon. `calculateXpFromSpell` depende de raridade e CONTINUOUS, depois multiplica principleXpMultiplier. O attachment inicializa em 0, setLevel limita 0–20, e custo de `n→n+1` usa `(int)(20+20×1,3^(n+1))` (primeiro 0→1 = 46), não 40. Persistência/sync e verificação de funcionamento estão no [contrato comum](README.md).

`PowerSpellsMixin` também altera getSpellPower para Player: soma um termo `Pbase×(basePower+levelAddition×nívelCategoria)` por categoria; as subcategorias usesShoot/createsAoeEntities/usesSummon/usesTargeting recebem metade se configurado. Depois multiplica pela razão de fatigue quando ativa. Defaults −0,10 e +0,01; não é substituição de P por apenas esse termo. A ativação de cada passiva não é checada individualmente nesse loop de power. Esse efeito compartilhado pode influenciar os demais campos do spell que consumam P e não é novo dano terminal.

**Referências comuns:** [enum dos 13 Principles](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/util/Principles.java#L3) · [nome técnico](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/PrinciplesProgressionManager.java#L165) · [setLevel/clamp](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/customAtt/PrinciplesLevelsAttachment.java#L88) · [XP/cast event](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L567) · [power compartilhado](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/mixins/principlesMixins/PowerSpellsMixin.java#L35).

RPG Skill Tree continua authority de seus atributos/perks/Mastery; Ypsilon mantém seu ledger, categorias, fatigue e efeitos. Black Arcana mantém seu runtime mágico/world safety; Enshrouded mantém Shroud/exposure. Não escrever attachment do provider, aplicar novamente sua passiva nem conceder XP paralelo sem contrato de integração comprovado. Mixin privado é localizador de comportamento, não API pública de perk.

## QA e próximos testes

Comparar MAX_MANA antes/depois nos níveis 0/1/20, refund/redução de nível, login/death/restart e flags; verificar soma com investimentos do RPG sem sobrescrever modifier ou duplicar capacity.

Estado: **source examinado; runtime/config/cliente/Survival/modpack PENDING**. Nenhum adapter/perk, cópia de código/assets ou promoção de Stage. Descrição é resumo original do código consultado; links servem para inspeção, não incorporam implementação. [Índice e licença](README.md).
