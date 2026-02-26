import { Brain } from "lucide-react";
import type { Message } from "@langchain/langgraph-sdk";

// Styles for each message type - kept separate for readability
const BUBBLE_STYLES = {
    human:
        "bg-neutral-800 text-neutral-100 rounded-2xl px-4 py-2.5 ml-auto max-w-[85%] md:max-w-[70%] w-fit",
    system:
        "bg-amber-500/10 border border-amber-500/20 text-amber-200 rounded-lg px-4 py-3",
    ai: "text-neutral-100",
} as const;

/**
 * Extract text content from a message
 */
function getTextContent(message: Message): string {
    if (typeof message.content === "string") {
        return message.content;
    }
    if (Array.isArray(message.content)) {
        return message.content
            .filter((c: any): c is { type: "text"; text: string } => c.type === "text")
            .map((c) => c.text)
            .join("\n");
    }
    return "";
}

export function MessageBubble({ message }: { message: Message }) {
    const isAI = message.type === "ai";
    const isHuman = message.type === "human";
    const content = getTextContent(message);

    if (!content && isHuman) return null;

    return (
        <div
            className={`flex flex-col gap-2 animate-fade-in ${isHuman ? "items-end" : "items-start"
                }`}
        >
            {/* Grouping Header (e.g., Assistant Label) */}
            {!isHuman && (
                <div className="flex items-center gap-2 mb-1 px-1">
                    <div className="w-5 h-5 rounded-md bg-blue-500/20 border border-blue-500/30 flex items-center justify-center">
                        <Brain className="w-3 h-3 text-blue-500" />
                    </div>
                    <span className="text-xs font-medium text-neutral-400">Assistant</span>
                </div>
            )}

            {/* Bubble Content */}
            <div className={BUBBLE_STYLES[message.type as keyof typeof BUBBLE_STYLES]}>
                {content && (
                    <p className="text-sm leading-relaxed whitespace-pre-wrap tracking-wide">
                        {content}
                    </p>
                )}
            </div>
        </div>
    );
}
