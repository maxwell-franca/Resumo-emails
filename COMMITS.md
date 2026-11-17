# 📝 Padrão de commits

Este projeto usa commits com **gitmoji**: um emoji no início da mensagem indica o tipo da mudança, seguido de uma frase curta no imperativo.

```
<emoji> <resumo curto da mudança>
```

## Emojis usados

| Emoji | Quando usar | Exemplo |
| --- | --- | --- |
| ✨ | Nova funcionalidade | `✨ Adiciona ramo para outro provedor de IA` |
| 🐛 | Correção de bug | `🐛 Evita eventos duplicados na agenda` |
| ⚡ | Melhoria de desempenho | `⚡ Reduz o tamanho do prompt enviado ao modelo` |
| 🔒 | Segurança e privacidade | `🔒 Remove e-mails e IDs do export do n8n` |
| 📝 | Documentação | `📝 Atualiza o README com a configuração do Ollama` |
| 🎉 | Commit inicial | `🎉 Primeiro commit` |
| ♻️ | Refatoração sem mudar comportamento | `♻️ Separa a lógica de datas no nó Parse` |
| 🔧 | Configuração | `🔧 Ajusta .gitignore` |
| 🔥 | Remoção de código ou arquivos | `🔥 Remove nó não utilizado` |

## Regras

- Uma mudança lógica por commit.
- Resumo com até ~70 caracteres, sem ponto final.
- **Nunca commitar um export bruto do n8n.** Rode sempre o `scripts/limpar_workflow.py` e publique só o resultado em `workflow/`.
