"use client";

import { ArchitectureOverview } from "@/components/architecture/architecture-overview";
import { ArchitectureReviewHeader } from "@/components/architecture/review-header";
import { DataFlowDiagram } from "@/components/architecture/data-flow-diagram";
import { ERDiagram } from "@/components/architecture/er-diagram";
import { MLDataFlow } from "@/components/architecture/ml-data-flow";
import { MultiTenancyDiagram } from "@/components/architecture/multi-tenancy-diagram";
import { SchemaExplorer } from "@/components/architecture/schema-explorer";
import { SecurityFlow } from "@/components/architecture/security-flow";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export function ArchitecturePage() {
  return (
    <div className="flex min-h-svh flex-col bg-background">
      <ArchitectureReviewHeader />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-6 lg:px-8">
        <Tabs defaultValue="overview" className="gap-6">
          <TabsList className="flex h-auto w-full flex-wrap justify-start gap-1 bg-muted/50 p-1">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="schema">Database schema</TabsTrigger>
            <TabsTrigger value="tenancy">Multi-tenancy</TabsTrigger>
            <TabsTrigger value="er">Entity relationships</TabsTrigger>
            <TabsTrigger value="dataflow">Data flow</TabsTrigger>
            <TabsTrigger value="security">Security & access</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="mt-0">
            <ArchitectureOverview />
          </TabsContent>
          <TabsContent value="schema" className="mt-0">
            <SchemaExplorer />
          </TabsContent>
          <TabsContent value="tenancy" className="mt-0">
            <MultiTenancyDiagram />
          </TabsContent>
          <TabsContent value="er" className="mt-0">
            <ERDiagram />
          </TabsContent>
          <TabsContent value="dataflow" className="mt-0 space-y-8">
            <DataFlowDiagram />
            <MLDataFlow />
          </TabsContent>
          <TabsContent value="security" className="mt-0">
            <SecurityFlow />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
