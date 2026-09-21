---
name: "copilot-sdk"
description: "Build agentic applications with the GitHub Copilot SDK. Use when embedding AI agents in applications, creating custom tools, implementing streaming responses, managing sessions, connecting to MCP servers, or creating custom agents. Triggers include Copilot SDK, GitHub SDK, agentic application, embed Copilot, programmable agent, MCP server, and custom agent."
---
# GitHub Copilot SDK

Embed Copilot's agentic workflows in any application with Python, TypeScript, Go, or .NET.

| Area | Sections |
|---|---|
| Setup | Prerequisites, installation, quick start |
| Interaction | Streaming responses, interactive CLI assistant, common patterns |
| Agent extension | Custom tools, MCP server integration, custom agents, system message |
| Advanced configuration | Client configuration, session configuration, session persistence |
| Reference | Event types, available models, best practices, architecture |

## Overview

The GitHub Copilot SDK exposes the same engine as the Copilot CLI: a production-tested agent runtime you can invoke from code. You do not need to build your own orchestration. You define the agent's behavior, and Copilot handles planning, tool invocation, file editing, and other tasks.

## When to Invoke

- "Embed a Copilot agent in our application with the Copilot SDK."
- "Add a custom tool the agent can call during a session."
- "Stream the model's response, token by token, in our CLI."
- "Connect the SDK to an MCP server and a custom agent."

> [!NOTE]
> The SDK controls the GitHub Copilot CLI, which must be installed and authenticated (see prerequisites). It is in Technical Preview and may introduce breaking changes. Pin versions and retest when upgrading.

## Prerequisites

1. **GitHub Copilot CLI** installed and authenticated ([installation guide](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli))
2. **Language runtime**: Node.js 18+, Python 3.8+, Go 1.21+, or .NET 8.0+

Check the CLI: `copilot --version`

## Installation

### Node.js/TypeScript

```bash
mkdir copilot-demo && cd copilot-demo
npm init -y --init-type module
npm install @github/copilot-sdk tsx
```

### Installation for Python

```bash
pip install github-copilot-sdk
```

### Installation for Go

```bash
mkdir copilot-demo && cd copilot-demo
go mod init copilot-demo
go get github.com/github/copilot-sdk/go
```

### Installation for .NET

```bash
dotnet new console -n CopilotDemo && cd CopilotDemo
dotnet add package GitHub.Copilot.SDK
```

## Quick start

### Quick start with TypeScript

```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
});

const response = await session.sendAndWait({ prompt: "What is 2 + 2?" });
console.log(response?.data.content);

await client.stop();
process.exit(0);
```

Run: `npx tsx index.ts`

### Quick start with Python

```python
import asyncio
from copilot import CopilotClient, PermissionHandler

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
    })
    response = await session.send_and_wait({"prompt": "What is 2 + 2?"})

    print(response.data.content)
    await client.stop()

asyncio.run(main())
```

### Quick start with Go

```go
package main

import (
    "fmt"
    "log"
    "os"
    copilot "github.com/github/copilot-sdk/go"
)

func main() {
    client := copilot.NewClient(nil)
    if err := client.Start(); err != nil {
        log.Fatal(err)
    }
    defer client.Stop()

    session, err := client.CreateSession(&copilot.SessionConfig{
        OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
        Model:               "gpt-4.1",
    })
    if err != nil {
        log.Fatal(err)
    }

    response, err := session.SendAndWait(copilot.MessageOptions{Prompt: "What is 2 + 2?"}, 0)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println(*response.Data.Content)
    os.Exit(0)
}
```

### .NET (C#)

```csharp
using GitHub.Copilot.SDK;

await using var client = new CopilotClient();
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
});

var response = await session.SendAndWaitAsync(new MessageOptions { Prompt = "What is 2 + 2?" });
Console.WriteLine(response?.Data.Content);
```

Run: `dotnet run`

## Streaming responses

Enable real-time output for a better user experience:

### Streaming responses with TypeScript

```typescript
import { CopilotClient, approveAll, SessionEvent } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    streaming: true,
});

session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
    }
    if (event.type === "session.idle") {
        console.log(); // Newline on completion
    }
});

await session.sendAndWait({ prompt: "Tell a short joke" });

await client.stop();
process.exit(0);
```

### Streaming responses with Python

