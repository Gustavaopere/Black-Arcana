# Apresentação e itens da escuridão — evidência do publisher 1.0.10

Alex's Caves Continued, arquivo publisher 8856293. JAR de 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O selo registra a varredura das 1.555 classes e o ABI das quatro classes em ordem alfabética. Os dois itens concretos somam 12 corpos próprios. O conjunto de armadura tem dois bindings da mesma classe. [Selo JSON](EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.json)

| Classe | Disposição e evidência |
|---|---|
| `CustomArmorPostRender` | Uma declaração abstrata, seis classes atribuíveis e uma chamada tipada no mixin da camada de armadura. A ficha mapeia modelo, slot, textura, foil e glow. [Ficha](systems/custom-armor-post-render.md) |
| `CustomTabBehavior` | Uma declaração abstrata, um consumidor e nenhum implementador nativo nas 1.555 classes. Disposição de apresentação, sem ficha adicional. |
| `DarkenedAppleItem` | Dois corpos, modelo, receita, avanço e propriedades alimentares. `finishUsingItem` amplia um efeito existente e entrega a conclusão ao pai. [Ficha](items/darkened-apple.md) |
| `DarknessArmorItem` | Dez corpos e duas factories. Material, receitas, guarda de luz, carga, seletor de portador, débito, efeito e caminhos visuais. [Hood](items/hood-of-darkness.md) · [Cloak](items/cloak-of-darkness.md) |

## CustomTabBehavior

`server.item.CustomTabBehavior.fillItemCategory(Lnet/minecraft/world/item/CreativeModeTab$Output;)V` é público e abstrato. SHA-256 da classe `6a77f884be2f7556f8c5085a534bd70968628c52d83687be2efde8237dba6cbe`. O único consumidor no censo tipado é `ACCreativeTabRegistry.add(Output,ItemLike)`. Em @1–4 o método testa o item recebido. O ramo true converte a interface em @8, chama `fillItemCategory` em @14 e retorna sem chamada de fallback. O outro ramo pede `Output.accept(ItemLike)` em @24. A interface não fornece um corpo padrão.

Os seis callbacks de abas para Magnetic Caves, Primordial Caves, Toxic Caves, Abyssal Chasm, Forlorn Hollows e Candy Cavity são `lambda$static$2/$6/$10/$14/$18/$24`. Usam o helper e também inserem as stacks vinculadas de Tablet e Codex diretamente via `Output.accept(ItemStack)` em @18 e @41. O censo fecha o despacho **publicado** desta interface no JAR, com chamadas presentes e nenhum emissor customizado nativo. Transformações e implementações externas continuam fora desse recorte. A API cuida da composição de abas criativas. Dano, alvo de combate, timing de cast e custos de perk são inaplicáveis.

## Referências do engine

O cliente oficial de Minecraft 1.21.1 tem SHA-256 `499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99`. O mapeamento oficial de mesmo release tem SHA-256 `140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec`. O replay destas referências usa os classfiles diretamente, sem iniciar o jogo. [Cliente](https://piston-data.mojang.com/v1/objects/30c73b1c5da787909b2f73340419fdf13b9def88/client.jar) · [Mapeamento](https://piston-data.mojang.com/v1/objects/2244b6f072256667bcd9a73df124d6c58de77992/client.txt)

- `ArmorItem$Type → csf$a`, SHA-256 `304d6345c9ed3d0cdeaea281ed1171b98505b266c04e2b25a023dec665197732`. No inicializador, `HELMET` usa ordinal 0 e `CHESTPLATE`, 1. As factories do publisher aplicam esses ordinais à defesa e à durabilidade do material. [Material](systems/armor-material.md)
- `MobEffectInstance → brz`, SHA-256 `a7453d5f04ab3b6b10d7a524b5f1c9d47a0a76c84a57c79c9b457429339b64bb`. O construtor curto usa `ambient=false`, mostra partículas e ícone e passa o efeito oculto como nulo no encadeamento. A duração infinita usa `-1`. A Maçã Obscura faz a soma inteira no próprio corpo antes de passar a duração ao construtor. [Efeito](effects/darkness-incarnate.md) · [Alimentação](systems/food-builder.md)

## Reprodução e limites

A [descoberta da PR #1135](EXACT-DARKNESS-PRESENTATION-1.0.10.md) permanece preservada como evidência anterior. O selo atual acrescenta contratos individuais verificáveis, com o renderizador como suporte técnico.

O workflow confere o SHA do publisher, reproduz assinaturas, corpos e consumidores tipados e confere os três bindings, os modelos, as receitas, os avanços, os nomes empacotados e as 11 texturas. O selo fixa ainda os oito manifestos anteriores usados como referência. SHA-256 do selo `3c4214f54fef7198463b6efa91b181d57a899c3c031ff1c5dd6bf1d44f520f9e`. [Verificador](../../../../docs/qa/alexscaves_1010_darkness_items_catalog.py) · [Workflow](../../../../.github/workflows/alexscaves-1010-darkness-items-catalog.yml)

As fichas cobrem identidade, comportamento, parâmetros, seleção, custos, integração e validação estática. A ação de Darkness Incarnate continua com seu próprio contrato. Aceitação ou sincronização de efeito, liquidação de inventário, autoridade de rede, mixins aplicados e aparência no cliente real têm QA pendente. `STATIC_TECHNICAL_CATALOG_ONLY`, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider aberto. São quatro contratos estáticos, incluindo as três fichas de item já publicadas, uma disposição de apresentação e zero raízes adicionais.
