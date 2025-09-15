import { useAppSelector } from "@/app/hooks/redux";
import { SearchState } from "@/lib/types";
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

const initialState: SearchState = {
  query: "",
  filters: {
    query: "",
  },
  isSearching: false,
  pagination: {
    limit: 10, // Default page size
  },
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
    setPaginationLimit: (state, action: PayloadAction<number>) => {
      state.pagination.limit = action.payload;
    },
    clearSearch: (state) => {
      state.query = "";
      state.filters.query = "";
      state.isSearching = false;
    },
  },
});

export const useSearch = () => useAppSelector((state) => state.search);

export const { 
  setQuery, 
  setSearching, 
  setPaginationLimit, 
  clearSearch 
} = searchSlice.actions;
export default searchSlice.reducer;
