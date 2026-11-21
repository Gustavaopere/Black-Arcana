# Gazing Pearl — descoberta causal SHA-exata do publisher 1.0.10

**Estado:** ⚠️ parcial, STATIC_DISCOVERY_ONLY, NO_MUTATION, mutating_hook=NOT_VERIFIED, physical_qa=NOT_TESTED, provider_universe_closed=false. Uma ficha individual em [items/gazing-pearl.md](items/gazing-pearl.md), nenhum novo cast ou magia.

## Identidade, artefato e reprodução

Modlist sibling: alexscaves-1.0.10-neoforge+1.21.1.jar (Minecraft 1.21.1/NeoForge/Java 21), SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570. O publisher realmente lido tem **75.279.314 bytes**, SHA-256 **36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c**, 1.555 classfiles. Não foi obtido dump atualizado da instalação. Classfile da GazingPearlItem SHA-256 2519bc5aed494deccc0423053ea42904314511094b29cd1e4025cc65a08a5a07; DeepOneReaction SHA-256 5898cd4286885ad85e92065f68bff883131e921af295b781b806e076ff1e54dc.

A [sonda read-only](../../../../docs/qa/alexscaves_1010_gazing_pearl_discovery.py) e o [workflow](../../../../.github/workflows/alexscaves-1010-gazing-pearl-discovery.yml) inspecionam o JAR SHA-exato, todas as instruções locais dos 5+9 métodos, hierarquia, censo de consumidores tipados e JSON filename-matched. [Manifesto compacto](EXACT-GAZING-PEARL-DISCOVERY-1.0.10.json) registra descritores, digests e limites; [checker fail-closed](../../../../docs/qa/alexscaves_1010_gazing_pearl_static_checks.py) compara a prova reproduzível. Primeiro run [44936198921](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44936198921), job 136943226304 PASS, report SHA-256 **d73959ca968bd23e57240d2fb3943e400362af9da92940af7343e93f47ff01c5**; artefato 14719307762, ZIP SHA-256 99adb9c94f95711e5cac1a80c8156a5476e467ddf5761e222ef2ec5a8592ce02, expiração 05/12/2026. O novo checker ainda depende do gate final de CI desta PR.

## Causalidade e JVM

| Método | Instruções | Localizadores e efeitos solicitados |
|---|---:|---|
| GazingPearlItem.<init> | 10 | stacksTo(1); Rarity.UNCOMMON |
| GazingPearlItem.acInventoryTick | 46 | isClientSide @1/4; LastReputationTimestamp @15; getLong @17; <=0 @26; gameTime @30; 100L @36; comparação delta>100 @40; ACWorldData.get @44; null @51; putLong @62, putBoolean @70, entity.getUUID @80, getDeepOneReputation @83, putInt @86, setTag @92 |
| GazingPearlItem.appendHoverText | 38 | HasReputation @13/18; Reputation @23/25; fromReputation @32; Locale.ROOT @42; translatable @58; cinza/itálico @61/67; super @85 |
| GazingPearlItem.getPearlColor | 73 | HasReputation @10/15; currentTimeMillis @18/71/83; sin @26/91; HSBtoRGB @63/110; constantes 4000,10000,100,200,0.3,0.5,0.7; resultado visual sem contrato RGB integral |
| GazingPearlItem.shouldCauseReequipAnimation | 16 | ACItemRegistry.GAZING_PEARL @1/19; ItemStack.is @12/30, guardas @15/33 |
| DeepOneReaction.fromReputation | 17 | limites inteiros −10,10,30 e categorias AGGRESSIVE,STALKING,NEUTRAL,HELPFUL |
| DeepOneReaction.<clinit> | 35 | quatro categorias com dados de distância da IA (não raio do item) |
| DeepOneReaction.validPlayer | 31 | STALKING, AGGRESSIVE, HELPFUL, Y diferenciado por 15D, água/bolha; não é usado diretamente pelo callback da pérola |
| DeepOneReaction.getMinDistance/getMaxDistance | 3 cada | leitura dos campos de distância da enum, não targeting do item |

Os demais métodos do enum (<init>, $values, values, valueOf) constam no manifesto. Há três owners consumidores tipados da GazingPearlItem (ClientProxy, ACItemRegistry, própria classe) e sete de DeepOneReaction (AI e mobs Deep One, classe enum e pérola). Não transferir o contrato de reação completa dos mobs para a pérola.

**Classificação por Reputation inteiro:** até −10 AGGRESSIVE; −9..10 STALKING; 11..30 NEUTRAL; 31 ou maior HELPFUL. **World data** é a autoridade; a pérola apenas solicita leitura e salva um snapshot no próprio item. A escrita do timestamp depende de world data não nulo. Atualizações são server-side com delta de **gameTime >100**, não relógio civil. O getter de cor usa relógio civil e representa uma decisão de apresentação. O dispatcher ACTickingItem já possui [contrato estático independente](systems/ticking-item.md).

O censo filename-matched encontrou modelo de Gazing Pearl e receita de conversão **Gazing Pearl + Marine Snow → Pearl**; hashes/JSON no manifesto. A receita não prova aquisição da pérola. Fonte de revisão 1.1.1 do publisher é auxiliar apenas; valores alegados vêm do JAR 1.0.10.

## Integração, riscos e próximos gates

N/A para dano próprio, projétil, AOE, custo de mana, cooldown ou cast. Snapshot por UUID da entidade recebida não equivale a owner persistente da pérola; world data, clock rewind, reload, fallback de client e transferências de inventário exigem estudo. O método validPlayer é da IA e não concede ataque/defesa ao portador. Sem hook por usuário verificado, não modificar Reputation/HasReputation ou cadência do dispatcher para implementar perks. Mastery não pode contar tooltip/tempo como sucesso de magia. Black Arcana mantém seu runtime; RPG Skill Tree é provider de progressão mediante contratos reais.

CI de manifesto, build e índices, referência engine, world data completo, render client, modpack instalado e QA física permanecem separadamente pendentes. Não copiar código/assets de terceiro. **NO_MUTATION/fail-closed**.
