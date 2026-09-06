# Magia Infernal — Catálogo candidato

## Estado

`CONCEITO / PESQUISA — DEDUP DE IGNIS/CATACLYSM/GOETY OBRIGATÓRIO`

A escola Infernal só cria efeitos onde houver delta real em relação a Fire/Ignis/Soulfire já instalado.

## Família 1 — Lava Infernal / infraestrutura

### Vínculo da Caldeira Infernal
Liga caster a uma estrutura válida no Nether e expõe `INFERNAL_RESERVOIR` como fonte para spells autorizados. Não transporta fluido; transporta autorização/consulta de recurso dentro das regras de dimensão.

### Sifão da Fenda
Transfere Lava Infernal entre depósitos válidos no Nether. Não funciona através de portal, inventory portátil ou dimensão diferente.

### Sobrecarga da Fornalha
Consome grande volume do reservatório para amplificar um único cast, aumentando backlash/heat e aplicando limites de infraestrutura.

## Família 2 — Hellfire de delta real

### Maré Rubra
Onda baixa de Lava/Hellfire mágica que avança por frontier bounded. Não deve duplicar Incineration, Black Pyre ou vanilla lava spread. O diferencial precisa ser control de terreno/pressão térmica e consumo de mB.

### Sangria de Magma
Fissura linear que abre pulsos de Hellfire por uma curta janela. Deve ser comparada contra Tectonic Tremble, Incineration e outros ground spells antes de aprovação.

### Núcleo de Ruína
Projétil/seed que cria zona curta de pressão térmica + magical damage, sem ser outro fireball. Precisa de diferença clara de delivery e persistent-zone semantics.

### Correntes da Fossa
Binding infernal que prende criatura elegível e pode puxá-la toward anchor. Deduplicar contra Arcane Shackle, Goety chains e Order containment.

### Marca da Fornalha
Debuff que registra exposição infernal e altera apenas efeitos HELLFIRE aprovados. Não é vulnerabilidade universal a Fire.

### Pele de Escória
Defesa que converte parte de dano recebido em heat/backlash e reduz categorias específicas. Deduplicar contra Bedrock Skin, fire resistance e Ignis buffs.

## Família 3 — Pactos e contratos

### Pacto de Cinzas
Contrato persistente com benefício e custo explícitos. O pacto pode desbloquear receitas/spells, mas não cria mana/Lava Infernal.

### Dívida Infernal
Marca contratual contabilizada por ledger bounded. Certos spells podem gastar ou acumular dívida; default/ruptura produz consequência definida. Não usar punição irreversível sem counterplay.

### Gaiola de Nome Verdadeiro
Ritual compartilhado com Witchcraft/Binding para entidade infernal reconhecida. A escola visual/host depende do método de obtenção.

### Retorno Infernal
Portal de emergência que usa `ALTERED_BLOOD` demoníaco ou outro token infernal como chave. Não converte esse item/recurso em Lava Infernal.

## Família 4 — Miracle-tier infernal

### Erupção do Abismo
Ultimate de alto consumo em mB que cria uma erupção bounded e telegraphed. Requer infraestrutura no Nether ou link permitido; sem fonte válida, falha fechado.

### Domínio da Fornalha
Forbidden Domain com regras HELLFIRE específicas, por exemplo heat buildup e redução de eficiência de certas ações. Nenhuma regra global do servidor é alterada.

### Colapso da Caldeira
Spell/ritual de desespero que queima uma fração grande do estoque para um efeito devastador, podendo danificar temporariamente a infraestrutura própria. Claims/other-player infrastructure nunca podem ser destruídos sem authority.

## Provider-native que bloqueia duplicatas

Cataclysm: Spellbooks baseline público já cobre pelo menos:

- Incineration;
- Infernal Strike;
- Hellish Blade;
- Bone Storm;
- Bone Pierce;
- Ashen Breath;
- Abyss Fireball;
- Tectonic Tremble;
- Conjure Ignited Reinforcement.

A build instalada 1.1.13 é mais nova que o source público 1.1.11, então valores e lista final devem ser extraídos do JAR atual antes de qualquer decisão de overlap.

Também auditar:

- Cataclysm: Ignis Soulfires;
- Ignis Soulfires: Spellbooks;
- Soul Fire'd;
- Goety e Goety Cataclysm;
- Black Flame do próprio Black Arcana;
- Fire school base do Iron's e addons.

## Constantine routing

Constantine acrescenta boas formas de obtenção/uso, não novos danos:

- pactos/barganhas;
- demon blood como chave/reagente;
- portais infernais;
- cages/true-name bindings;
- rituais que exploram regras da entidade infernal.

## Lava Infernal — regra rígida

`Lava Infernal != lava vanilla != Black Flame != Soul Fire != mana`

- só existe/é armazenada validamente no Nether;
- não sai via bucket/tank/contraption/portal/serialization;
- cross-dimension link proibido por padrão;
- storage invalid dimension rejeita inserção e uso;
- sem regeneração passiva;
- cada cast reserva e commita mB transacionalmente.

## VFX

- líquido vermelho muito mais escuro/saturado que lava vanilla;
- núcleo branco-amarelado apenas em pontos de temperatura extrema;
- veios pretos e emissive cracks;
- heat haze;
- brasas volumétricas;
- runas queimadas no ar/solo;
- spells grandes puxam visualmente energia em direção ao caster a partir do vínculo, sem precisar renderizar linha infinita entre dimensões.
