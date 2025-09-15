import { configureStore } from "@reduxjs/toolkit";
import analysisModalReducer from "./features/analysisModal/analysisModalSlice";
import analysisDetailReducer from "./features/analysisDetail/analysisDetailSlice";
import searchReducer from "./features/search/searchSlice";

// Factory function called on server to create a new store for each SSR request to keep state isolated
export const makeStore = () => {
  return configureStore({
    reducer: {
      analysisModal: analysisModalReducer,
      analysisDetail: analysisDetailReducer,
      search: searchReducer,
    },
  });
};

export type AppStore = ReturnType<typeof makeStore>;
export type RootState = ReturnType<AppStore["getState"]>;
export type AppDispatch = AppStore["dispatch"];
