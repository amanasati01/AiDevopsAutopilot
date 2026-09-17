"use client";
import { Provider } from "react-redux";
import { store } from "./index";

type StoreProviderProp = {
  children: React.ReactNode;
};
export default function StoreProvider({ children }: StoreProviderProp) {
  return <Provider store={store}>{children}</Provider>;
}
