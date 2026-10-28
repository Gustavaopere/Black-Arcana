# WizardSpellComboGoal — seleção de combos por IA

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`WizardSpellComboGoal.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/mobs/goals/WizardSpellComboGoal.java) — `entity/mobs/goals/WizardSpellComboGoal.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`WizardSpellComboGoal extends Goal`; o construtor recebe `IMagicEntity`, `List<AbstractSpell>`, limites de qualidade `minQuality/maxQuality` e intervalos de ataque mínimo/máximo. Possui controle de alvo, contador `attackTime` e ciclo de seleção/execução de um combo AI via `canUse`, `canContinueToUse`, `tick` e `resetAttackTimer`. `interval = 5` é constante observada no helper.

## Targeting, geometria, custos e duração

Mob `PathfinderMob` e seu alvo de IA; identidade de spells é herdada da lista recebida e dos registros do addon consumidor.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não inferir todas as magias lançadas por bosses usando este goal; lista, level, peso, timings e checks são responsabilidade de quem constrói o Goal. Não usar callback de IA como prova de hit ou crédito de Mastery.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. Código-fonte Ace compilou contra Iron's `3.16.2` no build pinado; pack usa `3.16.3` segundo inventário, exigindo teste efetivo.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
