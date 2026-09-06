# Política canônica de deduplicação de magia

## Princípio

`PROVIDER-NATIVE FIRST`.

Black Arcana não deve recriar um spell apenas para dar outro nome, outra cor ou outro provider. Se um mod instalado já fornece a mecânica com qualidade e authority adequadas, a preferência é integrar, especializar, retexturizar quando permitido ou compor sobre essa implementação.

## Assinatura semântica

Cada spell/poder catalogado recebe uma assinatura mínima:

`{ host/provider, escola, recurso, delivery, target topology, effect family, damage family, control/mobility primitive, world mutation, persistence, acquisition, special mechanic }`

Exemplos de `delivery`: projectile, beam, self, target, area, channel, ritual, trap, portal, aura.

Exemplos de `target topology`: single, cone, chain, radius, line, paired endpoints, linked source, domain.

## Classes de sobreposição

- `EXATO` — mesma mecânica/função substancial. Reutilizar provider; novo spell proibido salvo migração explícita.
- `ALTO` — fantasia diferente, mas loop/efeito quase idêntico. Preferir integração/skin/variant antes de novo spell.
- `PARCIAL` — compartilha primitivas, mas possui decisão ou consequência mecânica nova. Pode existir se o delta for documentado.
- `DISTINTO` — papel e mecânica claramente diferentes. Pode prosseguir normalmente.

Não usar percentual automático como autoridade. A classificação precisa justificar quais dimensões coincidem e quais criam gameplay novo.

## Gate para spell novo

Antes de aprovar um spell novo, a página deve responder:

1. Qual spell/glyph/ritual existente é o concorrente mais próximo?
2. Por que não basta integrar esse provider?
3. Qual decisão nova o jogador toma?
4. Qual consequência mecânica nova aparece?
5. Há novo recurso, targeting, persistência, risco, domínio ou interação que justifique existir?
6. O novo conteúdo cria uma escola coerente ou apenas inflação de catálogo?

Sem delta claro, o conceito fica `REDUNDANTE / NÃO APROVADO`.

## Bridges e composições

Uma bridge pode transformar a apresentação ou conectar autoridades sem criar um segundo efeito. Exemplo: o Portal Spell do Iron's pode continuar sendo o cast/provider enquanto Immersive Portals fornece o portal contínuo e Black Arcana aplica políticas adicionais de segurança quando necessário.

Witchcraft pode compor efeitos existentes de Hexalia/Toxony/Malum/Eidolon/Ars/Iron's sem copiar as poções ou buffs. A receita/ritual novo deve ser uma composição com provenance, não uma duplicata invisível.

## Variantes visuais

Cor, textura, partículas, animação e áudio não bastam para justificar spell duplicado. Variantes puramente visuais devem compartilhar identidade mecânica ou ser tratadas como skin/presentation profile quando a API permitir.

## Migração de ideias do Mahou

A origem histórica no Mahou deve ser registrada em `Proveniência`, mas a implementação final deve escolher o provider atual mais adequado do pack. Uma inspiração Mahou não obriga o Black Arcana a manter a mesma arquitetura nem a duplicar algo que Iron's, Ars, Goety, Malum, Eidolon, Hexalia ou outro provider já faça melhor.

## Evidência

A deduplicação só fecha com a versão instalada real. Páginas públicas e wikis ajudam a descobrir conteúdo, mas IDs, valores e hooks que afetam implementação devem ser validados contra runtime/código/config da versão instalada sempre que necessário.
