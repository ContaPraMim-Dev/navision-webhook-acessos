## Padrão de commit

Os commits devem ser semânticos e seguir o seguinte padrão:


feat: Adiciona gatinho dançante
^--^   ^------------^ -> Mensagem no imperativo
 *-> Tipos: chore, docs, feat, fix, refact, style or test.


Os tipos disponíveis são:

- `docs`: se refere à alterações na documentação.
- `feat`: se refere à implementação de features.
- `fix`: se refere à uma correção.
- `refact`: se refere à refatoração de uma feature previamente implementada.
- `style`: se refere à uma mudança estética no código. Por exemplo: alterar a indentação de espaço para tab.
##

#1 ORGANIZAÇÃO DE BRANCHS
- Para cada implementação, crie uma branch nova com o padrão dos tipos disponíveis e o nome do que será implementado;
  Exemplo: [feat/gatinho-dancante], [refact/gatinho-pulante];
- Para criar uma branch, use: git checkout -b x-nome-da-branch;
- Após criar a branch pra sua implementação, faça o que quiser nela, pois ainda não está na branch main, logo, não
  oferece risco à branch de produção;
- Depois de terminar a branch que você estava fazendo, dê git push, solicite o merge da sua branch e marque os outros devs do projeto como revisores do código, uma vez aprovado por TODOS, poderá subir a sua branch pra 'prod', onde será testada para então subir pra main;
- *NÃO CODAR NA PASTA MAIN!*

#2 MANTENDO SUA BRANCH ATUALIZADA
- Sempre que houver uma nova atualização, use "git pull origin main";
- Isso serve para que nossas branchs não tenham conflito, uma vez que pode ocorrer de alguém atualizar o código e
  você ainda não ter essa atualização na sua máquina, e vice-versa.
# Whatsapp_Bot_Mai
# Whatsapp_Bot_Mai_AWS
# Envio_de_mensagem_API_Gmail
# Django_API_Gmail
# Navision
# Aquacert# Aquacert
# aquacert_certificado
# aquacert_certificado
# aquacert_certificado
# aquacert_api_imo
# aquacert_api_imo
# navision-webhook-acessos
