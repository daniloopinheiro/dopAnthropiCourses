# Exemplo: deck didático enxuto

```markdown
# Introdução ao Repository Pattern

> **Formato:** Pronto para copiar em slides ou apresentar
> **Duração sugerida:** 25 min + 10 min Q&A
> **Audiência:** Desenvolvedores .NET iniciantes em camadas

---

## Slide 1: Repository Pattern isola persistência do domínio

**Plataforma .NET — Semana 17**

**Objetivos:**
- Explicar o que é Repository Pattern
- Mostrar quando usar e quando não usar
- Implementar um repositório simples com EF Core

**Notas do apresentador:** Confirmar que todos já viram DbContext direto no controller.

---

## Slide 2: Controllers não devem conhecer detalhes de SQL ou EF

**Problema:**
- Lógica de acesso a dados espalhada
- Testes unitários difíceis (precisam de banco)
- Trocar EF por outro provider vira refactor grande

**Visual sugerido:** diagrama Controller → DbContext (❌) vs Controller → Repository → DbContext (✅)

---

## Slide 3: Repository é uma abstração sobre coleções de entidades

**Definição:**
- Interface no domínio/aplicação (`IProductRepository`)
- Implementação na infraestrutura (`EfProductRepository`)
- Métodos expressam intenção de negócio (`GetBySku`, não `Query().Where...`)

**Código (máx. 8 linhas):**
```csharp
public interface IProductRepository
{
    Task<Product?> GetBySkuAsync(string sku, CancellationToken ct);
}
```

**Notas do apresentador:** Enfatizar que a interface vive onde a aplicação precisa, não na infra.

---

## Slide 4: Resumo — abstraia persistência, teste com mocks, implemente na infra

1. Interface na Application/Domain
2. Implementação com EF na Infrastructure
3. Registrar no DI
4. Controller/Handler depende da interface

**Próximo passo:** exercício — extrair repositório do projeto ToDoList
```
