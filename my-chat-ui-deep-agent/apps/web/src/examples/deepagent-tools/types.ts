export type SubagentType = "researcher" | "data-analyst" | "content-writer";

export const SUBAGENT_CONFIGS: Record<
    SubagentType,
    {
        icon: string;
        title: string;
        gradient: string;
        borderColor: string;
        bgColor: string;
        iconBg: string;
        accentColor: string;
    }
> = {
    researcher: {
        icon: "search",
        title: "Research Specialist",
        gradient: "from-blue-500/20 to-indigo-600/20",
        borderColor: "border-blue-500/40",
        bgColor: "bg-blue-950/30",
        iconBg: "bg-blue-500/20",
        accentColor: "text-blue-400",
    },
    "data-analyst": {
        icon: "bar-chart",
        title: "Data Analyst",
        gradient: "from-emerald-500/20 to-teal-600/20",
        borderColor: "border-emerald-500/40",
        bgColor: "bg-emerald-950/30",
        iconBg: "bg-emerald-500/20",
        accentColor: "text-emerald-400",
    },
    "content-writer": {
        icon: "pen-line",
        title: "Content Strategist",
        gradient: "from-purple-500/20 to-pink-600/20",
        borderColor: "border-purple-500/40",
        bgColor: "bg-purple-950/30",
        iconBg: "bg-purple-500/20",
        accentColor: "text-purple-400",
    },
};
