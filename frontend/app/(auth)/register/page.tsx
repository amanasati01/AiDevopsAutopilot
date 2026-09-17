"use client";

import Link from "next/link";
import { Workflow } from "lucide-react";
import { SignupForm } from "@/components/signup-form";

export default function SignupPage() {
  return (
    <div className="grid h-svh w-full lg:grid-cols-2 bg-background overflow-y-auto lg:overflow-hidden">
      {/* Left Column: Form & Branding */}
      <div className="relative flex flex-col justify-between p-6 sm:p-8 lg:p-10 xl:p-12 h-full">
        {/* Subtle Background Glow & Grid Pattern */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_70%_50%_at_30%_-10%,rgba(99,102,241,0.07),rgba(255,255,255,0))] dark:bg-[radial-gradient(ellipse_70%_50%_at_30%_-10%,rgba(99,102,241,0.12),rgba(0,0,0,0))] pointer-events-none" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:32px_32px] pointer-events-none" />

        <header className="relative z-10 flex justify-start shrink-0">
          <Link
            href="/"
            className="flex items-center gap-3 group w-fit transition-opacity hover:opacity-90 focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-ring rounded-lg p-1"
          >
            <div className="flex size-10 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-md ring-1 ring-primary/20">
              <Workflow className="size-5" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-base tracking-tight text-foreground group-hover:text-primary transition-colors leading-tight">
                AI DevOps Autopilot
              </span>
              <span className="text-[10px] font-semibold text-muted-foreground/70 uppercase tracking-[0.15em]">
                DevOps Intelligence
              </span>
            </div>
          </Link>
        </header>

        <main className="relative z-10 my-auto flex flex-1 items-center justify-center py-2">
          <div className="w-full max-w-[420px]">
            <SignupForm />
          </div>
        </main>

        <footer className="relative z-10 text-center text-xs text-muted-foreground/60 tracking-wide shrink-0">
          &copy; {new Date().getFullYear()} AI DevOps Autopilot. All rights reserved.
        </footer>
      </div>

      {/* Right Column: AI DevOps Illustration Showcase */}
      <div className="relative hidden lg:block h-full w-full bg-slate-950 overflow-hidden select-none">
        <img
          src="/images/auth/RegisterPage.png"
          alt="AI DevOps Autopilot platform workflow diagram illustrating PR analysis, security scanning, CI/CD pipeline monitoring, and risk detection"
          className="w-full h-full object-cover object-center"
        />
        {/* Subtle overlay gradients for polish */}
        <div className="absolute inset-y-0 left-0 w-px bg-white/[0.08] pointer-events-none" />
        <div className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-slate-950/40 to-transparent pointer-events-none" />
      </div>
    </div>
  );
}