```python
import asyncio
import sys
from copilot import CopilotClient, PermissionHandler
from copilot.generated.session_events import SessionEventType

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
        "streaming": True,
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()
        if event.type == SessionEventType.SESSION_IDLE:
            print()

    session.on(handle_event)
    await session.send_and_wait({"prompt": "Tell a short joke"})
    await client.stop()

asyncio.run(main())
```

### Streaming responses with Go

```go
session, err := client.CreateSession(&copilot.SessionConfig{
 OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
    Model:     "gpt-4.1",
    Streaming: true,
})

session.On(func(event copilot.SessionEvent) {
    if event.Type == "assistant.message_delta" {
        fmt.Print(*event.Data.DeltaContent)
    }
    if event.Type == "session.idle" {
        fmt.Println()
    }
})

_, err = session.SendAndWait(copilot.MessageOptions{Prompt: "Tell a short joke"}, 0)
```

### Streaming responses with .NET

```csharp
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
    Streaming = true,
});

session.On(ev =>
{
    if (ev is AssistantMessageDeltaEvent deltaEvent)
        Console.Write(deltaEvent.Data.DeltaContent);
    if (ev is SessionIdleEvent)
        Console.WriteLine();
});

await session.SendAndWaitAsync(new MessageOptions { Prompt = "Tell a short joke" });
```

## Custom tools

Define tools that Copilot can invoke during reasoning. When defining a tool, you tell Copilot:

1. **What the tool does** (description)
2. **Which parameters it requires** (schema)
3. **Which code to execute** (handler)

### TypeScript (JSON Schema)

```typescript
import { CopilotClient, approveAll, defineTool, SessionEvent } from "@github/copilot-sdk";

const getWeather = defineTool("get_weather", {
    description: "Get the current weather for a city",
    parameters: {
        type: "object",
        properties: {
            city: { type: "string", description: "The city name" },
        },
        required: ["city"],
    },
    handler: async (args: { city: string }) => {
        const { city } = args;
        // In a real application, call a weather API here
        const conditions = ["sunny", "cloudy", "rainy", "partly cloudy"];
        const temp = Math.floor(Math.random() * 30) + 50;
        const condition = conditions[Math.floor(Math.random() * conditions.length)];
        return { city, temperature: `${temp}°F`, condition };
    },
});

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    streaming: true,
    tools: [getWeather],
});

session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
    }
});

await session.sendAndWait({
    prompt: "What is the weather like in Seattle and Tokyo?",
});

await client.stop();
process.exit(0);
```

### Python (Pydantic)

```python
import asyncio
import random
import sys
from copilot import CopilotClient, PermissionHandler
from copilot.tools import define_tool
from copilot.generated.session_events import SessionEventType
from pydantic import BaseModel, Field

class GetWeatherParams(BaseModel):
    city: str = Field(description="The name of the city whose forecast will be queried")

@define_tool(description="Get the current weather for a city")
async def get_weather(params: GetWeatherParams) -> dict:
    city = params.city
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    temp = random.randint(50, 80)
    condition = random.choice(conditions)
    return {"city": city, "temperature": f"{temp}°F", "condition": condition}

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
        "streaming": True,
        "tools": [get_weather],
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()

    session.on(handle_event)

    await session.send_and_wait({
        "prompt": "What is the weather like in Seattle and Tokyo?"
    })

    await client.stop()

asyncio.run(main())
```

### Custom tools with Go

```go
type WeatherParams struct {
    City string `json:"city" jsonschema:"The city name"`
}

type WeatherResult struct {
    City        string `json:"city"`
    Temperature string `json:"temperature"`
    Condition   string `json:"condition"`
}

getWeather := copilot.DefineTool(
    "get_weather",
    "Get the current weather for a city",
    func(params WeatherParams, inv copilot.ToolInvocation) (WeatherResult, error) {
        conditions := []string{"sunny", "cloudy", "rainy", "partly cloudy"}
        temp := rand.Intn(30) + 50
        condition := conditions[rand.Intn(len(conditions))]
        return WeatherResult{
            City:        params.City,
            Temperature: fmt.Sprintf("%d°F", temp),
            Condition:   condition,
        }, nil
    },
)

session, _ := client.CreateSession(&copilot.SessionConfig{
 OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
    Model:     "gpt-4.1",
    Streaming: true,
    Tools:     []copilot.Tool{getWeather},
})
```

### .NET (Microsoft.Extensions.AI)

