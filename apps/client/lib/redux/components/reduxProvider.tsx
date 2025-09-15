"use client";
import { useRef } from "react";
import { Provider } from "react-redux";
import { AppStore, makeStore } from "../store";

interface ProvidersProps {
  children: React.ReactNode;
}

const ReduxProvider = ({ children }: ProvidersProps) => {
  // Ensures the store is created only once on the client side, maintaining its state throughout the user's session.
  const storeRef = useRef<AppStore | null>(null);

  if (!storeRef.current) {
    // Create the store instance the first time this component is rendered
    storeRef.current = makeStore();
  }

  return <Provider store={storeRef.current}>{children}</Provider>;
};

export default ReduxProvider;
