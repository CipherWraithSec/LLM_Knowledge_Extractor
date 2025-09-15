import { useAppSelector } from "@/app/hooks/redux";
import { Analysis, AnalysisModalState } from "@/lib/types";
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

const initialState: AnalysisModalState = {
  isOpen: false,
  isAnalyzing: false,
  text: "",
  result: null,
  error: null,
};

const analysisModalSlice = createSlice({
  name: "analysisModal",
  initialState,
  reducers: {
    openModal: (state) => {
      state.isOpen = true;
      state.text = "";
      state.result = null;
      state.error = null;
    },
    closeModal: (state) => {
      state.isOpen = false;
      state.text = "";
      state.result = null;
      state.error = null;
    },
    setText: (state, action: PayloadAction<string>) => {
      state.text = action.payload;
    },
    setAnalyzing: (state, action: PayloadAction<boolean>) => {
      state.isAnalyzing = action.payload;
    },
    setResult: (state, action: PayloadAction<Analysis>) => {
      state.result = action.payload;
      state.isAnalyzing = false;
      state.error = null;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isAnalyzing = false;
    },
  },
});

export const useAnalysisModal = () =>
  useAppSelector((state) => state.analysisModal);

export const {
  openModal,
  closeModal,
  setText,
  setAnalyzing,
  setResult,
  setError,
} = analysisModalSlice.actions;
export default analysisModalSlice.reducer;