```csharp
using GitHub.Copilot.SDK;
using Microsoft.Extensions.AI;
using System.ComponentModel;

var getWeather = AIFunctionFactory.Create(
    ([Description("The city name")] string city) =>
    {
        var conditions = new[] { "sunny", "cloudy", "rainy", "partly cloudy" };
        var temp = Random.Shared.Next(50, 80);
        var condition = conditions[Random.Shared.Next(conditions.Length)];
        return new { city, temperature = $"{temp}°F", condition };
    },
    "get_weather",
    "Get the current weather for a city"
);

await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
    Streaming = true,
    Tools = [getWeather],
});
```

## How tools work

When Copilot decides to call your tool:

1. Copilot sends a tool call request with the parameters.
2. The SDK executes your handler function.
3. The result is sent back to Copilot.
4. Copilot incorporates the result into the response.

Copilot decides when to call the tool based on the user's question and the tool's description.

## Interactive CLI assistant

Create a complete interactive assistant:

### Interactive CLI assistant with TypeScript

```typescript
import { CopilotClient, approveAll, defineTool, SessionEvent } from "@github/copilot-sdk";
import * as readline from "readline";

const getWeather = defineTool("get_weather", {
    description: "Get the current weather for a city",
    parameters: {
        type: "object",
        properties: {
            city: { type: "string", description: "The city name" },
        },
        required: ["city"],
    },
    handler: async ({ city }) => {
        const conditions = ["sunny", "cloudy", "rainy", "partly cloudy"];
        const temp = Math.floor(Math.random() * 30) + 50;
        const condition = conditions[Math.floor(Math.random() * conditions.length)];
        return { city, temperature: `${temp}°F`, condition };
    },
});

const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    streaming: true,
    tools: [getWeather],
});

session.on((event: SessionEvent) => {
    if (event.type === "assistant.message_delta") {
        process.stdout.write(event.data.deltaContent);
    }
});

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

console.log("Weather assistant (type 'sair' to exit)");
console.log("Try: 'What is the weather like in Paris?'\n");

const prompt = () => {
    rl.question("You: ", async (input) => {
        if (input.toLowerCase() === "sair") {
            await client.stop();
            rl.close();
            return;
        }

        process.stdout.write("Assistant: ");
        await session.sendAndWait({ prompt: input });
        console.log("\n");
        prompt();
    });
};

prompt();
```

### Interactive CLI assistant with Python

```python
import asyncio
import random
import sys
from copilot import CopilotClient, PermissionHandler
from copilot.tools import define_tool
from copilot.generated.session_events import SessionEventType
from pydantic import BaseModel, Field

class GetWeatherParams(BaseModel):
    city: str = Field(description="The name of the city whose forecast will be queried")

@define_tool(description="Get the current weather for a city")
async def get_weather(params: GetWeatherParams) -> dict:
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    temp = random.randint(50, 80)
    condition = random.choice(conditions)
    return {"city": params.city, "temperature": f"{temp}°F", "condition": condition}

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "on_permission_request": PermissionHandler.approve_all,
        "model": "gpt-4.1",
        "streaming": True,
        "tools": [get_weather],
    })

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()

    session.on(handle_event)

    print("Weather assistant (type 'sair' to exit)")
    print("Try: 'What is the weather like in Paris?'\n")

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break

        if user_input.lower() == "sair":
            break

        sys.stdout.write("Assistant: ")
        await session.send_and_wait({"prompt": user_input})
        print("\n")

    await client.stop()

asyncio.run(main())
```

## MCP server integration

Connect to MCP (Model Context Protocol) servers to use ready-made tools. Connect to the GitHub MCP server to access repositories, issues, and PRs:

### MCP server integration in TypeScript

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    mcpServers: {
        github: {
            type: "http",
            url: "https://api.githubcopilot.com/mcp/",
        },
    },
});
```

### MCP server integration in Python

```python
session = await client.create_session({
    "on_permission_request": PermissionHandler.approve_all,
    "model": "gpt-4.1",
    "mcp_servers": {
        "github": {
            "type": "http",
            "url": "https://api.githubcopilot.com/mcp/",
        },
    },
})
```

### MCP server integration in Go

```go
session, _ := client.CreateSession(&copilot.SessionConfig{
 OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
    Model: "gpt-4.1",
    MCPServers: map[string]copilot.MCPServerConfig{
        "github": {
            "type": "http",
            "url": "https://api.githubcopilot.com/mcp/",
        },
    },
})
```

### MCP server integration in .NET

```csharp
await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
    McpServers = new Dictionary<string, McpServerConfig>
    {
        ["github"] = new McpServerConfig
        {
            Type = "http",
            Url = "https://api.githubcopilot.com/mcp/",
        },
    },
});
```

## Custom agents

Define specialized AI personas for specific tasks:

### Custom agents in TypeScript

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    customAgents: [{
        name: "pr-reviewer",
        displayName: "PR reviewer",
        description: "Reviews pull requests against best practices",
        prompt: "You are a code review expert. Focus on security, performance, and maintainability.",
    }],
});
```

