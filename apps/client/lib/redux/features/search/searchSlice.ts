import { useAppSelector } from "@/app/hooks/redux";
import { SearchState } from "@/lib/types";
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

const initialState: SearchState = {
  query: "",
  filters: {
    query: "",
  },
  isSearching: false,
};

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    setQuery: (state, action: PayloadAction<string>) => {
      state.query = action.payload;
      state.filters.query = action.payload;
    },
    setSearching: (state, action: PayloadAction<boolean>) => {
      state.isSearching = action.payload;
    },
    clearSearch: (state) => {
      state.query = "";
      state.filters.query = "";
      state.isSearching = false;
    },
  },
});

export const useSearch = () => useAppSelector((state) => state.search);

export const { setQuery, setSearching, clearSearch } = searchSlice.actions;
export default searchSlice.reducer;
