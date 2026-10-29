# Telelinked — marcador sem produtor ativo

- Registro: `aero_additions:telelinked`, `MobEffect`, implementação `MagicMobEffect`, categoria `BENEFICIAL`, cor `0xdb74ff`.
- Ativação: efeito **REGISTERED**; magia produtora `TelelinkSpell` **NOT_REGISTERED**. Não promover o marcador a magia ativa. Contribuição estrita de magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). Publisher não sana o SHA-1 instalado histórico inválido de 35 caracteres.

## Alcance de código e comportamento

O registro é ativo, mas não há subclasse local, atributos, dano, movimento, tick, owner/link de grupo ou NBT próprios. A única aplicação provider-side localizada está em `TelelinkSpell.onRecastFinished`, cuja entrada em `AASpells` está comentada. Essa implementação inativa aplicaria o mesmo marcador ao caster e aos UUIDs resolvidos, sem gravar no efeito um vínculo entre eles, por `(int)((3×spellLevel×getSpellPower(level,caster)+12)×20)` ticks e amplifier default 0.

Os handlers de teleporte e pocket-dimension que consultariam o marcador em `AAServerEvents` estão **integralmente comentados**. Não existe consumidor ativo provider-side de “teleportar juntos” e nenhum dos dez spells ativos aplica Telelinked. Registro/asset/tradução permitem existência da identidade, mas não comprovam aquisição, produção via gameplay nem sincronização de teleporte. Aplicação por comandos ou outro mod é externa ao fluxo ativo auditado.

| Eixo para perks | Consumidor real | Fronteira |
|---|---|---|
| Aplicação/duração | Somente `TelelinkSpell` inativa; ver [código não registrado](../systems/unregistered-spell-code.md) | Não disponibilizar como perk de uma magia ativa. Hook **NOT_VERIFIED**. |
| Teleporte/grupo | Handlers propostos estão comentados | Nome do efeito não autoriza implementar teleporte nem inferir links persistidos. |
| Persistência | `MagicMobEffect`/`MobEffectInstance` do host | Sem lista de UUIDs ou NBT local no marcador; estado de recast é outro objeto. |
| Causalidade | Nenhum dano ou movimento local | Nenhum proc de Mastery certificado. |

QA: aplicação externa, expiração/sync e eventual integração futura exigem prova própria; o source não fecha comportamento de teleporte. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — registro do efeito L165–172](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L165-L172); [magia comentada L74–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L74-L78).
- [TelelinkSpell.java — aplicação inativa L77–110](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/TelelinkSpell.java#L77-L110).
- [AAServerEvents.java — teleporte comentado L141–170](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L141-L170); [pocket dimension/recall comentados L179–202](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L179-L202).
