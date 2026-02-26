export type AgentState = {
    messages: any[];
    subagent_type?: string;
};

// This is a mock agent object for useStream type inference
export const agent = {
    __brand: "agent"
} as any;
