# AbstractDomainEntity — domínio e clash

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`AbstractDomainEntity.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java) — `entity/spells/AbstractDomainEntity.java`
- [`AcesSpellUtilsConfig.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/AcesSpellUtilsConfig.java) — `utils/AcesSpellUtilsConfig.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`AbstractDomainEntity` é uma classe abstrata de entidade, com dados sincronizados para radius, refinement, open/transported, clash e spawn time. Defaults: radius/refinement/tempo em clash 0, open/transported/clashing false, clashable true, spawn time `Long.MIN_VALUE`; `spawnAnimTime` começa em `Integer.MAX_VALUE`. No `tickCount == 1`, `tick()` chama `onActivation()`: no servidor define tempo pelo mundo e adiciona `TicketType.FORCED` com nível 20/`forceTicks=true`; a busca de clashes não possui gate servidor adicional ([campos][domain-defaults], [defaults sincronizados][domain-sync-defaults], [ativação][domain-activation], [tick][domain-tick]).

Na ativação, ignora o outro domínio se ele não for clashable ou se ambos têm o mesmo owner não-null. Testa primeiro `outro.refinement / este.refinement >= factor` para destruir este; depois o inverso para destruir o outro; senão registra clash recíproco. O config `Refinement victory factor` tem default 1.5, sem faixa no builder mostrado. Refinement 0 não recebe guarda de divisão; não pressupor empate balanceado para zero/negativos. Durante clash incrementa o contador e chama `handleDomainClash`; sem clash chama sure-hit quando aberto ou transportado ([comparação][domain-activation], [config][domain-config], [tick][domain-tick]).

Transporte exige fechado, não transportado, sem clash, `tickCount > spawnAnimTime` e entidade não removida. `canTransport()` é **private**, apesar do comentário sobre override; o consumidor configura o delay e sobrescreve `handleTransportation`, cujo default só marca transported true. `handleDomainClash`, `handleSureHit` e `onAntiMagic` são vazios: a base não implementa dano, teleport real, expiração total ou counterspell ([gates e callbacks][domain-callbacks], [transporte][domain-transport]).

## Targeting, geometria, custos e duração

Tanto a busca de domínios como sure-hit consultam AABB de posição **±`radius/2`**, depois filtram `distanceTo < radius`; isso não cobre automaticamente uma esfera inteira de radius. Sure-hit consulta `Entity`, sem exigir living/linha de visão. `canTarget` exclui a própria entidade e seu owner, mas a checagem de tame compara o owner do candidato consigo mesmo e a de projectile compara `proj.getOwner()` ao próprio candidato; não são filtro comprovado de aliados do caster. O raio é estado por entidade, não parâmetro de um spell autônomo ([scan de clash][domain-activation], [alvos][domain-target]).

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

O NBT da entidade salva radius/refinement/open/transported/spawn-time/clashable/time-clashing/clashing; a interface `serializeNBT` salva somente `Spawn Time`, `Time Spent Clashing` e `Clashing`. Nenhuma rota salva owner, lista de oponentes ou spawnAnimTime. `destroyDomain()` descarta, retira referências dos oponentes e a entrada no clash map; não remove ownerMap nem o ticket nessa classe. O tick continua após pedir destruição por morte do owner. São riscos de lifecycle a validar, sem concluir vazamento real no host ([cleanup][domain-cleanup], [tick][domain-tick], [persistência][domain-nbt]). Domínio de terceiros NÃO é Black Arcana Domain: qualquer alteração de bloco precisa do `WorldEffectPolicy` do Black Arcana quando originada por ele.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**

[domain-defaults]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L27-L45
[domain-activation]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L48-L91
[domain-tick]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L149-L178
[domain-config]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/AcesSpellUtilsConfig.java#L18-L22
[domain-callbacks]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L107-L130
[domain-transport]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L180-L188
[domain-target]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L116-L147
[domain-cleanup]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L93-L105
[domain-nbt]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L294-L345

[domain-sync-defaults]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/entity/spells/AbstractDomainEntity.java#L318-L328
