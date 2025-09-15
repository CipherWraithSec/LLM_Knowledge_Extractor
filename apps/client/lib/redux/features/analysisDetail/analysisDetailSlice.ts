import { useAppSelector } from "@/app/hooks/redux";
import { Analysis } from "@/lib/types";
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

interface AnalysisDetailState {
  isOpen: boolean;
  analysis: Analysis | null;
}

const initialState: AnalysisDetailState = {
  isOpen: false,
  analysis: null,
};

const analysisDetailSlice = createSlice({
  name: "analysisDetail",
  initialState,
  reducers: {
    openModal: (state, action: PayloadAction<Analysis>) => {
      state.isOpen = true;
      state.analysis = action.payload;
    },
    closeModal: (state) => {
      state.isOpen = false;
      state.analysis = null;
    },
  },
});

export const useAnalysisDetail = () =>
  useAppSelector((state) => state.analysisDetail);

export const { openModal, closeModal } = analysisDetailSlice.actions;
export default analysisDetailSlice.reducer;