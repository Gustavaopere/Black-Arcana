# Limestone Spear

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; provider OPEN. Não representa nova raiz mágica ou cast certificado.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10; Minecraft 1.21.1 / NeoForge 21.1.250 documental / Java 21. Modlist física sibling #019; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Não houve comparação nova com dump físico instalado nem observação do runtime transformado. [Dossiê de descoberta SHA-exata](../EXACT-JELLY-KEYBIND-LIMESTONE-1.0.10.md) e [replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45651673635/job/139337522318): 186.937 bytes, SHA-256 `61a6010adbe0c6f41968a6ffc8f85e8c4c6e013175007f6be93280d3cf2da0ed`, duas saídas byte-idênticas, seis checks. O dossiê detalha consumidores, hashes de métodos e offsets. Replay da HEAD consolidada obrigatório.

## Identidade e descrição funcional

`alexscaves:limestone_spear`, factory `ACItemRegistry.lambda$static$45`, Code SHA `33b072bd23f120bb5040ee52db21241e05a6589692f0a9d9c95565bf8a70ccef`; [registro](../systems/item-registry.md). Owner `LimestoneSpearItem`, SHA-256 `1f068faf0b5829d4c63ab56a09a6c9fc2de6b57c030ae58c6d3211ffacd86510`, dois corpos próprios, ancestral SpearItem. Arma que solicita criação/lançamento de entidade ao liberar uso; resultado efetivo e dano não estão certificados.

## Ativação e parâmetros

Factory solicita stack máximo 16; construtor passa 3D ao ancestral (significado confirmado na prova suplementar abaixo). releaseUsing, 76 instruções, Code SHA `6f034115f35bc9a3586a7f76ffc78ce4be38241ffaf23e418d6c1b7d13559037`: exige Player; elapsed=getUseDuration−remaining, power=getPowerForTime(elapsed), prossegue se power>0,1D. Cria LimestoneSpearEntity(Level,LivingEntity,ItemStack) @50, shootFromRotation @76 com XRot/YRot, offset 0, velocidade argumento 2,5×power, inaccuracy 1. Se instabuild solicita pickup=CREATIVE_ONLY. addFreshEntity @101; retorno/settlement não deve ser presumido como sucesso. Sem guarda explícita de lado observada nesse corpo.

Som LIMESTONE_SPEAR_THROW / PLAYERS volume/pitch 1. Solicita shrink(1) fora de instabuild @144 e ITEM_USED @156. Receita declarativa usa três limestone e duas posições de tag rods/wooden, produz quatro itens. Modelo throwing=1 e Better Combat weapon_attributes parent bettercombat:spear são metadados; integração ativa NÃO VERIFICADA.

## Targeting, efeitos, autoria, persistência e custos

Owner passado ao construtor é o Player/LivingEntity; não prova persistência ou atribuição final. Dano/tipo downstream, alcance, colisão, pickup, trajetória, AOE, knockback, cooldown, custos efetivos, encantamentos e permissões ainda NÃO VERIFICADOS. Não confundir parâmetro inicial de velocidade com velocidade efetiva. Próximos gates: LimestoneSpearEntity, consumers/hits e engine distribuída, recursos e tags efetivos, compatibilidade, world safety e settlement. NO_MUTATION, sem hook confirmado, não duplicar lançamento ou custo, sem Mastery.

## Reuso do contrato parcial do ancestral SpearItem

[Run 45794089646/job 139820166475](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089646/job/139820166475), SHA `7d70e29eb4bd2df5df5fe73720d1bd6213b61e7a950b43494f3efd416830e66f` / 439138 bytes, [dossiê](../EXACT-TERMINAL-ITEM-HELPERS-1.0.10.md). SpearItem class SHA `37b96d1b7936408c0dbd92f0a0715af8400ef55d452c196527e912c3eaf10583`. Construtor D é ADD_VALUE ATTACK_DAMAGE +3D para Limestone Spear; ATTACK_SPEED −3D, ambos mainhand (não dano/velocidade finais). UseAnim.SPEAR, duração72000 ticks, use inicia se stack não damageable ou damageValue<maxDamage−1, senão pass. getPowerForTime: t=elapsed/20F, min(1F,(t*t+2F*t)/3F) sem clamp inferior no corpo. acHurtEnemy solicita hurtAndBreak(1,MAINHAND), mineBlock solicita 2 se destroySpeed!=0; custo efetivo em stack não damageable não inferido. Permanece parcial: projétil, impacto, damage type, engine, ownership e QA.
