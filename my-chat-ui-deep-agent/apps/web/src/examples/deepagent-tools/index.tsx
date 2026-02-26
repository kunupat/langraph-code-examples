import { useCallback, useMemo, useState } from "react";
import { useStickToBottom } from "use-stick-to-bottom";
import { Layers } from "lucide-react";
import { useStream } from "@langchain/langgraph-sdk/react";
import type { Message } from "@langchain/langgraph-sdk";
import { LoadingIndicator } from "../../components/Loading";
import { EmptyState } from "../../components/States";
import { MessageBubble } from "../../components/MessageBubble";
import { MessageInput } from "../../components/MessageInput";
import { SubagentPipeline } from "./components/SubagentPipeline";
import type { agent } from "./agent";

import type { AgentState } from "./agent";

const EXAMPLE_SUGGESTIONS = [
    "Research the current state of AI in healthcare and create a summary report",
    "Analyze market trends for electric vehicles and draft key findings",
    "Gather information about sustainable energy and present the data",
    "Research remote work productivity studies and write a brief analysis",
];

function hasContent(message: Message): boolean {
    if (typeof message.content === "string") {
        return message.content.trim().length > 0;
    }
    if (Array.isArray(message.content)) {
        return (message.content as any[]).some(
            (c) => c.type === "text" && c.text.trim().length > 0
        );
    }
    return false;
}

function useThreadIdParam() {
    const [threadId, setThreadId] = useState<string | null>(() => {
        if (typeof window === "undefined") return null;
        const params = new URLSearchParams(window.location.search);
        return params.get("threadId");
    });

    const updateThreadId = useCallback((newThreadId: string | null) => {
        setThreadId(newThreadId);
        if (typeof window !== "undefined") {
            const url = new URL(window.location.href);
            if (newThreadId == null) {
                url.searchParams.delete("threadId");
            } else {
                url.searchParams.set("threadId", newThreadId);
            }
            window.history.replaceState({}, "", url.toString());
        }
    }, []);

    return [threadId, updateThreadId] as const;
}

export function DeepAgentToolsDemo() {
    const { scrollRef, contentRef } = useStickToBottom();
    const [threadId, onThreadId] = useThreadIdParam();

    const stream = useStream<AgentState>({

        assistantId: "deep_agent",
        apiUrl: "http://localhost:2024",
        filterSubagentMessages: true,
        threadId,
        onThreadId,
        reconnectOnMount: true,
        onError: (error) => {
            console.error("Stream error:", error);
        },
    });

    const hasMessages = stream.messages.length > 0;
    const hasSubagents = (stream.subagents?.size ?? 0) > 0;

    const allSubagentsDone = hasSubagents && [...(stream.subagents?.values() ?? [])].every(
        (s) => s.status === "complete" || s.status === "error"
    );

    const displayMessages = useMemo(() => {
        return stream.messages.filter((message) => {
            if (message.type === "human") return true;
            if (message.type === "tool") return false;
            if (message.type === "ai") {
                if ("tool_calls" in message && (message.tool_calls as any[])?.length) {
                    return hasContent(message);
                }
                return hasContent(message);
            }
            return false;
        });
    }, [stream.messages]);

    const handleSubmit = useCallback(
        (content: string) => {
            stream.submit(
                { messages: [{ content, type: "human" }] },
                {
                    streamSubgraphs: true,
                    config: { recursion_limit: 100 },
                }
            );
        },
        [stream]
    );

    const subagentsByHumanMessage = useMemo(() => {
        const result = new Map<string, ReturnType<typeof stream.getSubagentsByMessage>>();
        const msgs = stream.messages;
        for (let i = 0; i < msgs.length; i++) {
            if (msgs[i].type !== "human") continue;
            const next = msgs[i + 1];
            if (!next || next.type !== "ai" || !next.id) continue;
            const subagents = stream.getSubagentsByMessage(next.id);
            if (subagents.length > 0) {
                result.set(msgs[i].id!, subagents);
            }
        }
        return result;
    }, [stream.messages, stream.subagents]);

    return (
        <div className="h-full flex flex-col bg-neutral-950 text-white min-h-screen">
            <main ref={scrollRef} className="flex-1 overflow-y-auto [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-neutral-800 [&::-webkit-scrollbar-track]:bg-transparent">
                <div ref={contentRef} className="max-w-4xl mx-auto px-8 py-8">
                    {!hasMessages && !hasSubagents ? (
                        <EmptyState
                            icon={Layers}
                            title="Deep Agent with Tools"
                            description="Watch specialized subagents work on your task, each using their own tools. You'll see the research, analysis, and writing happen in real-time with full tool call visibility."
                            suggestions={EXAMPLE_SUGGESTIONS}
                            onSuggestionClick={handleSubmit}
                        />
                    ) : (
                        <div className="flex flex-col gap-6">
                            {displayMessages.map((message, idx) => {
                                const messageKey = message.id ?? `msg-${idx}`;
                                const turnSubagents = message.type === "human" ? subagentsByHumanMessage.get(messageKey) : undefined;
                                return (
                                    <div key={messageKey}>
                                        <MessageBubble message={message} />
                                        {turnSubagents && turnSubagents.length > 0 && (
                                            <div className="mt-6">
                                                <SubagentPipeline subagents={turnSubagents} isLoading={stream.isLoading && !allSubagentsDone} />
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                            {stream.isLoading && !hasSubagents && <LoadingIndicator />}
                            {stream.isLoading && allSubagentsDone && (
                                <div className="flex items-center gap-3 text-blue-400/70 animate-pulse">
                                    <span className="text-sm">Synthesizing results from all agents...</span>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </main>
            <MessageInput disabled={stream.isLoading} placeholder="Ask me to research, analyze, or write something..." onSubmit={handleSubmit} />
        </div>
    );
}

export default DeepAgentToolsDemo;