### Custom agents in Python

```python
session = await client.create_session({
    "on_permission_request": PermissionHandler.approve_all,
    "model": "gpt-4.1",
    "custom_agents": [{
        "name": "pr-reviewer",
        "display_name": "PR reviewer",
        "description": "Reviews pull requests against best practices",
        "prompt": "You are a code review expert. Focus on security, performance, and maintainability.",
    }],
})
```

## System message

Customize the AI's behavior and personality:

### System message in TypeScript

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    systemMessage: {
        content: "You are a helpful assistant for our engineering team. Always be concise.",
    },
});
```

### System message in Python

```python
session = await client.create_session({
    "on_permission_request": PermissionHandler.approve_all,
    "model": "gpt-4.1",
    "system_message": {
        "content": "You are a helpful assistant for our engineering team. Always be concise.",
    },
})
```

## External CLI server

Run the CLI separately in server mode and connect the SDK to it. This is useful for debugging, resource sharing, or custom environments.

### Start the CLI in server mode

```bash
copilot --server --port 4321
```

### Connect the SDK to an external server

#### Connect the SDK to an external server with TypeScript

```typescript
const client = new CopilotClient({
    cliUrl: "localhost:4321"
});

const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
});
```

#### Connect the SDK to an external server with Python

```python
client = CopilotClient({
    "cli_url": "localhost:4321"
})
await client.start()

session = await client.create_session({
    "on_permission_request": PermissionHandler.approve_all,
    "model": "gpt-4.1",
})
```

#### Connect the SDK to an external server with Go

```go
client := copilot.NewClient(&copilot.ClientOptions{
    CLIUrl: "localhost:4321",
})

if err := client.Start(); err != nil {
    log.Fatal(err)
}

session, _ := client.CreateSession(&copilot.SessionConfig{
 OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
 Model:               "gpt-4.1",
})
```

#### Connect the SDK to an external server with .NET

```csharp
using var client = new CopilotClient(new CopilotClientOptions
{
    CliUrl = "localhost:4321"
});

await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-4.1",
});
```

**Note:** when `cliUrl` is supplied, the SDK does not start or manage a CLI process. It only connects to the existing server.

## Event types

| Event | Description |
|-------|-------------|
| `user.message` | User input added |
| `assistant.message` | Complete model response |
| `assistant.message_delta` | Streaming response chunk |
| `assistant.reasoning` | Model reasoning (model-dependent) |
| `assistant.reasoning_delta` | Streaming reasoning chunk |
| `tool.execution_start` | Tool invocation started |
| `tool.execution_complete` | Tool execution completed |
| `session.idle` | No active processing |
| `session.error` | An error occurred |

## Client configuration

| Option | Description | Default |
|--------|-------------|---------|
| `cliPath` | Path to the Copilot CLI executable | System PATH |
| `cliUrl` | Connection to an existing server (for example, "localhost:4321") | None |
| `port` | Server communication port | Random |
| `useStdio` | Use stdio transport instead of TCP | true |
| `logLevel` | Log verbosity | "info" |
| `autoStart` | Automatic server startup | true |
| `autoRestart` | Restart after failures | true |
| `cwd` | CLI process working directory | Inherited |

## Session configuration

| Option | Description |
|--------|-------------|
| `model` | LLM to use ("gpt-4.1", "claude-sonnet-4.5", etc.) |
| `sessionId` | Custom session identifier |
| `tools` | Custom tool definitions |
| `mcpServers` | MCP server connections |
| `customAgents` | Custom agent personas |
| `systemMessage` | Override of the default system instruction |
| `streaming` | Enable incremental response chunks |
| `availableTools` | Allowed tool list |
| `excludedTools` | Disabled tool list |

## Session persistence

Save and resume conversations across restarts:

### Create with a custom ID

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    sessionId: "user-123-conversation",
    model: "gpt-4.1"
});
```

### Resume a session

