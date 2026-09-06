# Fonte Celestial — Sanctum e Ressonância Celestial

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO`

## Objetivo

Dar aos maiores milagres uma fonte rara/preparada sem exigir Aether e sem transformar luz solar em mana infinita.

## Modelo

`CASTER ⇄ CONSECRATED LINK ⇄ SANCTUM CORE ⇄ CELESTIAL RESONANCE`

Ressonância Celestial é uma carga abstrata armazenada, não um fluido em mB por padrão. A unidade final permanece `TBD`.

## Regras

- spells Holy normais continuam livres para usar mana/provider do Iron's;
- somente spells classificados `MIRACLE_TIER` exigem Ressonância Celestial, salvo design individual diferente;
- visão do céu é um gate físico, não fonte passiva infinita;
- geração requer ritual/consagração/ação causal;
- geração e consumo são server-authoritative;
- estrutura e owner precisam ser revalidados antes do gasto;
- nenhum evento visual do céu é prova de recurso disponível.

## Sem Aether

O sistema usa o Overworld real:

- céu aberto;
- Sol/Lua;
- estrelas/ciclo noturno;
- clima;
- altitude quando fizer sentido;
- eventos astronômicos/provider-native quando existirem.

Nenhuma dimensão celestial adicional é requisito.

## Integrações candidatas

### Paladin Spells / Holy

Pode fornecer ações Holy causais para consagração quando existir hook confiável. Não converter `Holy Spell Power` em moeda.

### Asterism Arcanum

Pode fornecer condições/objetos astral/celestial quando semanticamente adequados. `ASTRAL` e `HOLY` permanecem identidades diferentes.

### Hexalia

Hexalia possui `Celestial Infusion` e `Celestial Crystal`. Esse material/ritual é candidato forte a catalisador provider-native de construção/consagração, mas não deve ser automaticamente reinterpretado como Holy sem validar a versão instalada e a receita/semântica real.

### Eidolon

Teurgia, altares, oferendas e reputação podem ser provider-native para ritos de consagração se os hooks expuserem caster e resultado. Se não houver identidade causal suficiente, a integração fica fail-closed.

## Geração candidata

Uma cerimônia pode exigir simultaneamente:

1. Sanctum Core válido;
2. visão do céu;
3. janela solar/lunar/astral especificada;
4. reagentes consumíveis;
5. catalyst celestial/Holy provider-native;
6. ritual completo sem interrupção;
7. capacidade disponível no Sanctum.

O resultado adiciona uma quantidade bounded de Ressonância. Quantidade final = `TBD — Stage 08`.

## Anti-farm

- sem geração a cada tick por skylight;
- sem chunk loader necessário;
- sem duplicação por unload/reload;
- sem múltiplos cores creditando a mesma cerimônia se o contrato não permitir;
- sem fake sky em dimensão inválida;
- eventos/rituais possuem IDs e settlement exactly-once.

## HUD

Exemplo conceitual não numérico:

`Ressonância Celestial: 3 / 12 cargas`

ou unidade contínua caso o design final prove melhor. Não usar `mB` apenas por conveniência.

## Destruição/movimento

Sanctum móvel via contraption não é suportado por padrão. Se a estrutura perde validade, o link suspende. Política de recuperação do recurso armazenado precisa ser definida antes da implementação para impedir dupes e perdas arbitrárias.
