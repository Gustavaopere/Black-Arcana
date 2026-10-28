# AbstractSummonSpell — recast e invocação

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`AbstractSummonSpell.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/spells/AbstractSummonSpell.java) — `spells/AbstractSummonSpell.java`
- [`ExampleSummonSpell.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/spells/ExampleSummonSpell.java) — `spells/ExampleSummonSpell.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`AbstractSummonSpell extends AbstractSpell` de Iron's e é base abstrata, não registro próprio. `getEmptyCastData()` fornece `SummonedEntitiesCastData`; `getRecastCount` retorna **2**. `onCast` consulta `MagicData.getPlayerRecasts()`; só sem recast existente cria cast data novo, chama `onSummoningCast` definido pelo addon e usa o retorno como timer de `RecastInstance(spellId, spellLevel, recastCount, timer, castSource, castData)`. Adiciona o recast e sempre chama `super.onCast` ao final; presença de recast não repete localmente `onSummoningCast`.

`onRecastFinished` delega a `SummonManager.recastFinishedHelper` e só chama o método super se o helper retornar true. Remoção/contabilidade/lifetime efetivo e significado das duas recasts pertencem ao host; não interpretar 2 como duas novas invocações.

`spawnHelper(x,y,z,caster,level,summonTimer,castData,Supplier<K extends Mob>,spellId,spellLevel)` cria a entidade, posiciona-a, publica `SpellSummonEvent` e usa **`event.getCreature()`** tanto em `level.addFreshEntity` quanto em `SummonManager.initSummon`. Um listener pode substituir a criatura; não assumir que a instância do supplier é a adicionada. O helper não valida colisão/solo/LOS, não limita quantidade, não faz side-check próprio e não verifica o boolean retornado por `addFreshEntity`; admissão, lado e falhas de spawn exigem validação do consumidor/host. O evento de summon não comprova cast liquidado nem autoriza repetir spawn por um adapter.

## Targeting, geometria, custos e duração

Posições e entidade criada vêm do subclass/consumidor; `spellId`, `spellLevel` e `summonTimer` são parâmetros de helper. O exemplo não aparece como spell registrado neste provider.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não atribuir TTL, custo, distância, cap de número de summons ou callback do exemplo a todas as subclasses. Iron's é autoridade de cast, recast, custos e duração da entidade convocada.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
