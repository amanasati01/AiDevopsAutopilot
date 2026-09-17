"use client";

import Link from "next/link";
import React from "react";
import { cn } from "@/lib/utils";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";

function LoginPage({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <Card
      className={cn(
        "w-full border-border/50 shadow-lg shadow-black/[0.03] bg-card/98 backdrop-blur-sm transition-all duration-300",
        className,
      )}
      {...props}
    >
      <CardHeader className="space-y-1.5 pb-2 pt-5 px-6 sm:px-7">
        <CardTitle className="text-2xl font-bold tracking-tight text-foreground">
          Welcome back
        </CardTitle>

        <CardDescription className="text-xs sm:text-[13px] text-muted-foreground/80 leading-relaxed">
          Sign in to manage your projects, pull requests, and AI-powered code
          analysis.
        </CardDescription>
      </CardHeader>

      <CardContent className="px-6 sm:px-7 pb-5 sm:pb-6">
        <form className="space-y-4">
          <Field>
            <FieldLabel
              htmlFor="email"
              className="text-xs sm:text-[13px] font-medium"
            >
              Work Email
            </FieldLabel>

            <Input
              id="email"
              name="email"
              type="email"
              placeholder="john@company.com"
              className="h-9.5 bg-background/80 rounded-lg border-border/60 text-sm placeholder:text-muted-foreground/50 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-ring/30 focus-visible:border-ring/50"
            />
          </Field>

          <Field>
            <div className="flex items-center justify-between">
              <FieldLabel
                htmlFor="password"
                className="text-xs sm:text-[13px] font-medium"
              >
                Password
              </FieldLabel>

              <Link
                href="#"
                className="text-[11px] sm:text-xs font-medium text-primary hover:underline underline-offset-4"
              >
                Forgot password?
              </Link>
            </div>

            <Input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              className="h-9.5 bg-background/80 rounded-lg border-border/60 text-sm placeholder:text-muted-foreground/50 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-ring/30 focus-visible:border-ring/50"
            />

            <FieldDescription className="text-[11px] text-muted-foreground/60">
              Must be at least 8 characters.
            </FieldDescription>
          </Field>

          <div className="pt-0.5">
            <Button
              type="submit"
              className="w-full h-10 font-semibold text-sm tracking-wide rounded-lg transition-all duration-200 cursor-pointer shadow-sm hover:shadow-md active:scale-[0.99]"
            >
              Sign In
            </Button>
          </div>

          <FieldSeparator>Or continue with</FieldSeparator>

          <Button
            variant="outline"
            type="button"
            className="w-full h-10 font-medium text-sm rounded-lg border-border/60 hover:bg-muted/60 hover:border-border transition-all duration-200 cursor-pointer"
          >
            <svg
              className="size-4 mr-2 shrink-0"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
            >
              <path
                d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
                fill="currentColor"
              />
            </svg>
            Continue with GitHub
          </Button>

          <div className="pt-1 text-center text-xs sm:text-[13px] text-muted-foreground/70">
            Don't have an account?{" "}
            <Link
              href="/register"
              className="font-semibold text-primary hover:text-primary/80 hover:underline underline-offset-4 focus-visible:outline-hidden focus-visible:ring-1 focus-visible:ring-ring rounded-xs transition-colors duration-150"
            >
              Create an account
            </Link>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

export default LoginPage;
