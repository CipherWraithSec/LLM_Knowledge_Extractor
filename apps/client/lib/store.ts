import { configureStore, createSlice, PayloadAction } from '@reduxjs/toolkit'
import { Analysis, AnalysisModalState, SearchState } from './types'

// Analysis Modal Slice
const initialAnalysisModalState: AnalysisModalState = {
  isOpen: false,
  isAnalyzing: false,
  text: '',
  result: null,
  error: null,
}

const analysisModalSlice = createSlice({
  name: 'analysisModal',
  initialState: initialAnalysisModalState,
  reducers: {
    openModal: (state) => {
      state.isOpen = true
      state.text = ''
      state.result = null
      state.error = null
    },
    closeModal: (state) => {
      state.isOpen = false
      state.text = ''
      state.result = null
      state.error = null
    },
    setText: (state, action: PayloadAction<string>) => {
      state.text = action.payload
    },
    setAnalyzing: (state, action: PayloadAction<boolean>) => {
      state.isAnalyzing = action.payload
    },
    setResult: (state, action: PayloadAction<Analysis>) => {
      state.result = action.payload
      state.isAnalyzing = false
      state.error = null
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload
      state.isAnalyzing = false
    },
  },
})

// Search Slice
const initialSearchState: SearchState = {
  query: '',
  filters: {
    query: '',
  },
  isSearching: false,
}

const searchSlice = createSlice({
  name: 'search',
  initialState: initialSearchState,
  reducers: {
    setQuery: (state, action: PayloadAction<string>) => {
      state.query = action.payload
      state.filters.query = action.payload
    },
    setSearching: (state, action: PayloadAction<boolean>) => {
      state.isSearching = action.payload
    },
    clearSearch: (state) => {
      state.query = ''
      state.filters.query = ''
      state.isSearching = false
    },
  },
})

// Configure store
export const store = configureStore({
  reducer: {
    analysisModal: analysisModalSlice.reducer,
    search: searchSlice.reducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

// Action exports
export const analysisModalActions = analysisModalSlice.actions
export const searchActions = searchSlice.actions