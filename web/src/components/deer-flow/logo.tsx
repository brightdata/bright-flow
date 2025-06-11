// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT
import Link from "next/link";

function BrightFlowIcon() {
  return (
    <svg 
      version="1.0" 
      xmlns="http://www.w3.org/2000/svg"
      width="20" 
      height="20" 
      viewBox="0 0 148.000000 148.000000"
      preserveAspectRatio="xMidYMid meet"
      className="inline-block"
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
  );
}

export function Logo() {
  return (
    <Link
      className="opacity-70 transition-opacity duration-300 hover:opacity-100 flex items-center gap-2"
      href="/"
    >
      <BrightFlowIcon />
      BrightFlow
    </Link>
  );
}