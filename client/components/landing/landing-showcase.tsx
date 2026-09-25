"use client";

import Image from "next/image";
import { useCallback, useEffect, useState } from "react";
import { IconX, IconZoomIn } from "@tabler/icons-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export type ShowcaseItem = {
  src: string;
  alt: string;
  title: string;
  lead: string;
  bullets: string[];
};

export function LandingShowcase({ items }: { items: ShowcaseItem[] }) {
  const [active, setActive] = useState<ShowcaseItem | null>(null);

  const close = useCallback(() => setActive(null), []);

  useEffect(() => {
    if (!active) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", onKey);
    };
  }, [active, close]);

  return (
    <>
      <div className="space-y-20 sm:space-y-28">
        {items.map((item, index) => {
          const imageFirst = index % 2 === 1;
          return (
            <article
              key={item.src}
              className="grid items-center gap-8 lg:grid-cols-2 lg:gap-12"
            >
              <div className={imageFirst ? "lg:order-2" : undefined}>
                <h3 className="font-heading text-xl font-semibold tracking-tight text-foreground sm:text-2xl">
                  {item.title}
                </h3>
                <p className="mt-3 text-sm leading-relaxed text-muted-foreground sm:text-base">
                  {item.lead}
                </p>
                <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                  {item.bullets.map((bullet) => (
                    <li key={bullet} className="flex gap-2">
                      <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-primary" />
                      <span>{bullet}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <button
                type="button"
                onClick={() => setActive(item)}
                className={cn(
                  "group relative overflow-hidden rounded-lg border border-border/70 bg-muted/20 text-left shadow-sm transition-shadow hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
                  imageFirst ? "lg:order-1" : undefined,
                )}
                aria-label={`View full screen: ${item.title}`}
              >
                <Image
                  src={item.src}
                  alt={item.alt}
                  width={1280}
                  height={720}
                  className="h-auto w-full"
                  sizes="(max-width: 1024px) 100vw, 50vw"
                />
                <span
                  className="pointer-events-none absolute inset-0 flex items-center justify-center bg-black/0 transition-colors group-hover:bg-black/25"
                  aria-hidden
                >
                  <span className="flex items-center gap-1.5 rounded-full bg-background/90 px-3 py-1.5 text-xs font-medium text-foreground opacity-0 shadow-sm transition-opacity group-hover:opacity-100">
                    <IconZoomIn className="size-3.5" />
                    Expand
                  </span>
                </span>
              </button>
            </article>
          );
        })}
      </div>

      {active && (
        <div
          className="fixed inset-0 z-100 flex flex-col bg-black/95"
          role="dialog"
          aria-modal="true"
          aria-label={active.title}
        >
          <div className="flex shrink-0 items-center justify-between gap-4 border-b border-white/10 px-4 py-3 sm:px-6">
            <p className="truncate text-sm font-medium text-white/90 sm:text-base">
              {active.title}
            </p>
            <Button
              type="button"
              variant="ghost"
              size="icon-sm"
              className="shrink-0 text-white hover:bg-white/10 hover:text-white"
              onClick={close}
              aria-label="Close"
            >
              <IconX className="size-5" />
            </Button>
          </div>
          <button
            type="button"
            className="flex min-h-0 flex-1 items-center justify-center p-4 sm:p-8"
            onClick={close}
            aria-label="Close preview"
          >
            {/* eslint-disable-next-line @next/next/no-img-element -- full-resolution lightbox */}
            <img
              src={active.src}
              alt={active.alt}
              className="max-h-full max-w-full object-contain"
              onClick={(e) => e.stopPropagation()}
            />
          </button>
          <p className="shrink-0 pb-4 text-center text-xs text-white/50">
            Esc or click outside the image to close
          </p>
        </div>
      )}
    </>
  );
}
