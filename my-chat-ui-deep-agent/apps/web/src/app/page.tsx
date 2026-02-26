"use client";

import DeepAgentToolsDemo from "@/examples/deepagent-tools";
import { Toaster } from "@/components/ui/sonner";
import React from "react";

export default function DemoPage(): React.ReactNode {
  return (
    <React.Suspense fallback={<div>Loading (layout)...</div>}>
      <Toaster />
      <DeepAgentToolsDemo />
    </React.Suspense>
  );
}

