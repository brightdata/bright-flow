// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT
import { StarFilledIcon, GitHubLogoIcon } from "@radix-ui/react-icons";
import Link from "next/link";
import { NumberTicker } from "~/components/magicui/number-ticker";
import { Button } from "~/components/ui/button";
import { env } from "~/env";

export async function SiteHeader() {
  return (
    <header className="supports-backdrop-blur:bg-background/80 bg-background/40 sticky top-0 left-0 z-40 flex h-15 w-full flex-col items-center backdrop-blur-lg">
      <div className="container flex h-15 items-center justify-between px-3">
        <div className="text-xl font-medium flex items-center">
          <svg
            version="1.0"
            xmlns="http://www.w3.org/2000/svg"
            width="28"
            height="28"
            viewBox="0 0 148.000000 148.000000"
            preserveAspectRatio="xMidYMid meet"
            className="inline-block mr-1"
          >
            <g
              transform="translate(0.000000,148.000000) scale(0.100000,-0.100000)"
              fill="currentColor"
              stroke="none"
            >
              <path d="M131 1465 c-59 -18 -98 -59 -116 -119 -22 -74 -22 -1138 0 -1212 18
               -61 58 -101 120 -120 72 -21 1138 -21 1211 1 61 18 101 58 120 120 21 71 21
               1139 0 1210 -19 62 -59 102 -120 120 -70 21 -1148 21 -1215 0z m645 -313 c24
               -31 27 -32 44 -17 17 15 18 13 25 -53 5 -55 3 -76 -9 -101 -34 -65 -123 -81
               -178 -32 -35 31 -35 28 -25 166 2 40 4 41 28 19 17 -16 19 -15 29 10 5 15 10
               31 10 34 0 4 8 18 17 31 l16 24 9 -24 c5 -13 20 -38 34 -57z m72 -545 c2 -255
               3 -267 21 -267 40 0 51 -11 51 -51 l0 -39 -160 0 -160 0 0 39 c0 40 11 51 51
               51 19 0 19 8 17 202 l-3 202 -33 8 c-32 8 -33 11 -30 51 l3 42 110 16 c61 9
               115 16 120 15 6 -2 11 -102 13 -269z"/>
            </g>
          </svg>
          <span>BrightFlow</span>
        </div>
        <div className="relative flex items-center">
          <div
            className="pointer-events-none absolute inset-0 z-0 h-full w-full rounded-full opacity-60 blur-2xl"
            style={{
              background: "linear-gradient(90deg, #ff80b5 0%, #9089fc 100%)",
              filter: "blur(32px)",
            }}
          />
          <Button
            variant="outline"
            size="sm"
            asChild
            className="group relative z-10"
          >
            <Link href="https://github.com/meirk-brd/deer-flow" target="_blank">
              <GitHubLogoIcon className="size-4" />
              Star on GitHub
              {env.NEXT_PUBLIC_STATIC_WEBSITE_ONLY &&
                env.GITHUB_OAUTH_TOKEN && <StarCounter />}
            </Link>
          </Button>
        </div>
      </div>
      <hr className="from-border/0 via-border/70 to-border/0 m-0 h-px w-full border-none bg-gradient-to-r" />
    </header>
  );
}

export async function StarCounter() {
  let stars = 1000; // Default value
  try {
    const response = await fetch(
      "https://api.github.com/repos/bytedance/deer-flow",
      {
        headers: env.GITHUB_OAUTH_TOKEN
          ? {
              Authorization: `Bearer ${env.GITHUB_OAUTH_TOKEN}`,
              "Content-Type": "application/json",
            }
          : {},
        next: {
          revalidate: 3600,
        },
      },
    );
    if (response.ok) {
      const data = await response.json();
      stars = data.stargazers_count ?? stars; // Update stars if API response is valid
    }
  } catch (error) {
    console.error("Error fetching GitHub stars:", error);
  }
  return (
    <>
      <StarFilledIcon className="size-4 transition-colors duration-300 group-hover:text-yellow-500" />
      {stars && (
        <NumberTicker className="font-mono tabular-nums" value={stars} />
      )}
    </>
  );
}