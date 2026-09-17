import {
  LoginRequest,
  TokenResponse,
  RegisterRequest,
  RegisterResponse,
} from "../types";
import api from "@/lib/api/axios";

export async function register(
  data: RegisterRequest,
): Promise<RegisterResponse> {
  const response = await api.post<RegisterResponse>("/auth/register", data);
  return response.data;
}
export async function login(data: LoginRequest): Promise<TokenResponse> {
  const response = await api.post<TokenResponse>("/auth/login", data);
  return response.data;
}
