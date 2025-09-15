"use client";

import { Search, Plus } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useAppDispatch } from "@/app/hooks/redux";
import { setQuery, useSearch } from "@/lib/redux/features/search/searchSlice";
import { openModal } from "@/lib/redux/features/analysisModal/analysisModalSlice";

export function Header() {
  const dispatch = useAppDispatch();
  const { query: searchQuery } = useSearch();

  const handleSearchChange = (query: string) => {
    dispatch(setQuery(query));
  };

  const handleNewAnalysis = () => {
    dispatch(openModal());
  };
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className=" flex h-16 items-center justify-between px-4 md:px-6">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-2">
            <span className="text-2xl">🧠</span>
            <h1 className="sm:inline text-xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent hidden ">
              Knowledge Extractor
            </h1>
          </div>
        </div>

        {/* Search Input */}
        <div className="flex-1 max-w-lg mx-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search analyses..."
              value={searchQuery}
              onChange={(e) => handleSearchChange(e.target.value)}
              className="pl-9 pr-4"
            />
          </div>
        </div>

        {/* New Analysis Button */}
        <Button
          onClick={handleNewAnalysis}
          className="flex items-center space-x-2"
          size="sm"
        >
          <Plus className="h-4 w-4" />
          <span className="hidden sm:inline">New Analysis</span>
        </Button>
      </div>
    </header>
  );
}
