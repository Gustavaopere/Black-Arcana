# Gazing Pearl — descoberta causal SHA-exata do publisher 1.0.10

**Estado:** ⚠️ parcial, STATIC_DISCOVERY_ONLY, NO_MUTATION, mutating_hook=NOT_VERIFIED, physical_qa=NOT_TESTED, provider_universe_closed=false. Uma ficha individual em [items/gazing-pearl.md](items/gazing-pearl.md), nenhum novo cast ou magia.

## Identidade, artefato e reprodução

Modlist sibling: alexscaves-1.0.10-neoforge+1.21.1.jar (Minecraft 1.21.1/NeoForge/Java 21), SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570. O publisher realmente lido tem **75.279.314 bytes**, SHA-256 **36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c**, 1.555 classfiles. Não foi obtido dump atualizado da instalação. Classfile da GazingPearlItem SHA-256 2519bc5aed494deccc0423053ea42904314511094b29cd1e4025cc65a08a5a07; DeepOneReaction SHA-256 5898cd4286885ad85e92065f68bff883131e921af295b781b806e076ff1e54dc.

A [sonda read-only](../../../../docs/qa/alexscaves_1010_gazing_pearl_discovery.py) e o [workflow](../../../../.github/workflows/alexscaves-1010-gazing-pearl-discovery.yml) inspecionam o JAR SHA-exato, todas as instruções locais dos 5+9 métodos, hierarquia, censo de consumidores tipados e JSON filename-matched. [Manifesto compacto](EXACT-GAZING-PEARL-DISCOVERY-1.0.10.json) registra descritores, digests e limites; [checker fail-closed](../../../../docs/qa/alexscaves_1010_gazing_pearl_static_checks.py) compara a prova reproduzível. Primeiro run [44936198921](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44936198921), job 136943226304 PASS, report SHA-256 **d73959ca968bd23e57240d2fb3943e400362af9da92940af7343e93f47ff01c5**; artefato 14719307762, ZIP SHA-256 99adb9c94f95711e5cac1a80c8156a5476e467ddf5761e222ef2ec5a8592ce02, expiração 05/12/2026. O novo checker ainda depende do gate final de CI desta PR.

## Causalidade e JVM

| Método | Instruções | Localizadores e efeitos solicitados |
|---|---:|---|
| GazingPearlItem.<init> | 10 | stacksTo(1); Rarity.UNCOMMON |
| GazingPearlItem.acInventoryTick | 46 | isClientSide @1/4; LastReputationTimestamp @15; getLong @17; <=0 @26; gameTime @30; 100L @36; comparação delta>100 @40; ACWorldData.get @44; null @51; putLong @62, putBoolean @70, entity.getUUID @80, getDeepOneReputation @83, putInt @86, setTag @92 |
| GazingPearlItem.appendHoverText | 38 | HasReputation @13/18; Reputation @23/25; fromReputation @32; Locale.ROOT @42; translatable @58; cinza/itálico @61/67; super @85 |
| GazingPearlItem.getPearlColor | 73 | Matiz com reputação `float(100-R)/200F`, sem flag `(timeMillis%10000L)/10000F`; saturação `0.7F+0.3F*((float)(sin((double)((float)timeMillis/4000F))+1)*0.5F)`; brilho `1F`; HSBtoRGB @63/@110; render efetivo não testado |
| GazingPearlItem.shouldCauseReequipAnimation | 16 | ACItemRegistry.GAZING_PEARL @1/19; ItemStack.is @12/30, guardas @15/33 |
| DeepOneReaction.fromReputation | 17 | limites inteiros −10,10,30 e categorias AGGRESSIVE,STALKING,NEUTRAL,HELPFUL |
| DeepOneReaction.<clinit> | 35 | quatro categorias com dados de distância da IA (não raio do item) |
| DeepOneReaction.validPlayer | 31 | STALKING, AGGRESSIVE, HELPFUL, Y diferenciado por 15D, água/bolha; não é usado diretamente pelo callback da pérola |
| DeepOneReaction.getMinDistance/getMaxDistance | 3 cada | leitura dos campos de distância da enum, não targeting do item |

Os demais métodos do enum (<init>, $values, values, valueOf) constam no manifesto. Há três owners consumidores tipados da GazingPearlItem (ClientProxy, ACItemRegistry, própria classe) e sete de DeepOneReaction (AI e mobs Deep One, classe enum e pérola). Não transferir o contrato de reação completa dos mobs para a pérola.

**Classificação por Reputation inteiro:** até −10 AGGRESSIVE; −9..10 STALKING; 11..30 NEUTRAL; 31 ou maior HELPFUL. **World data** é a autoridade; a pérola apenas solicita leitura e salva um snapshot no próprio item. A escrita do timestamp depende de world data não nulo. Atualizações são server-side com delta de **gameTime >100**, não relógio civil. O getter de cor usa relógio civil e representa uma decisão de apresentação. O dispatcher ACTickingItem já possui [contrato estático independente](systems/ticking-item.md).

