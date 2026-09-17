import { z } from "zod";

export const registerRequestSchema = z.object({
  first_name: z.string().min(1).max(50),
  last_name: z.string().min(1).max(50),
  username: z.string().min(3).max(10),
  email: z.email(),
  password: z.string().min(8).max(128),
});

export const registerResponseSchema = z.object({
  id: z.uuid(),
  first_name: z.string().min(1).max(50),
  last_name: z.string().min(1).max(50),
  username: z.string().min(3).max(10),
  email: z.email(),
});
export type RegisterRequest = z.infer<typeof registerRequestSchema>;
export type RegisterResponse = z.infer<typeof registerResponseSchema>;
export const loginSchema = z.object({
  email: z.email(),
  password: z.string().min(8).max(128),
});
export const tokenSchema = z.object({
  access_token: z.string(),
  token_type: "bearer",
});
export type TokenResponse = z.infer<typeof tokenSchema>;
export type LoginRequest = z.infer<typeof loginSchema>;
