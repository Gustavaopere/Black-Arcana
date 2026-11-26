# Fechamento candidato de alimentos, essências e interface de armadura — 1.0.10

**STATIC_CLOSURE_CANDIDATE_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Base main `9eeb5db432e5c9c552e8866214d34ec9fd20da73`. Modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Candidato a fechamento individual, nenhum novo selo nesta etapa.

## Escopo

Sete fichas candidatas: [Green Soylent](items/green-soylent.md), [Slam](items/slam.md), [Spelunkie](items/spelunkie.md), [Radiant Essence](items/radiant-essence.md), [Licowitch Radiant Essence](items/licowitch-radiant-essence.md), [Jelly Bean](items/jelly-bean.md), [KeybindUsingArmor](systems/keybind-using-armor.md).

Reuso de prova existente: [Food Builder](systems/food-builder.md) já fixa composição vanilla 1.21.1 e NeoForge 21.1.250, eventos Start/Tick/Finish, cópia de efeito e custo/recipiente referencial. [Foods](systems/foods.md) e seu selo nativo fixam SOYLENT_GREEN N3 m0.35 alwaysEat, SLAM N4 m0.5 DAMAGE_BOOST 400t p1, SPELUNKIE N2 m0.1 fast, JELLY_BEAN N1 m0.05 sem efeitos declarados. JellyBeanItem tem override próprio e não deve herdar inferência de alimentação vanilla sem prova. [Cloak](actions/cloak-darkness-incarnate.md) já documenta limites de autoridade do ArmorKeyMessage e bridge bidirecional; não constitui autorização para mutar pacote ou ativar habilidade de terceiros. O dispatcher e implementador precisam ser selados no recorte específico de suporte.

## Gates adicionais

[Probe nativo](../../../../docs/qa/alexscaves_1010_food_identity_keybind_probe.py): censo de 1555 classfiles por Fieldref exato de seis IDs em ACItemRegistry; janelas e projeções causais, referências tipadas e recursos por valores JSON exatos (não apenas filename). Reprojetar ACCompat food/nutrition/effect/potionEffects/potionColor/applyInstantenousEffect, handlers ArmorKeyMessage/ACNetwork/UpdateItemTagMessage, implementação DarknessArmorItem e quatro owners já pinados. O índice de ID e os caminhos em JSON são candidatos; tags indiretas, transforms, reflexão e consumidores por componentes podem escapar. Não declarar inexistência por ausência em censo delimitado.

[Referência de saúde/potion](../../../../docs/qa/alexscaves_1010_food_health_reference.py): Mojang 1.21.1 client SHA/mappings exatos, membros getHealth/setHealth/getMaxHealth/heal/addEffect, ItemUtils, PotionItem, PotionContents e MobEffect. Referência vanilla separada de NeoForge transformado; usar patches/provas adicionais se houver diferença pertinente. [Workflow](../../../../.github/workflows/alexscaves-1010-food-identity-keybind.yml) executa dois replays independentes por job. Confirmar resultado real e hashes antes de qualquer certificação, validar sete eixos por ficha e ledger. Sem alterações de índices, runtime ou Stage nesta PR preparatória.
