# Updraft Visual

- Registro: `aero_additions:updraft_visual`, `EntityType<UpdraftEntity>`, categoria `MISC`, tamanho **0.5×0.5**, tracking **64**.
- Ativação: **REGISTERED**; produtor ativo: finalização de recast de [Updraft](../spells/updraft.md). Contribuição estrita de magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). SHA-1 instalado histórico de 35 caracteres continua inválido/desconhecido.

## Lifecycle e alcance semântico

`UpdraftEntity extends Entity`. No construtor define rotação X=**−90°**, Y=**0°**. Não tem owner, alvo, damage field, colisão de dano, movimento ofensivo nem status aplicado. `defineSynchedData`, `readAdditionalSaveData` e `addAdditionalSaveData` são vazios: não salva idade ou estado auxiliar próprios.

No tick guarda posição XYZ; se `tickCount>8`, descarta, caso contrário chama `super.tick`; ao final restaura XYZ com `setPosRaw`. Portanto permanece na posição capturada a cada tick, com fim pelo teste de idade antes do incremento. O spell ainda chama `updraft.tick()` **antes** de `addFreshEntity`, iniciando sua idade no spawn; “oito ticks exatos visíveis” não é garantido sem QA. Age não é persistido pelo override local.

Na finalização de Updraft, o spell resolve cada UUID, soma impulso Y **0.9**, aplica **MOVEMENT_SLOWDOWN por 100 ticks, amplifier 3** e só então cria esta entidade em `target.getPosition(0.2f)`. O alcance helper **64**, a janela recast **80 ticks**, slots **2+level** e o alvo pertencem ao spell. O visual não aplica esse impulso/debuff, não acompanha explicitamente alvo depois e não aplica [Stunned](../effects/stunned.md). Tracking 64 não é raio de uma aura.

`UpdraftVisualRenderer` usa o model layer `irons_spellbooks:gust_model/main` e textura `irons_spellbooks:textures/entity/trident_riptide.png`. Faz três renders escalados, rotação por idade, escala inicial **(0.25,0.10,0.25)**, interpolação visual 1→2.3 em seis ticks e alpha `1−age/10`. O helper `createBodyLayer` define geometria, mas o construtor bakeia a camada Iron's existente; esses números não alteram AABB nem força do lançamento.

| Eixo para perks | Consumidor real | Fronteira |
|---|---|---|
| Impulso/slow/alvos | `UpdraftSpell.onRecastFinished` | A entidade é consequência visual. Hook de mutação por jogador **NOT_VERIFIED**; modificar render não altera status. |
| Vida/posição | `UpdraftEntity.tick` | TTL e posição são locais; aumentar duração visual não estende debuff nem lança novamente. |
| Persistência/sync | Métodos vazios + `Entity` host | Sem owner/target/NBT local para recuperar causalidade após reload. |
| Mastery | Nenhuma tentativa de dano no entity body | Não contar cada visual como magia ou hit adicional. |

QA: idade pré-spawn, vida no cliente dedicado, reload do visual, alvo descarregado e dissociação entre visual/impulso/debuff. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — registro L90–93](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L90-L93).
- [UpdraftEntity.java — contrato completo L9–38](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/updraft/UpdraftEntity.java#L9-L38).
- [UpdraftSpell.java — aplicação/visual L112–129](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/updraft/UpdraftSpell.java#L112-L129).
- [UpdraftVisualRenderer.java — modelo/render L24–65](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/updraft/UpdraftVisualRenderer.java#L24-L65).
