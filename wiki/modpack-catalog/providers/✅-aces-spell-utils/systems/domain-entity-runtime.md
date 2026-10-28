# AbstractDomainEntity — domínio e clash

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`AbstractDomainEntity.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java) — `entity/spells/AbstractDomainEntity.java`
- [`AcesSpellUtilsConfig.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/AcesSpellUtilsConfig.java) — `utils/AcesSpellUtilsConfig.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`AbstractDomainEntity` é uma classe abstrata de entidade, com dados sincronizados para radius, refinement, open/transported, clash e spawn time. `onActivation()` define tempo pelo mundo, adiciona `TicketType.FORCED` por região no servidor e avalia domínios locais num AABB limitado pelo raio. O coeficiente configurável de vitória automática por refinement é `Refinement victory factor`, default 1.5. `tick()` trata ciclo de clash, transporte e `targetSureHit`, sendo `handleDomainClash`, `handleSureHit` e `handleTransportation` pontos de extensão.

## Targeting, geometria, custos e duração

Entidades dentro de AABB centrado no domínio e filtro de distância `distanceTo < getRadius()`; `canTarget` tenta excluir owner e alguns aliados. O raio é estado por entidade, não parâmetro de um spell autônomo.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Há ticket de chunk forçado em `onActivation`; `destroyDomain()` descarta a entidade e atualiza o mapa de clashes, mas a limpeza do ticket não é demonstrada nesse método. Não concluir vazamento real sem QA do host. Domínio de terceiros NÃO é Black Arcana Domain: qualquer alteração de bloco precisa do `WorldEffectPolicy` do Black Arcana quando originada por ele.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
