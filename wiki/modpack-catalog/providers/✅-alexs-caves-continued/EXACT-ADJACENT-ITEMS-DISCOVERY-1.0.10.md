# Descoberta agrupada de cinco classes de item — publisher 1.0.10

Estado: DISCOVERY_NOT_CERTIFIED. JAR físico SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c; 1.555 classes examinadas. Report 357381bd6a9ca6f8df9d79ef274552468033832664a40f59fc04ec2d76d99a6c, run 44671878664, job 136074491135. Manifesto preserva declarações, hashes, referências, ancestrais e recursos. Sem fechamento integral nem mutação.

| Classe | Métodos próprios com código | Disposição inicial |
|---|---:|---|
| AlwaysCombinableOnAnvil | 0 | Interface vazia, mas CommonEvents contém referência tipada; auditar teste de tipo, não presumir marcador inerte. Raygun e ShotGum implementam. |
| BiomeTreatItem | 8 | Item concreto; pai CaveInfoItem, associação CaveBiome, troca FOOD para BIOME_TREAT_DONE e consumidores Conversion Crucible. |
| BlockItemWithISTER | 2 | Delegação a BlockItemWithSupplier, inicialização de extensão de cliente. |
| BlockItemWithScaffolding | 3 | Contexto de colocação e distância literal 12, requere fronteira MetalScaffoldingBlock e world safety. |
| BlockItemWithSupplierLore | 2 | Tooltip traduzível a partir da identificação de bloco; receitas bootstrap a validar. |

A descoberta não certifica cada classe, nem os efeitos completos do Biome Treat, da bigorna ou da colocação de blocos. O próximo relatório cobre testes de tipo e dependências diretas; cada objeto recebe uma disposição individual após ordenação e validação.
