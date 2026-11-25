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
