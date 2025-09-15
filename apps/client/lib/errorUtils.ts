// Simple error message extraction for toast notifications
export const getErrorMessage = (error: any): string => {
  // API error with standardized message
  if (error?.response?.data?.message) {
    return error.response.data.message;
  }
  
  // Pydantic validation errors  
  if (error?.response?.data?.detail?.[0]?.msg) {
    return error.response.data.detail[0].msg;
  }
  
  // Generic error with message
  if (error?.message) {
    return error.message;
  }
  
  // Default fallback
  return "An error occurred";
};