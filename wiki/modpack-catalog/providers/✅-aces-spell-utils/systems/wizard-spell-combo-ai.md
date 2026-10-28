# WizardSpellComboGoal — seleção de combos por IA

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`WizardSpellComboGoal.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/goals/WizardSpellComboGoal.java) — `entity/mobs/goals/WizardSpellComboGoal.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`WizardSpellComboGoal extends Goal`; o construtor recebe `IMagicEntity`, `List<AbstractSpell>`, limites de qualidade `minQuality/maxQuality` e intervalos de ataque mínimo/máximo. Exige que a entidade seja `PathfinderMob`, senão lança `IllegalStateException`; flags MOVE/LOOK/TARGET, `attackRadius=20`, `interval=5`, índice inicial 0. Guarda a lista recebida e seu tamanho naquele instante, sem cópia defensiva; editar a lista depois pode divergir do tamanho capturado ([construtor][combo-constructor]).

`canUse` lê `mob.getTarget()` e retorna sem decrementar se sem alvo ou já casting. Fora disso reseta timer ao atingir `-5*(length-1)`, decrementa e aceita quando `attackTime<=0` e múltiplo de 5. `canContinueToUse` é false; `requiresUpdateEveryTick` true. A cadência depende das avaliações/scheduler do goal, não é cooldown próprio de spell; `stop` limpa alvo e, se o timer ainda é positivo, força-o além da sequência ([admissão][combo-admission]).

`tick` só tenta cast se distância² **<400**, sem teste local adicional de linha de visão/alvo vivo. Olha ao alvo com limites 45/45; pega a próxima spell e calcula `max(1, (int)(maxLevel * lerp(randomFloat,minQuality,maxQuality)))`, sem clamp superior ao maxLevel. Chama `initiateCastSpell`, incrementa o índice e para sem verificar resultado. `resetAttackTimer` sorteia intervalo mínimo/máximo inclusivo e zera índice; faixa de qualidade/lista vazia/intervalos inválidos não recebem validação nessa classe ([seleção e timer][combo-selection]).

## Targeting, geometria, custos e duração

Mob `PathfinderMob` e seu alvo de IA; identidade de spells é herdada da lista recebida e dos registros do addon consumidor.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não inferir todas as magias lançadas por bosses usando este goal; lista, qualidade, timings e checks dependem de quem constrói o Goal e da spell concreta. A chamada de início não prova cast aceito, hit ou crédito de Mastery.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**

[combo-constructor]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/goals/WizardSpellComboGoal.java#L13-L50
[combo-admission]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/goals/WizardSpellComboGoal.java#L52-L86
[combo-selection]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/goals/WizardSpellComboGoal.java#L88-L118
