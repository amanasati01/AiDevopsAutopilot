import { useMutation } from "@tanstack/react-query";
import { LoginRequest, RegisterRequest } from "../types";
import { login, register } from "@/features/auth/api/auth.api";

export function useRegister() {
  return useMutation({
    mutationFn: (data: RegisterRequest) => register(data),
  });
}
export function useLogin() {
  return useMutation({
    mutationFn: (data: LoginRequest) => login(data),
  });
}
