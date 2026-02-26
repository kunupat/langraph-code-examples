import { useEffect, useRef, useMemo, useState } from "react";
import { Search, BarChart3, PenLine, Loader2, CheckCircle2, AlertCircle, Clock, ChevronDown, ChevronRight, Wrench } from "lucide-react";
import type { SubagentStream } from "@langchain/langgraph-sdk/react";
import { SubagentToolCallCard } from "./SubagentToolCallCard";
import { SUBAGENT_CONFIGS, type SubagentType } from "../types";

interface SubagentMessage {
    id?: string;
    type: "human" | "ai" | "tool" | "system";
    content: string | Array<{ type: string; text?: string }>;
    tool_calls?: Array<{ id: string; name: string; args: Record<string, unknown> }>;
}

const DEFAULT_CONFIG = {
    icon: "tool", title: "Specialist Agent", gradient: "from-violet-500/20 to-purple-600/20", borderColor: "border-violet-500/40", bgColor: "bg-violet-950/30", iconBg: "bg-violet-500/20", accentColor: "text-violet-400"
};

function getSubagentIcon(type: string | undefined) {
    switch (type) {
        case "researcher": return <Search className="w-5 h-5" />;
        case "data-analyst": return <BarChart3 className="w-5 h-5" />;
        case "content-writer": return <PenLine className="w-5 h-5" />;
        default: return <Loader2 className="w-5 h-5 animate-spin" />;
    }
}

function getStreamingContent(messages: SubagentMessage[]): string {
    return messages.filter((m) => m.type === "ai").map((m) => {
        if (typeof m.content === "string") return m.content;
        if (Array.isArray(m.content)) return m.content.filter((c: any) => c.type === "text" && c.text).map((c: any) => c.text).join("");
        return "";
    }).join("");
}

function StatusIcon({ status, accentColor }: { status: string; accentColor: string }) {
    switch (status) {
        case "pending": return <Clock className="w-4 h-4 text-neutral-500" />;
        case "running": return <Loader2 className={`w-4 h-4 animate-spin ${accentColor}`} />;
        case "complete": return <CheckCircle2 className="w-4 h-4 text-green-400" />;
        case "error": return <AlertCircle className="w-4 h-4 text-red-400" />;
        default: return null;
    }
}

export function SubagentStreamCard({ subagent, defaultExpanded = true }: { subagent: SubagentStream; defaultExpanded?: boolean }) {
    const scrollRef = useRef<HTMLDivElement>(null);
    const [isExpanded, setIsExpanded] = useState(defaultExpanded);
    const subagentType = subagent.toolCall?.args?.subagent_type as SubagentType | undefined;
    const config = (subagentType && SUBAGENT_CONFIGS[subagentType]) || DEFAULT_CONFIG;
    const streamingContent = useMemo(() => getStreamingContent(subagent.messages as unknown as SubagentMessage[]), [subagent.messages]);
    const toolCalls = subagent.toolCalls;

    useEffect(() => {
        if (scrollRef.current && subagent.status === "running" && isExpanded) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [streamingContent, toolCalls.length, subagent.status, isExpanded]);

    const displayContent = subagent.status === "complete" ? subagent.result : streamingContent;
    const hasToolCalls = toolCalls.length > 0;
    // @ts-ignore
    const hasContent = !!displayContent;

    return (
        <div className={`relative flex flex-col rounded-2xl border-2 transition-all duration-300 ${config.borderColor} ${config.bgColor} ${subagent.status === "running" ? "ring-2 ring-offset-2 ring-offset-black ring-opacity-50" : ""}`}>
            <div className={`flex items-center gap-3 px-4 py-3 cursor-pointer bg-gradient-to-r ${config.gradient} rounded-t-xl ${!isExpanded ? "rounded-b-xl" : "border-b border-neutral-800/50"}`} onClick={() => setIsExpanded(!isExpanded)}>
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${config.iconBg} ${config.accentColor}`}>{getSubagentIcon(subagentType)}</div>
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                        <h3 className={`font-semibold ${config.accentColor}`}>{config.title}</h3>
                        {hasToolCalls && <span className="flex items-center gap-1 text-xs text-neutral-500"><Wrench className="w-3 h-3" />{toolCalls.length}</span>}
                    </div>
                    <p className="text-xs text-neutral-500 truncate">{subagent.toolCall.args.description || "Working on task..."}</p>
                </div>
                <div className="flex items-center gap-2">
                    <StatusIcon status={subagent.status} accentColor={config.accentColor} />
                    {isExpanded ? <ChevronDown className="w-4 h-4 text-neutral-500" /> : <ChevronRight className="w-4 h-4 text-neutral-500" />}
                </div>
            </div>
            {isExpanded && (
                <>
                    {hasToolCalls && (
                        <div className="px-4 py-3 border-b border-neutral-800/50">
                            <div className="space-y-2">{toolCalls.map((tc: any) => <SubagentToolCallCard key={tc.id} toolCall={tc} accentColor={config.accentColor} />)}</div>
                        </div>
                    )}
                    <div ref={scrollRef} className="overflow-y-auto px-4 py-4 min-h-0 max-h-64">
                        {hasContent ? <div className="text-sm text-neutral-300 whitespace-pre-wrap">{displayContent as any}</div> : subagent.status === "running" ? <div className="animate-pulse text-sm">Working...</div> : null}
                    </div>
                </>
            )}
        </div>
    );
}
