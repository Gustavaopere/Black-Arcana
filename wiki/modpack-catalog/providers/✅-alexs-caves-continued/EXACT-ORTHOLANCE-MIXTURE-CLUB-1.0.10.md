# Ortholance, PrehistoricMixtureItem e Primitive Club — próximo recorte de classes externas 1.0.10

**DISCOVERY_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Base canônica `f3f48196a0853fe51cefd0dd5ba462b354773dc2`. Autoridade documental: modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Nova coleta pendente; sem novo dump físico.

## Reuso e reconciliação

OccultGemItem é a próxima classe após MothDustItem no inventário; já mapeada à [ficha certificada Occult Gem](actions/occult-gem-beholder-observation.md). Não duplicar objeto, raiz, certificado ou runtime. A PR #1230 permanece independente; seu contador e a fila consolidada dependem da aprovação da HEAD corrigida.

As próximas três classes representam cinco factories registradas, não cinco novas magias. Já há provas de modificadores de Ortholance e Primitive Club e de ACFoods. O objetivo é fechar o recorte do objeto e não repetir certificações dos encantamentos.

| ID | Classe | Factory | Code SHA-256 |
|---|---|---|---|
| `alexscaves:ortholance` | `OrtholanceItem` | `lambda$static$110` | `8b877c684803c7473ec03238d4f62a31f2125d8b896b31340e2bd3894d3db0da` |
| `alexscaves:primitive_club` | `PrimitiveClubItem` | `lambda$static$40` | `f88517fec12d13fcfc61890e09e7310f0a000ab35eea36adc82ddd7af3bab032` |
| `alexscaves:primordial_soup` | `PrehistoricMixtureItem` | `lambda$static$37` | `5814d536831c0df71d18745af3571e2420a7881043c4011999201da8e21dc26e` |
| `alexscaves:seething_stew` | `PrehistoricMixtureItem` | `lambda$static$36` | `0422c42f5408367b8987440476afca13be6ae1bd001f429a8789cf3ba7d57b60` |
| `alexscaves:serene_salad` | `PrehistoricMixtureItem` | `lambda$static$35` | `06fad7a5b6e47e921cd25b041a9caad976b82bd0671c9f2c5021e8b4076e7c0e` |

Fonte: [registro](systems/item-registry.md).

## Evidências existentes reaproveitáveis

- Ortholance: [Flinging](enchantments/flinging.md), [Tsunami](enchantments/tsunami.md), [Second Wave](enchantments/second-wave.md), [Sea Swing](enchantments/sea-swing.md). Classfile SHA-256 `996b208a60f2c26c275e60e5d0e3a2fd0090cfb0ba1687907cac242de9a17d09`. O contrato Tsunami documenta factory durabilidade 340, raridade UNCOMMON, duração de uso 72000 ticks e gate damageValue>=maxDamage−1. Flinging audita integralmente releaseUsing, mas isso não fecha a arma inteira; mapear todos os demais corpos, custos, atributos, componentes, eventos, projéteis/ondas e consumidores relevantes.
- Primitive Club: [Swiftwood](enchantments/swiftwood.md), [Dazing Sweep](enchantments/dazing-sweep.md), [Bonking](enchantments/bonking.md). Classfile SHA-256 `92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac`. Durabilidade 120, modificador ATTACK_DAMAGE +8D e ATTACK_SPEED min(0F,−3.75F+0.15F×L), L limitado a 0..3 no recorte Swiftwood, MAINHAND. O manifesto Bonking cobre os 16 corpos / 381 instruções; aproveitar hashes e contratos prévios, examinar pontos de ataque/swing/desgaste e settlement ainda não fechados para a arma.
- PrehistoricMixtureItem: [Foods](systems/foods.md) comprova perfis ACFoods, não liquidação do item. PRIMORDIAL_SOUP N=6, m=0.6, DIG_SPEED 800 ticks p=1; SEETHING_STEW N=6, m=0.6, RAGE 2200 ticks p=1; SERENE_SALAD N=5, m=0.35, sem efeito declarado pelo builder. Os três têm bowl. Investigar callbacks do item, gatilhos, efeitos de status e consumo, componentes, retorno de recipiente, regras de target, aquisição e modificadores sem inferir efeitos do nome.

## Reprodução proposta e limites

[Auditor](../../../../docs/qa/alexscaves_1010_ortholance_mixture_club_probe.py) reutiliza ClassReader e projeção read-only integrados. Exige SHA-exato, roster de 1555 classes, hashes prévios do registro e das cinco factories e dois classfiles previamente auditados. Projeta todos os corpos próprios (não só os do encantamento), consumidores tipados diretos, recursos JSON por nome. [Workflow](../../../../.github/workflows/alexscaves-1010-ortholance-mixture-club.yml) exige dois relatórios byte-idênticos. Hash/tamanho do novo resultado ainda não observados. A projeção não é prova integral dos consumidores herdados ou efetivos; recorte de filename não fecha recursos transitivos. Nenhum índice, ledger, ficha, raiz, hook ou Stage alterado. Após a coleta, comparar os resultados com os manifestos anteriores e fechar lacunas individuais antes de promover qualquer contrato. NO_MUTATION.

## Resultado binário observado

[Run 45745854148 / job 139661611420](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45745854148/job/139661611420), HEAD `41b0080f4a161c9fa82fdb3dc5ed57c3b77f0d82`: oito checks, 38 declarações projetadas (13 Ortholance, 4 PrehistoricMixture, 16 Club e 5 factories), quatro owners com referências tipadas e 24 JSONs por filename. Dois relatórios byte-idênticos, 384.061 bytes, SHA-256 `4c9aefbfedf99868ae394f1a77dfaaa85cd3c5e8b6d1554b44ed41a902d569b1`. A nova HEAD sela tamanho/digest e precisa reproduzi-los.

- [Ortholance](equipment/ortholance.md)
- [Primitive Club](equipment/primitive-club.md)
- [Primordial Soup](items/primordial-soup.md)
- [Seething Stew](items/seething-stew.md)
- [Serene Salad](items/serene-salad.md)

A #1230 consolida a coleta da #1231 sem duplicar histórico; cinco fichas novas parciais. 137/154 contratos no recorte proposto; 55/81 classes com disposição documentada. Não promover contratos, roots, hooks ou QA. Próximo: reconciliar PrimordialArmorItem antes de QuarrySmasherItem.
