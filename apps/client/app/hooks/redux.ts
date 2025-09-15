"use client";

import { useDispatch, useSelector, useStore } from "react-redux";
import type { RootState, AppDispatch, AppStore } from "@/lib/redux/store";

// Hooks to ensure better TypeScript support and avoid repetitive type definitions.
export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
export const useAppStore = useStore.withTypes<AppStore>();
