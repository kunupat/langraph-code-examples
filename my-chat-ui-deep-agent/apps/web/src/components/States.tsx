import { MessageCircle, type LucideIcon } from "lucide-react";

interface EmptyStateProps {
    icon?: LucideIcon;
    title?: string;
    description?: string;
    suggestions?: string[];
    onSuggestionClick?: (suggestion: string) => void;
}

export function EmptyState({
    icon: Icon = MessageCircle,
    title = "How can I help you today?",
    description = "Send a message to start a conversation with the AI assistant.",
    suggestions = [],
    onSuggestionClick,
}: EmptyStateProps) {
    return (
        <div className="flex-1 flex flex-col items-center justify-center text-center px-4 py-24">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/20 to-neutral-800/30 border border-blue-500/30 flex items-center justify-center mb-6">
                <Icon className="w-8 h-8 text-blue-500" strokeWidth={1.5} />
            </div>
            <h2 className="text-xl font-semibold text-white mb-2">{title}</h2>
            <p className="text-neutral-400 max-w-md mb-6 leading-relaxed">
                {description}
            </p>

            {suggestions.length > 0 && (
                <div className="flex flex-wrap gap-2 justify-center">
                    {suggestions.map((suggestion) => (
                        <button
                            key={suggestion}
                            onClick={() => onSuggestionClick?.(suggestion)}
                            className="px-3 py-1.5 rounded-full bg-neutral-800/40 hover:bg-neutral-800/60 text-neutral-100 text-xs transition-colors border border-neutral-700/20 hover:border-neutral-700/40 cursor-pointer"
                        >
                            {suggestion}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
