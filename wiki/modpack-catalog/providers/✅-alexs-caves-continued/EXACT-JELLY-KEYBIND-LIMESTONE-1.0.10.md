# Jelly Bean, KeybindUsingArmor e Limestone Spear — descoberta binária 1.0.10

**DISCOVERY_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Sem novos certificados, fichas individuais promovidas, raízes semânticas, hook ou fechamento de provider. Este é um dossiê auxiliar de coleta, não substitui as fichas individuais após interpretação.

Autoridade: publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, Minecraft 1.21.1, Java 21. Modlist sibling #019; NeoForge 21.1.250 documental, sem novo dump físico.

## Escopo e evidência reutilizada

O inventário físico [INTEGRATION-SCOPE-INVENTORY-1.0.10.json](INTEGRATION-SCOPE-INVENTORY-1.0.10.json) identifica as três classes em ordem alfabética após InkBombItem. Galena, Gazing Pearl, Gingerbread/Hazmat, Holocoder, Hot Chocolate e Ink Bomb têm dossiês individuais existentes; o prefixo histórico não é promovido automaticamente. O [contrato de registro](systems/item-registry.md) comprova:

| Objeto / símbolo | Identidade declarada | Factory e Code SHA-256 |
|---|---|---|
| JellyBeanItem | `alexscaves:jelly_bean` | `lambda$static$198` / `546da6af37d6cc4834693c322a2cd13c1852123744a3bd55006b0bee3fd5ed63` |
| KeybindUsingArmor | Classe no censo, sem assumir registry ou habilidade independente | N/A até investigar implementação/consumidores |
| LimestoneSpearItem | `alexscaves:limestone_spear` | `lambda$static$45` / `33b072bd23f120bb5040ee52db21241e05a6589692f0a9d9c95565bf8a70ccef` |

A [sonda read-only](../../../../docs/qa/alexscaves_1010_jelly_keybind_limestone_probe.py) exige JAR SHA-exato e roster de 1.555 classfiles, classfile de ACItemRegistry e os dois Code hashes prévios; exige new tipado das factories. Projeta todas as declarações dos três owners, separa corpos executáveis de abstratos, e censita referências tipadas, implementadores/subclasses diretos e janelas locais nos consumidores. A seleção de recursos JSON por nome é apenas recorte, não grafo completo de tags, recipes, loot ou assets. O [workflow](../../../../.github/workflows/alexscaves-1010-jelly-keybind-limestone.yml) exige duas saídas byte-idênticas; interpretar resultados e selar digest antes de qualquer certificado.

## Pendências

Nenhuma fórmula, dano, atributo, custo, tecla, ação, estado ou entidade foi presumida a partir do nome. Após a coleta, classificar interface/objeto, inspecionar corpos herdados e callbacks/eventos downstream aplicáveis e criar fichas individuais com os sete eixos. Não somar classes, factories e consumidores como magias; não avançar a Stage numerada.

## Resultado observado — primeiro replay exato

[Run 45651673635 / job 139337522318](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45651673635/job/139337522318), HEAD `fcdbbf908163c7e30700987e65ea5f8a5cdac0d8`: seis checks de escopo, dois relatórios idênticos de **186.937 bytes**, SHA-256 `61a6010adbe0c6f41968a6ffc8f85e8c4c6e013175007f6be93280d3cf2da0ed`. Os três alvos têm 12 declarações (11 Code e uma abstrata), mais duas factories Code. Sete owners com referências tipadas/implementação direta e oito JSONs no recorte por filename. Esta revisão fixa também tamanho e digest. O selo não autoriza execução de efeitos nem representa todos os recursos associados.

### JellyBeanItem — `alexscaves:jelly_bean`

Classfile SHA-256 `9842c28cd2eff05621a23be37ce5917ca88a19bf0bd99f0da9b5a5cc62a4355f`, superclasse PotionItem, nove corpos. O construtor (10 instruções; Code `7c9221640edb8c32051a9de28e6c771fb5215a7278aca4069423fc52dfd1bff2`) usa ACFoods.JELLY_BEAN @8, ACFoodBuilder.food @11, stacksTo(16) @16. getUseDuration (2; `587ee4123eea46a1985d4a111f62e7f950c2e261b98176356a0c11e7ad0d0b92`) retorna 16 ticks. getDrinkingSound (2; `ccff6406fe1f555f5c48f689548dfb8df57f2dc6c393904297a757fc7dac082e`) retorna GENERIC_EAT.

