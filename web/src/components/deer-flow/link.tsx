// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT
import { useMemo } from "react";
import { useStore, useToolCalls } from "~/core/store";
import { Tooltip } from "./tooltip";
import { WarningFilled } from "@ant-design/icons";

export const Link = ({
  href,
  children,
  checkLinkCredibility = false,
}: {
  href: string | undefined;
  children: React.ReactNode;
  checkLinkCredibility: boolean;
}) => {
  const toolCalls = useToolCalls();
  const responding = useStore((state) => state.responding);
  
  const credibleLinks = useMemo(() => {
    const links = new Set<string>();
    if (!checkLinkCredibility) return links;
    
    (toolCalls || []).forEach((call) => {
      if (call && call.name === "web_search" && call.result) {
        try {
          const result = JSON.parse(call.result);
          // Handle array of results (original format)
          if (Array.isArray(result)) {
            result.forEach((r) => {
              if (r.url) {
                links.add(r.url);
              }
              if (r.link) {
                links.add(r.link);
              }
            });
          }
        } catch (e) {
          console.warn('Failed to parse web_search result:', e);
        }
      }
    });
    return links;
  }, [toolCalls, checkLinkCredibility]);

  // Calculate if the current link is credible
  const isCredible = useMemo(() => {
    if (!checkLinkCredibility || !href) return true;
    return credibleLinks.has(href);
  }, [checkLinkCredibility, href, credibleLinks]);

  return (
    <span className="flex items-center gap-1.5">
      <a href={href} target="_blank" rel="noopener noreferrer">
        {children}
      </a>
      {checkLinkCredibility && !isCredible && (
        <Tooltip
          title="This link might be a hallucination from AI model and may not be reliable."
          delayDuration={300}
        >
          <WarningFilled className="text-sx transition-colors hover:!text-yellow-500" />
        </Tooltip>
      )}
    </span>
  );
};