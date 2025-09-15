import { getQueryClient } from "@/app/getQueryClient";
import { dehydrate, HydrationBoundary } from "@tanstack/react-query";
import Home from "../components/Home";

export default async function LoginPage() {
  const queryClient = getQueryClient();

  // prefetch data server-side
  // await queryClient.prefetchQuery({
  //   query key
  //   server action
  // });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Home />
    </HydrationBoundary>
  );
}
