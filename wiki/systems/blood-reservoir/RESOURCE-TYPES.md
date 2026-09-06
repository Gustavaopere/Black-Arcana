# Tipos de Recurso — Fronteiras Canônicas

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO`

## Tipos

### Sangue (`BLOOD`)
Recurso fisiológico hemático. É o único recurso que satisfaz custos que exigem sangue.

### Energia Vital (`VITAL_ENERGY`)
Representa força vital/vida abstrata quando uma mecânica futura explicitamente a usar. Não é sangue e não preenche reservatórios hemáticos.

### Mana (`MANA`)
Recurso arcano normal do provider. A nova disciplina hemática não deve consumi-lo.

### Soul Energy (`SOUL_ENERGY`)
Recurso do Goety. Mantém authority do Goety e não se converte automaticamente em sangue.

### Spirit (`SPIRIT`)
Recurso/essência do Malum ou outros providers espirituais. Mantém authority do provider e não se converte automaticamente em sangue.

### Alma (`SOUL`)
Identidade/recurso espiritual conceitualmente distinto de sangue. Qualquer uso depende de hook/provider seguro.

## Exemplos

- jogador/humanoide biológico: pode ser `BLOOD`, sujeito a classificação final;
- animal biológico: pode ser `BLOOD`;
- vampiro: pode possuir subtipo de sangue alterado, não deve ser assumido idêntico ao sangue comum;
- Iron Golem: `NO_BLOOD`; vida/energia vital não equivale a sangue;
- constructo mágico: `NO_BLOOD` por padrão até provider provar recurso hemático;
- máquina: `NO_BLOOD`.

## Regra fail-closed

`UNKNOWN` nunca é tratado como `BLOOD` por conveniência.