```typescript
const session = await client.resumeSession("user-123-conversation", { onPermissionRequest: approveAll });
await session.send({ prompt: "What did we discuss previously?" });
```

### List and delete sessions

```typescript
const sessions = await client.listSessions();
await client.deleteSession("old-session-id");
```

## Error handling

```typescript
try {
    const client = new CopilotClient();
    const session = await client.createSession({
        onPermissionRequest: approveAll,
        model: "gpt-4.1",
    });
    const response = await session.sendAndWait(
        { prompt: "Hello!" },
        30000 // timeout in ms
    );
} catch (error) {
    if (error.code === "ENOENT") {
        console.error("Copilot CLI is not installed");
    } else if (error.code === "ECONNREFUSED") {
        console.error("Could not connect to the Copilot server");
    } else {
        console.error("Error:", error.message);
    }
} finally {
    await client.stop();
}
```

## Graceful shutdown

```typescript
process.on("SIGINT", async () => {
    console.log("Shutting down...");
    await client.stop();
    process.exit(0);
});
```

## Common patterns

### Multi-turn conversation

```typescript
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
});

await session.sendAndWait({ prompt: "My name is Alice" });
await session.sendAndWait({ prompt: "What is my name?" });
// Response: "Your name is Alice"
```

### File attachments

```typescript
await session.send({
    prompt: "Analyze this file",
    attachments: [{
        type: "file",
        path: "./data.csv",
        displayName: "Sales data"
    }]
});
```

### Abort long-running operations

```typescript
const timeoutId = setTimeout(() => {
    session.abort();
}, 60000);

session.on((event) => {
    if (event.type === "session.idle") {
        clearTimeout(timeoutId);
    }
});
```

## Available models

Query available models at runtime:

```typescript
const models = await client.getModels();
// Returns: ["gpt-4.1", "gpt-4o", "claude-sonnet-4.5", ...]
```

## Best practices

1. **Always clean up**: use `try-finally` or `defer` to guarantee the `client.stop()` call.
2. **Set timeouts**: use `sendAndWait` with a timeout for long-running operations.
3. **Handle events**: subscribe to error events for robust error handling.
4. **Use streaming**: enable streaming for a better experience with long responses.
5. **Persist sessions**: use custom IDs for multi-turn conversations.
6. **Define clear tools**: write informative tool names and descriptions.

## Architecture

```text
Your application
       |
  SDK client
       | JSON-RPC
  Copilot CLI (server mode)
       |
  GitHub (models, authentication)
```

The SDK automatically manages the CLI process lifecycle. All communication uses JSON-RPC over stdio or TCP.

## Output Template

A delivered integration follows this structure: client, session, optional tools, execution loop, and guaranteed cleanup:

```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

// 1. Create the client and a session (add custom tools through `tools: [...]`).
const client = new CopilotClient();
const session = await client.createSession({
    onPermissionRequest: approveAll,
    model: "gpt-4.1",
    streaming: true,
});

// 2. Drive the agent.
try {
    const response = await session.sendAndWait({ prompt: "..." }, 30000);
    console.log(response?.data.content);
} finally {
    // 3. Always clean up.
    await client.stop();
}
```

Report the language and runtime, models used, connected tools or MCP servers, and how the process is cleaned up.

## Quality Gate

- [ ] Copilot CLI is installed and authenticated, and the chosen runtime matches the SDK (Node.js 18+, Python 3.8+, Go 1.21+, or .NET 8.0+).
- [ ] `client.stop()` is guaranteed on every path (`try/finally`, `defer`, or `await using`).
- [ ] Long-running calls use `sendAndWait` with a timeout, and errors and `session.error` events are handled.
- [ ] Custom tools declare clear names, descriptions, and parameter schemas.
- [ ] Secrets and tokens are never hardcoded. MCP endpoints and models remain in configuration.
- [ ] The integration runs end to end on the target model before it is considered complete.

## Resources

- **GitHub repository**: https://github.com/github/copilot-sdk
- **Getting started tutorial**: https://github.com/github/copilot-sdk/blob/main/docs/tutorials/first-app.md
- **GitHub MCP server**: https://github.com/github/github-mcp-server
- **MCP server directory**: https://github.com/modelcontextprotocol/servers
- **Cookbook**: https://github.com/github/copilot-sdk/tree/main/cookbook
- **Examples**: https://github.com/github/copilot-sdk/tree/main/samples

## Status

This SDK is in **Technical Preview** and may receive breaking changes. It is not yet recommended for production use.