- getBeanColor (25; `7cbfe97883569b6ff7f89879403fcbe9fefcb3e6e104187b4da27d7ea4be9b36`): tag não nula e Rainbow verdadeiro, hue=(currentTimeMillis%4000)/4000F, saturation=1, brightness=0,8; senão potionColor @42. É uma fórmula de apresentação, não duração ou potência. ClientProxy.lambda$onItemColors$22 chama @9.
- finishUsingItem (72; `285ba91b3197410e4ea9e455598f972ce7a7c2be1d1febc8aa9702959b493e18`): extrai Player quando aplicável, CONSUME_ITEM para ServerPlayer @34; fora do cliente lê potionEffects @45 e percorre instâncias. Efeito instantâneo pede ACCompat.applyInstantenousEffect @105 com level, duas referências Player (possivelmente null), consumidor, amplificador da instância e fator 1D; não instantâneo copia a instância @118 e pede addEffect @121, descartando retorno. Player recebe ITEM_USED @142 e shrink(1) se !instabuild @158; sem Player, não há shrink no corpo. EAT @165, sem chamada explícita ao ancestral finishUsingItem no recorte. Não inferir nutrição efetivamente consumida, durações universais, efeito garantido ou reembolso: depende de componentes e engine. Alvo direto é a entidade consumidora; sem projétil/AOE ofensiva própria demonstrada.
- onUseTick (134; `a835f3b8b8771f424990ef4253499cbcf67db4945466edb84bae66094a66b621`): constrói vetores com aleatoriedade e rotações da entidade, soma posição/eyeY; ServerLevel solicita sendParticles @233 com count=1 e rota alternativa Level.addParticle @290. Partícula JELLY_BEAN_EAT, não hit de combate.
- appendHoverText (222; `334427b5a40bc2d8dd270d17c5afa82109544fc93d87fe458162f9588d1de48f`): lista efeitos da stack e seus modificadores conforme amplificador, formata duração quando !endsWithin(20), multiplica por 100 para operações ADD_MULTIPLIED_BASE/TOTAL, distingue valores positivos/negativos. Tooltip não liquida atributos. Dois getDescriptionId delegam à descrição, não certificam tradução.
- JSON model generated; advancement inventory_changed exige item jelly_bean; ícone com Rainbow=1 é metadado de display e não gate de obtenção do componente. Recurso de partícula vazio. Pendente: produtores de POTION_CONTENTS/Rainbow, ACFoods e ponte efetiva de consumo/PotionItem, codecs e aplicação de efeitos, custos e aceitação física.

### KeybindUsingArmor — contrato de interface candidato

Classfile SHA-256 `6ed129bf051acf5b551e2e96ed898c818304fe99e0298fb9f0a5ebf226bc3b86`, uma declaração sem Code: onKeyPacket(Entity,ItemStack,int)V. O censo observou DarknessArmorItem como implementador direto e ArmorKeyMessage como consumidor. Janelas de ArmorKeyMessage.lambda$handle$0 (Code `0641114dc3b38ccf47d158b49226b2d4afe39ab7bf8d104faa58686c052f0e60`): Player.getItemBySlot @80 → getItem @87 → instanceof @94 / checkcast @102 → onKeyPacket @116 com Entity local 3, stack local 6 e type:I do pacote. Não comprova seleção/autorização inicial da entidade, limites do slot/type, thread ou lado, callback executado nem segurança. Reutilizar dossiês de DarknessArmorItem apenas no escopo demonstrado, inspecionar todos os corpos de ArmorKeyMessage e implementador antes de classificar disposição. Não contar interface como cast independente.

### LimestoneSpearItem — `alexscaves:limestone_spear`

Classfile SHA-256 `1f068faf0b5829d4c63ab56a09a6c9fc2de6b57c030ae58c6d3211ffacd86510`, dois corpos próprios, ancestral SpearItem. Factory (9) solicita stacksTo(16); construtor (5; `31ebbbfa831a75d4ad1f5e53246edce4d27539614fbe5160ea47d5006d5d39d9`) passa 3D à superclasse; significado depende da auditoria do ancestral, não presumir dano final.

releaseUsing (76; `6f034115f35bc9a3586a7f76ffc78ce4be38241ffaf23e418d6c1b7d13559037`): exige Player, calcula elapsed=getUseDuration−remaining e power=getPowerForTime(elapsed); prossegue se power>0,1D. Cria LimestoneSpearEntity(Level,LivingEntity,ItemStack) @50; shootFromRotation @76 usa XRot/YRot, offset 0, velocidade argumento 2,5×power, inaccuracy 1. Se instabuild solicita pickup=CREATIVE_ONLY; addFreshEntity @101, descarte do retorno precisa ser considerado no settlement. Som LIMESTONE_SPEAR_THROW / PLAYERS volume/pitch 1; shrink(1) fora de instabuild @144 e ITEM_USED @156. Sem guarda explícita de lado observada nesse corpo; não inferir spawn aceito nem débito efetivo. Receitas: 3 limestone e 2 posições de tag rods/wooden produzem 4 itens; modelo throwing=1 e arquivo Better Combat parent bettercombat:spear são metadados, não integração física. Pendente: significado do argumento 3D, fórmula de power e duration herdadas, entidade/projétil, dano/tipo, alcance, collision/pickup, interação com encantamentos, authority e custos.

Todas as conclusões acima são de descoberta. Nenhum certificado, ficha promovida, hook, raiz, execução física ou índice acrescido nesta revisão. Próximo passo: fichas individuais após a reconciliação das PRs que alteram ledger/índices.