O censo filename-matched encontrou modelo de Gazing Pearl e receita de conversão **Gazing Pearl + Marine Snow → Pearl**; hashes/JSON no manifesto. A receita não prova aquisição da pérola. Fonte de revisão 1.1.1 do publisher é auxiliar apenas; valores alegados vêm do JAR 1.0.10.

## Contrato algébrico da cor — recorte SHA-exato da versão 1.0.10

**Novo fechamento apenas do método local:** `GazingPearlItem.getPearlColor:(Lnet/minecraft/world/item/ItemStack;)I` — access `public static`, **73 instruções**, Code SHA-256 `0b2790fa924d0e99c0acf32b85906e4b9ea72ca3a8807ec0c14419e33e400630`, instruction SHA-256 `e4bffbeaf3e572d06916a5e34bb84399f8114cf52c203cda0d2d67ebfac6c6cc`. Relatório `report.json` **301.601 bytes**, SHA-256 `d73959ca968bd23e57240d2fb3943e400362af9da92940af7343e93f47ff01c5`, [artifact #14719307762](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44936198921/artifacts/14719307762). O [verificador](../../../../docs/qa/alexscaves_1010_gazing_pearl_color_checks.py) confronta as duas trajetórias de controle, constantes, descritor, Code SHA e 49 pivôs/offsets e executa dois testes negativos de adulteração. O positivo e os negativos passaram localmente no relatório SHA-exato; a CI da nova HEAD deve reproduzi-los.

Abaixo, `F(x)` representa arredondamento para **float IEEE 754 de 32 bits** e as operações são efetuadas na ordem JVM, com arredondamentos intermediários:

- **Se tag não nula e `HasReputation=true`:** `R = ACCompat.getInt(tag,"Reputation")`; `H = F(F(100-R)/200.0F)`, com `100-R` em inteiros JVM antes de `i2f`; `p=F(F(t)/4000.0F)`, `q=F((sin((double)p)+1.0d))*0.5F`; `S=F(0.7F+F(0.3F*q))`; `B=1.0F`; `Color.HSBtoRGB(H,S,B)` @63.
- **Se não há informação de reputação:** `H=F(F((t1 % 10000L))/10000.0F)` @71–81; `S` usa a mesma equação acima, mas com **outra chamada a `System.currentTimeMillis`** em @83 (`t2`), seguida de `Color.HSBtoRGB` @110. O método não captura um único timestamp para ambos os cálculos.
- **Sem clamp próprio ou correção de matiz:** antes de `HSBtoRGB`, os únicos guards são `ifnull @6 -> 71` e `ifeq @15 -> 71`. A semântica interna de `java.awt.Color.HSBtoRGB` e a cor efetivamente renderizada pelo cliente ficam fora do contrato de bytecode do mod.
- **Precisão temporal:** `l2f @21/@86` ocorre antes do `fdiv 4000.0F`. Para `t=1795305600000 ms` (2026-11-22 00:00 UTC), uma verificação numérica em Java 21 da expressão `Math.nextUp((float)t)-(float)t` retorna **131072 ms** (≈2,18 minutos). Logo, a fase de seno pode permanecer invariável por múltiplos frames e mudar discretamente mesmo com relógio contínuo. Isso é **inferência matemática respaldada pela sequência de bytecode**, não teste visual, nem garantia do comportamento do renderer.
- **Segurança e perks:** o método é estático/de apresentação e não gera XP, dano, mana, cooldown, alteração de reputação ou hook mutador. É indevido transferir-lhe autoridade de `ACWorldData`, criar Mastery por leitura ou mutar cor como se alterasse a reação dos Deep Ones. Preservar `NO_MUTATION`.

**Status:** esta prova fecha somente a interpretação algébrica do método `getPearlColor`; `GazingPearlItem` integral ainda **⚠️ parcial**, `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; world data, consumer client efetivo e engine permanecem fora do gate.

## Integração, riscos e próximos gates

N/A para dano próprio, projétil, AOE, custo de mana, cooldown ou cast. Snapshot por UUID da entidade recebida não equivale a owner persistente da pérola; world data, clock rewind, reload, fallback de client e transferências de inventário exigem estudo. O método validPlayer é da IA e não concede ataque/defesa ao portador. Sem hook por usuário verificado, não modificar Reputation/HasReputation ou cadência do dispatcher para implementar perks. Mastery não pode contar tooltip/tempo como sucesso de magia. Black Arcana mantém seu runtime; RPG Skill Tree é provider de progressão mediante contratos reais.

CI de manifesto, build e índices, referência engine, world data completo, render client, modpack instalado e QA física permanecem separadamente pendentes. Não copiar código/assets de terceiro. **NO_MUTATION/fail-closed**.
