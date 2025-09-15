import { useAppSelector } from "@/app/hooks/redux";
import { Analysis, AnalysisModalState } from "@/lib/types";
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

const initialState: AnalysisModalState = {
  isOpen: false,
  text: "",
};

const analysisModalSlice = createSlice({
  name: "analysisModal",
  initialState,
  reducers: {
    openModal: (state) => {
      state.isOpen = true;
      state.text = "";
    },
    closeModal: (state) => {
      state.isOpen = false;
      state.text = "";
    },
    setText: (state, action: PayloadAction<string>) => {
      state.text = action.payload;
    },
  },
});

export const useAnalysisModal = () =>
  useAppSelector((state) => state.analysisModal);

export const {
  openModal,
  closeModal,
  setText,
} = analysisModalSlice.actions;
export default analysisModalSlice.reducer;
