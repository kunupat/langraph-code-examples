import { Search, FileText, Loader2, ListTodo } from "lucide-react";
import type { ToolMessage } from "@langchain/langgraph-sdk";
import type { ToolCallWithResult } from "@langchain/langgraph-sdk/react";

function parseToolResult(result?: ToolMessage) {
    if (!result) return { status: "pending" };
    try { return JSON.parse(result.content as string); } catch { return { status: "success", content: result.content as string }; }
}

function getToolIcon(name: string) {
    switch (name) {
        case "search_web": return <Search className="w-3.5 h-3.5" />;
        case "write_todos": return <ListTodo className="w-3.5 h-3.5" />;
        default: return <FileText className="w-3.5 h-3.5" />;
    }
}

export function SubagentToolCallCard({ toolCall, accentColor = "text-neutral-400" }: { toolCall: ToolCallWithResult; accentColor?: string }) {
    const { call, result, state } = toolCall;
    const parsedResult = parseToolResult(result);
    const isLoading = state === "pending";

    return (
        <div className="rounded-lg bg-black/30 border border-neutral-800/50 overflow-hidden">
            <div className="flex items-center gap-2 px-3 py-2 bg-neutral-900/50">
                <div className={`${accentColor}`}>{getToolIcon(call.name)}</div>
                <span className="text-xs font-medium text-neutral-300">{call.name}</span>
                {isLoading && <Loader2 className="w-3 h-3 animate-spin ml-auto" />}
            </div>
            {!isLoading && result && (
                <div className="px-3 py-2 text-xs border-t border-neutral-800/30 font-mono text-neutral-400 truncate">
                    {JSON.stringify(parsedResult)}
                </div>
            )}
        </div>
    );
}
