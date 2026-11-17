# 📬 Resumo Diário de E-mails → Agenda

**Fluxo do n8n que, todo dia às 9h, lê os e-mails das últimas 24 horas, classifica por urgência com uma IA local (Ollama), envia um resumo para você e cria na agenda as tarefas que precisam de ação.**

![n8n](https://img.shields.io/badge/n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=for-the-badge)

---

## 🧠 O que é

Um fluxo de automação que transforma a caixa de entrada em uma lista do que realmente importa:

- 📥 **Leitura:** busca na caixa de entrada os e-mails das últimas 24 horas (até 30), ignorando os próprios resumos.
- 🤖 **Triagem por IA local:** um modelo rodando no seu computador (padrão `qwen2.5:7b`, via Ollama) define tópico, urgência, motivo, próxima ação e prazo de cada e-mail. **Nenhum conteúdo de e-mail vai para a nuvem.**
- 📧 **Resumo:** você recebe um e-mail com o panorama do dia, agrupado por tópico e com cores de urgência.
- 📅 **Agenda:** cada e-mail que exige ação vira um evento de 30 minutos no Google Agenda.

---

## ⚙️ Como funciona

```
Todo dia 9h → Config → Buscar e-mails (24h) → Prepare → Tem e-mails? → Usar Ollama? → Ollama → Parse ─┬→ Separar eventos → Criar evento na agenda
                                                                                                      └→ Enviar resumo
```

| Urgência | Quando | Horário do evento na agenda |
| --- | --- | --- |
| 🔴 Alta | Prazo em até 48h, cobrança pendente, cliente ou chefia aguardando | Hoje às 11h (ou às 9h do dia do prazo) |
| 🟡 Média | Pede resposta ou ação, sem prazo curto | Hoje às 16h (ou às 9h do dia do prazo) |
| 🟢 Baixa | Informativo, newsletter, promoção, notificação | Não vai para a agenda |

---

## ✨ Funcionalidades

- Execução diária por agendamento (`0 9 * * *`)
- Classificação em tópicos: Financeiro/Cobrança, Clientes, Trabalho, Pessoal, Notificações/Newsletters e Outros
- Resumo em HTML com contagem por urgência e prazos
- Texto dos e-mails escapado antes de entrar no HTML do resumo
- Não envia nada quando não há e-mails novos
- Configuração em um único nó (`Config`): modelo, endereço do Ollama, limite de e-mails e seu e-mail
- Fluxo importado **inativo**, para você testar antes de ligar

---

## 🔧 Requisitos

| Item | Observação |
| --- | --- |
| [n8n](https://n8n.io/) | Versão com os nós Gmail, Google Calendar, Code e Schedule |
| [Ollama](https://ollama.com/) | Com o modelo baixado: `ollama pull qwen2.5:7b` |
| Conta Google | Credenciais OAuth2 do Gmail (ler e enviar) e do Google Calendar (criar eventos) |

---

## 📁 Estrutura

```
n8n-resumo-emails-agenda/
├── workflow/
│   └── resumo-diario-emails-agenda.json   # fluxo limpo, pronto para importar
├── scripts/
│   └── limpar_workflow.py                 # limpa um export antes de publicar
├── COMMITS.md                             # padrão de commits do projeto
├── LICENSE
└── README.md
```

---

## 🚀 Como usar

1. **Clone o repositório**
   ```
   git clone https://github.com/maxwell-franca/n8n-resumo-emails-agenda.git
   ```
2. **Importe o fluxo** no n8n: menu **⋯** → **Import from File** → `workflow/resumo-diario-emails-agenda.json`.
3. **Crie as credenciais** do Gmail e do Google Calendar no n8n (guia oficial: [Google credentials](https://docs.n8n.io/integrations/builtin/credentials/google/)) e selecione-as nos três nós que as usam: `Buscar e-mails (24h)`, `Enviar resumo` e `Criar evento na agenda`.
4. **Edite o nó `Config`:**
   - `meuEmail`: o e-mail que vai receber o resumo (o valor inicial é `COLOQUE_SEU_EMAIL_AQUI`, de propósito: se você esquecer, o envio falha em vez de ir para o endereço errado)
   - `ollamaUrl`: onde está o Ollama (padrão `http://host.docker.internal:11434`, para n8n em Docker e Ollama no computador)
   - `ollamaModel` e `maxEmails`, se quiser mudar
5. **Confira o nó `Criar evento na agenda`:** ele vem apontando para a agenda principal (`primary`). Se quiser outra agenda, escolha-a na lista.
6. **Teste:** clique em **Execute workflow** e confira o e-mail de resumo e os eventos criados.
7. **Ative o fluxo** (botão **Active**) para rodar todo dia às 9h.

> **Docker no Linux:** o endereço `host.docker.internal` só funciona se o contêiner do n8n for iniciado com `--add-host=host.docker.internal:host-gateway`.

> **Horário:** o agendamento usa o fuso configurado na sua instância do n8n. Ajuste em **Settings** do fluxo, ou na variável `GENERIC_TIMEZONE`, para que as 9h sejam as suas. Os nós de código calculam as datas em `America/Fortaleza`.

---

## 🔒 Privacidade e segurança

**Para onde vai o conteúdo dos e-mails:** remetente, assunto e os primeiros 300 caracteres de cada e-mail vão **somente** para o Ollama no endereço de `ollamaUrl`. Com o Ollama no seu computador, nada sai da sua máquina, além das chamadas normais às APIs do Google (Gmail e Agenda) feitas com a sua autorização.

> O nó `Config` tem os campos `provider` e `claudeModel`, mas **o fluxo não tem ramo para outro provedor**: com `provider` diferente de `ollama`, ele simplesmente termina sem fazer nada. Se você criar esse ramo, o conteúdo dos e-mails passará a ser enviado a esse serviço externo.

**Nunca publique o export bruto do n8n.** Ele traz o seu e-mail, o ID das suas credenciais, o ID da sua instância e, se houver, dados fixados de execuções (`pinData`), que podem conter e-mails reais. Antes de publicar qualquer alteração, rode:

```
python scripts/limpar_workflow.py meu-export.private.json workflow/resumo-diario-emails-agenda.json
```

O script troca e-mails por placeholder, remove credenciais, IDs e `pinData`, e **se recusa a gravar** se sobrar algo suspeito. Nomeie seus exports como `*.private.json`: o `.gitignore` já os ignora.

**E-mails podem tentar manipular a IA.** O texto de e-mails recebidos entra no prompt, e a resposta do modelo vira eventos na agenda. Um e-mail malicioso poderia fazer o modelo criar um evento com texto escolhido por quem escreveu. O risco é baixo (eventos de 30 minutos, no máximo `maxEmails` por execução, 30 por padrão, sem acesso a mais nada), mas **revise a agenda** de vez em quando.

---

## ⚠️ Limitações

- **Só o Ollama funciona:** não há ramo para outros provedores de IA (veja acima).
- **Sem controle de duplicatas:** rodar o fluxo duas vezes no mesmo dia cria os eventos duas vezes.
- **Resposta inválida da IA interrompe o fluxo:** se o modelo não devolver um JSON válido (mais comum em modelos pequenos), o nó `Parse` gera erro e nada é enviado nem agendado.
- **Janela de 24 horas e até 30 e-mails:** o que passar disso não entra no resumo.
- **Só a caixa de entrada:** e-mails arquivados, no spam ou em outras pastas são ignorados.

---

## 📝 Padrão de commits

Este projeto usa commits com gitmoji. Os detalhes estão em [COMMITS.md](COMMITS.md).

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE).

---

## 👤 Autor

**Maxwell França** · Contador & Administrador | IA, Automação e Sistemas Embarcados  
🇧🇷 São Luís – MA, Brasil

<a href="https://github.com/maxwell-franca">
  <img src="https://img.shields.io/badge/GitHub-maxwell--franca-181717?style=for-the-badge&logo=github" />
</a>

---

⭐ Se gostou do projeto, deixe uma estrela no repositório
