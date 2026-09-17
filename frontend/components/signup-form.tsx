"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { AlertCircle, Loader2 } from "lucide-react";
import { cn } from "cn";

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
  FieldError,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { useRegister } from "@/features/auth/hooks/useAuth";
import { registerRequestSchema } from "@/features/auth/types";

export function SignupForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const router = useRouter();
  const registerMutation = useRegister();

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [apiError, setApiError] = useState<string | null>(null);
  const [githubNotice, setGithubNotice] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[name];
        return next;
      });
    }
    if (apiError) setApiError(null);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrors({});
    setApiError(null);
    const result = registerRequestSchema.safeParse(formData);
    if (!result.success) {
      const fieldError: Record<string, string> = {};
      result.error.issues.forEach((issue) => {
        const fieldName = issue.path[0] as string;
        if (fieldName && !fieldError[fieldName]) {
          fieldError[fieldName] = issue.message;
        }
      });
      setErrors(fieldError);
      return;
    }
    registerMutation.mutate(formData, {
      onSuccess: () => {
        router.push("/login?register=true");
      },
      onError: (err: any) => {
        const message =
          err?.response?.data?.detail ||
          err?.response?.data?.message ||
          "Registration failed. Please check your details and try again.";
        setApiError(message);
      },
    });
  };

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
          Create your account
        </CardTitle>
        <CardDescription className="text-xs sm:text-[13px] text-muted-foreground/80 leading-relaxed">
          Automate code reviews, detect risks, and ship with confidence.
        </CardDescription>
      </CardHeader>
      <CardContent className="px-6 sm:px-7 pb-5 sm:pb-6">
        <form onSubmit={handleSubmit} noValidate className="space-y-3.5">
          {apiError && (
            <div
              role="alert"
              className="flex items-start gap-2.5 rounded-xl border border-destructive/25 bg-destructive/[0.06] p-3 text-xs text-destructive font-medium animate-in fade-in slide-in-from-top-1 duration-200"
            >
              <AlertCircle className="size-4 shrink-0 mt-0.5" />
              <span>{apiError}</span>
            </div>
          )}

          <div className="grid grid-cols-1 gap-3.5 sm:grid-cols-2">
            <Field>
              <FieldLabel
                htmlFor="first_name"
                className="text-xs sm:text-[13px] font-medium"
              >
                First name
              </FieldLabel>
              <Input
                id="first_name"
                name="first_name"
                type="text"
                placeholder="John"
                value={formData.first_name}
                onChange={handleChange}
                required
                aria-invalid={!!errors.first_name}
                className={cn(
                  "h-9.5 bg-background/80 rounded-lg border-border/60 text-sm placeholder:text-muted-foreground/50 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-ring/30 focus-visible:border-ring/50",
                  errors.first_name &&
                    "border-destructive focus-visible:ring-destructive/30",
                )}
              />
              {errors.first_name && (
                <FieldError>{errors.first_name}</FieldError>
              )}
            </Field>

            <Field>
              <FieldLabel
                htmlFor="last_name"
                className="text-xs sm:text-[13px] font-medium"
              >
                Last name
              </FieldLabel>
              <Input
                id="last_name"
                name="last_name"
                type="text"
                placeholder="Doe"
                value={formData.last_name}
                onChange={handleChange}
                required
                aria-invalid={!!errors.last_name}
                className={cn(
                  "h-9.5 bg-background/80 rounded-lg border-border/60 text-sm placeholder:text-muted-foreground/50 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-ring/30 focus-visible:border-ring/50",
                  errors.last_name &&
                    "border-destructive focus-visible:ring-destructive/30",
                )}
              />
              {errors.last_name && <FieldError>{errors.last_name}</FieldError>}
            </Field>
          </div>

          <Field>
            <FieldLabel
              htmlFor="username"
              className="text-xs sm:text-[13px] font-medium"
            >
              Username
            </FieldLabel>
            <Input
              id="username"
              name="username"
              type="text"
              placeholder="johndoe"
              value={formData.username}
              onChange={handleChange}
              required
              aria-invalid={!!errors.username}
              className={cn(
                "h-9.5 bg-background/80 rounded-lg border-border/60 text-sm placeholder:text-muted-foreground/50 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-ring/30 focus-visible:border-ring/50",
                errors.username &&
                  "border-destructive focus-visible:ring-destructive/30",
              )}
            />
            {errors.username ? (
              <FieldError>{errors.username}</FieldError>
            ) : (
              <FieldDescription className="text-[11px] text-muted-foreground/60">
                3 to 10 characters.
              </FieldDescription>
            )}
          </Field>

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
              value={formData.email}
              onChange={handleChange}
              required
              aria-invalid={!!errors.email}
              className={cn(
                "h-9.5 bg-background/80 rounded-lg border-border/60 text-sm placeholder:text-muted-foreground/50 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-ring/30 focus-visible:border-ring/50",
                errors.email &&
                  "border-destructive focus-visible:ring-destructive/30",
              )}
            />
            {errors.email && <FieldError>{errors.email}</FieldError>}
          </Field>

          <Field>
            <FieldLabel
              htmlFor="password"
              className="text-xs sm:text-[13px] font-medium"
            >
              Password
            </FieldLabel>
            <Input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
              required
              aria-invalid={!!errors.password}
              className={cn(
                "h-9.5 bg-background/80 rounded-lg border-border/60 text-sm placeholder:text-muted-foreground/50 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-ring/30 focus-visible:border-ring/50",
                errors.password &&
                  "border-destructive focus-visible:ring-destructive/30",
              )}
            />
            {errors.password ? (
              <FieldError>{errors.password}</FieldError>
            ) : (
              <FieldDescription className="text-[11px] text-muted-foreground/60">
                Must be at least 8 characters.
              </FieldDescription>
            )}
          </Field>

          <div className="pt-0.5">
            <Button
              type="submit"
              disabled={registerMutation.isPending}
              className="w-full h-10 font-semibold text-sm tracking-wide rounded-lg transition-all duration-200 cursor-pointer shadow-sm hover:shadow-md active:scale-[0.99]"
            >
              {registerMutation.isPending ? (
                <>
                  <Loader2 className="mr-2 size-4 animate-spin" />
                  Creating account...
                </>
              ) : (
                "Create Account"
              )}
            </Button>
          </div>

          <FieldSeparator>Or continue with</FieldSeparator>

          <div className="space-y-2">
            <Button
              variant="outline"
              type="button"
              className="w-full h-10 font-medium text-sm rounded-lg border-border/60 hover:bg-muted/60 hover:border-border transition-all duration-200 cursor-pointer"
              onClick={() => setGithubNotice(true)}
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
              Sign up with GitHub
            </Button>
            {githubNotice && (
              <p className="text-[11px] text-center text-muted-foreground/70 animate-in fade-in slide-in-from-bottom-1 duration-200">
                GitHub OAuth will be supported soon. Please use email
                registration above.
              </p>
            )}
          </div>

          <div className="pt-1 text-center text-xs sm:text-[13px] text-muted-foreground/70">
            Already have an account?{" "}
            <Link
              href="/login"
              className="font-semibold text-primary hover:text-primary/80 hover:underline underline-offset-4 focus-visible:outline-hidden focus-visible:ring-1 focus-visible:ring-ring rounded-xs transition-colors duration-150"
            >
              Sign in
            </Link>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
