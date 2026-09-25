"use client";

import { useCallback, useLayoutEffect, useMemo, useRef, useState } from "react";
import { cn } from "@/lib/utils";

export type ERTreeNode = {
  id: string;
  label: string;
  children?: ERTreeNode[];
};

type LineSegment = { x1: number; y1: number; x2: number; y2: number; key: string };

/** Vertical space between depth rows — keeps connector curves readable. */
const ROW_GAP_PX = 56;

function collectByDepth(root: ERTreeNode): ERTreeNode[][] {
  const levels: ERTreeNode[][] = [];
  const walk = (node: ERTreeNode, depth: number) => {
    if (!levels[depth]) levels[depth] = [];
    levels[depth].push(node);
    for (const child of node.children ?? []) {
      walk(child, depth + 1);
    }
  };
  walk(root, 0);
  return levels;
}

function collectEdges(root: ERTreeNode): { from: string; to: string }[] {
  const edges: { from: string; to: string }[] = [];
  const walk = (node: ERTreeNode) => {
    for (const child of node.children ?? []) {
      edges.push({ from: node.id, to: child.id });
      walk(child);
    }
  };
  walk(root);
  return edges;
}

function EntityBox({
  node,
  depth,
  registerRef,
}: {
  node: ERTreeNode;
  depth: number;
  registerRef: (id: string, el: HTMLElement | null) => void;
}) {
  const isRoot = depth === 0;
  const isGroup = Boolean(node.children?.length) && !isRoot;

  return (
    <span
      ref={(el) => registerRef(node.id, el)}
      className={cn(
        "relative z-10 inline-flex max-w-full shrink-0 items-center rounded-lg border px-4 py-2.5 font-mono text-sm shadow-sm",
        isRoot &&
          "border-2 border-primary/60 bg-primary/10 px-5 py-3 text-base font-semibold",
        !isRoot && !isGroup && "border-border bg-card",
        isGroup && "border-primary/30 bg-muted/60 font-medium text-foreground",
      )}
    >
      {node.label}
    </span>
  );
}

function linePath(seg: LineSegment): string {
  const midY = (seg.y1 + seg.y2) / 2;
  return `M ${seg.x1} ${seg.y1} C ${seg.x1} ${midY}, ${seg.x2} ${midY}, ${seg.x2} ${seg.y2}`;
}

export function ERDiagramCanvas({ tree }: { tree: ERTreeNode }) {
  const levels = useMemo(() => collectByDepth(tree), [tree]);
  const edges = useMemo(() => collectEdges(tree), [tree]);
  const scrollRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLDivElement>(null);
  const nodeElements = useRef<Map<string, HTMLElement>>(new Map());
  const [lines, setLines] = useState<LineSegment[]>([]);
  const [size, setSize] = useState({ w: 0, h: 0 });

  const registerRef = useCallback((id: string, el: HTMLElement | null) => {
    if (el) nodeElements.current.set(id, el);
    else nodeElements.current.delete(id);
  }, []);

  const updateLines = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const cr = canvas.getBoundingClientRect();
    setSize({ w: canvas.offsetWidth, h: canvas.offsetHeight });

    const next: LineSegment[] = [];
    for (const { from, to } of edges) {
      const a = nodeElements.current.get(from);
      const b = nodeElements.current.get(to);
      if (!a || !b) continue;
      const ar = a.getBoundingClientRect();
      const br = b.getBoundingClientRect();
      next.push({
        key: `${from}-${to}`,
        x1: ar.left + ar.width / 2 - cr.left,
        y1: ar.bottom - cr.top,
        x2: br.left + br.width / 2 - cr.left,
        y2: br.top - cr.top,
      });
    }
    setLines(next);
  }, [edges]);

  useLayoutEffect(() => {
    updateLines();
    const canvas = canvasRef.current;
    const scrollEl = scrollRef.current;
    if (!canvas) return;

    const ro = new ResizeObserver(() => updateLines());
    ro.observe(canvas);
    window.addEventListener("resize", updateLines);
    scrollEl?.addEventListener("scroll", updateLines, { passive: true });

    return () => {
      ro.disconnect();
      window.removeEventListener("resize", updateLines);
      scrollEl?.removeEventListener("scroll", updateLines);
    };
  }, [updateLines, levels]);

  return (
    <div className="space-y-3">
      <p className="text-xs text-muted-foreground sm:text-sm">
        Scroll horizontally on smaller screens. Lines show parent → child (FK /
        ownership).
      </p>
      <div
        ref={scrollRef}
        className="overflow-x-auto overflow-y-visible rounded-lg border border-border/60 bg-muted/20"
      >
        <div
          ref={canvasRef}
          className="relative min-h-[36rem] min-w-[72rem] p-8 sm:min-w-[84rem] sm:p-12"
        >
          {size.w > 0 && size.h > 0 && (
            <svg
              className="pointer-events-none absolute left-0 top-0 z-0 text-primary"
              width={size.w}
              height={size.h}
              aria-hidden
            >
              {lines.map((seg) => (
                <g key={seg.key}>
                  <path
                    d={linePath(seg)}
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2}
                    strokeOpacity={0.55}
                  />
                  <circle
                    cx={seg.x2}
                    cy={seg.y2}
                    r={4}
                    className="fill-primary"
                    opacity={0.75}
                  />
                </g>
              ))}
            </svg>
          )}

          <div className="relative z-10 flex flex-col">
            {levels.map((nodes, depth) => (
              <div
                key={depth}
                style={{
                  marginBottom: depth < levels.length - 1 ? ROW_GAP_PX : 0,
                }}
              >
                <div className="flex min-h-[3.25rem] flex-row flex-wrap items-center gap-3 sm:gap-4">
                  {nodes.map((node) => (
                    <EntityBox
                      key={node.id}
                      node={node}
                      depth={depth}
                      registerRef={registerRef}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
