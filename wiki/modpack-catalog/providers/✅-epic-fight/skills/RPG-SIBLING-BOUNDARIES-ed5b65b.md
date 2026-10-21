# Epic Fight — contratos já presentes no RPG Skill Tree

**Autoridade consultada:** `Gustavaopere/neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`, código e testes existentes lidos em 21/10/2026. Este documento evita interpretar pendências do catálogo como ausência de runtime no sibling. Nenhum código RPG foi alterado ou reexecutado nesta rodada.

## Bootstrap e versão

[`RpgSkillTreeMod`](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ed5b65b890767b406ce41127bcb793775263c7bd/src/main/java/dev/gustavopere/rpgskilltree/RpgSkillTreeMod.java#L434-L457) chama `EpicFightProgressionHooks.register()` quando o adapter `EPIC_FIGHT` está ativo. [`EpicFightVersionContract.supportsVersion(String)`](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ed5b65b890767b406ce41127bcb793775263c7bd/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/epicfight/EpicFightVersionContract.java) exige igualdade com **`21.17.3.1`**. O build fixa `epicfight_version_id=8HHhJt6i` e range exato; não generalizar o contrato para versão futura.

## Matriz do código realmente existente

| Boundary | Registro e consumidor existentes | O que autoriza / limite |
|---|---|---|
| Custo de stamina | `EpicFightEventHooks.Player.CONSUME_SKILL` → `EpicFightProgressionHooks.onSkillConsume(SkillConsumeEvent)` → `EpicFightStaminaPolicy.adjustedCost(...)` → `event.setAmount(float)` | **`HOOK_VERIFICADO` no código do sibling**, somente para `ServerPlayerPatch`/player elegível, skill presente e `event.getResourceType()==Skill.Resource.STAMINA`. Modifica o valor antes do consumer; não cobra recurso, não prova cast concluído e não concede Mastery nesse callback. |
| Esquiva | `EpicFightEventHooks.Entity.ON_DODGE` → `onSuccessfulDodge(DodgeEvent)` | O sibling cria discovery `mastery:epicfight:dodge_success/first` e encaminha ao runtime canônico; repetições são bloqueadas pelo discovery persistido. Não premiar keybind, animação, tentativa ou `CONSUME_SKILL` em paralelo. |
| Hit e autoridade | `DELIVER_DAMAGE_PRE` → `onDealDamageAuthority(DealDamageEvent.Pre)` | Publica autoridade causal somente com alvo hostil e evidência de ataque direto do player; `EpicFightHitAuthority` pertence à integração RPG, não cria outro dano. |
| Resultado ofensivo | `DELIVER_DAMAGE_POST` → `onDealDamage(DealDamageEvent.Post)` | Descarta a referência de autoridade, exige player elegível/alvo hostil e `getModifiedDamage()>0`; resolve categoria pela capability da arma. Rewards são marcos por categoria/tipo de hostil ou política de punhos, usando `PlayerProgressionRuntime`/`WeaponMasteryMilestoneRuntime`. Não chamar `hurt` outra vez. |
| Troca de alvo, AOE, alcance, DamageType, collider | Não demonstrada por esses quatro callbacks | **`SEM_HOOK_SEGURO` neste levantamento** para ampliar tais campos. Um `setAmount` de custo não é setter de alvo, dano, projétil ou duração. |

Os registros e callbacks estão em [`EpicFightProgressionHooks.java`](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ed5b65b890767b406ce41127bcb793775263c7bd/src/main/java/dev/gustavopere/rpgskilltree/runtime/compat/epicfight/EpicFightProgressionHooks.java#L38-L176). A elegibilidade exclui `FakePlayer`, Creative e spectator; alvo hostil exclui self, aliados e invulnerável e exige `Enemy` ou `Player`. Estas são condições do código consultado, não observações novas de uma sessão real.

## Política de custo existente

[`EpicFightStaminaPolicy.adjustedCost(PassiveNodeProgress,String,float)`](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ed5b65b890767b406ce41127bcb793775263c7bd/src/main/java/dev/gustavopere/rpgskilltree/core/EpicFightStaminaPolicy.java#L15-L37) soma:

- `martial_000` aprendido: **0,05**;
- `martial_036`: **0,02 × min(3,rank)**;
- apenas categoria `DODGE` ou `MOVER`: `agility_000` aprendido **0,10**, mais `agility_036` **0,03 × min(3,rank)**.

Aplica `min(0,35,discount)` e retorna `originalCost × (1−discount)` convertido para float. **0,35 é o teto do código**, não a soma atingível garantida com esses quatro nodes. O método rejeita custo negativo/não finito; o callback normaliza o montante com `max(0,event.amount)` antes de chamá-lo. Outros listeners/provider-native podem alterar o evento; não concluir desconto final composto ou ordem universal só desta classe.

Exemplos que constam do teste existente: custo 10 sem nodes→10; `martial_000`/GUARD→9,5; `agility_000`/DODGE→9; `agility_000`/GUARD→10; configuração híbrida com os quatro nodes e ranks máximos/MOVER→7. [`EpicFightDepthPolicyTest`](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ed5b65b890767b406ce41127bcb793775263c7bd/src/test/java/dev/gustavopere/rpgskilltree/core/EpicFightDepthPolicyTest.java) também mantém Mastery fail-closed para pre-consume e procs e verifica marcos de hit/dodge. **O teste foi lido, não executado novamente nesta rodada.**

## Uso correto pelas fichas

1. Reutilizar o contrato existente no seu owner. Não adicionar outro listener Black Arcana/RPG para repetir o mesmo desconto ou reward.
2. O gate `Resource.STAMINA` é obrigatório: `consumption=50` de uma innate não se torna automaticamente stamina, mana ou desconto elegível. `WEAPON_CHARGE`, `HEALTH`, `COOLDOWN` e `NONE` não são convertidos por essa função.
3. `HOOK_VERIFICADO` acima significa existência e fluxo do código source-pinned no sibling. Não certifica automaticamente todas as skills, ABI futura, causalidade de cada dano final, ordem com outros listeners ou QA do modpack; testes adicionais devem pertencer ao contrato afetado.
4. Pendências de novos mutadores nas fichas não revogam esses contratos já presentes na `main`. A fonte de runtime é o sibling atual, e não o estado histórico de uma auditoria documental Black Arcana.
5. Black Arcana retém seu casting/domains/rituais/world safety/Arcane Danger; Epic Fight retém stamina, skills, animações e settlement; Enshrouded retém Shroud/exposure. Este levantamento não criou uma bridge Enshrouded por similaridade temática.

[Índice das 43 fichas](INDIVIDUAL-SKILL-CARDS-21.17.3.1.md) · [contrato de fichas](../../../meta/PERK-TECHNICAL-CATALOG-CONTRACT.md) · [progresso](../../../meta/PROGRESSO-CATALOGO-ATUAL.md).
